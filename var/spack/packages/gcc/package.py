##############################################################################
# Copyright (c) 2013, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Written by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://scalability-llnl.github.io/spack
# Please also see the LICENSE file for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License (as published by
# the Free Software Foundation) version 2.1 dated February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
from spack import *

from contextlib import closing
from glob import glob

class Gcc(Package):
    """The GNU Compiler Collection includes front ends for C, C++,
       Objective-C, Fortran, and Java."""
    homepage = "https://gcc.gnu.org"

    url = "http://open-source-box.org/gcc/gcc-4.9.2/gcc-4.9.2.tar.bz2"
    list_url = 'http://open-source-box.org/gcc/'
    list_depth = 2

    # Currently maintained versions
    version('5.2.0', 'a51bcfeb3da7dd4c623e27207ed43467')
    version('4.9.3', '6f831b4d251872736e8e9cc09746f327')
    version('4.8.5', '80d2c2982a3392bb0b89673ff136e223')    
    # Dependencies variants
    variant('binutils', default=False, description='Add a dependency on binutils')
    variant('libelf', default=False, description='Add a dependency on libelf')
    variant('isl', default=True, description='Add a dependency on isl')
    # Language variants
    variant('go', default=False, description='Add go to the list of enabled languages')
    variant('java', default=False, description='Add java to the list of enabled languages')
    variant('objc', default=False, description='Add objc to the list of enabled languages')

    depends_on("mpfr")
    depends_on("gmp")
    depends_on("mpc")     # when @4.5:
    depends_on("libelf", when='+libelf')
    depends_on("binutils",when="+binutils")

    # Save these until we can do optional deps.
    depends_on("isl", when='@5.0:+isl')
    #depends_on("ppl")
    #depends_on("cloog")

    def install(self, spec, prefix):
        enabled_languages = set(('c', 'c++', 'fortran'))
        if spec.satisfies("@4.7.1:+go"):
            enabled_languages.add('go')

        if '+java' in spec:
            # libjava/configure needs a minor fix to install into spack paths.
            filter_file(r"'@.*@'", "'@[[:alnum:]]*@'", 'libjava/configure', string=True)
            enabled_languages.add('java')

        if 'objc' in spec:
            enabled_languages.add('objc')

        # Generic options to compile GCC
        options = ["--prefix=%s" % prefix,
                   #"--libdir=%s/lib64" % prefix,
                   "--disable-multilib",
                   "--enable-languages=" + ','.join(enabled_languages),
                   "--with-mpc=%s"    % spec['mpc'].prefix,
                   "--with-mpfr=%s"   % spec['mpfr'].prefix,
                   "--with-gmp=%s"    % spec['gmp'].prefix,
                   "--with-stage1-ldflags=%s" % self.rpath_args,
                   "--with-boot-ldflags=%s"   % self.rpath_args,
                   "--enable-lto",
                   "--with-quad"]
        # Libelf
        if '+libelf' in spec:
            libelf_options = ["--with-libelf=%s" % spec['libelf'].prefix]
            options.extend(libelf_options)

        # Binutils
        if '+binutils' in spec:
            binutils_options = ["--with-ld=%s/bin/ld" % spec['binutils'].prefix,
                                "--with-as=%s/bin/as" % spec['binutils'].prefix,
                                "--with-gnu-ld",
                                "--with-gnu-as"]
            options.extend(binutils_options)
            
        # Isl
        if spec.satisfies('@5.0:+isl'):
            isl_options = ["--with-isl=%s" % spec['isl'].prefix]
            options.extend(isl_options)

        # Rest of install is straightforward.
        configure(*options)
        make()
        make("install")

        self.write_rpath_specs()


    @property
    def spec_dir(self):
        # e.g. lib64/gcc/x86_64-unknown-linux-gnu/4.9.2
        spec_dir = glob("%s/lib64/gcc/*/*" % self.prefix)
        return spec_dir[0] if spec_dir else None


    def write_rpath_specs(self):
        """Generate a spec file so the linker adds a rpath to the libs
           the compiler used to build the executable."""
        if not self.spec_dir:
            tty.warn("Could not install specs for %s." % self.spec.format('$_$@'))
            return

        gcc = Executable(join_path(self.prefix.bin, 'gcc'))
        lines = gcc('-dumpspecs', return_output=True).split("\n")
        for i, line in enumerate(lines):
            if line.startswith("*link:"):
                specs_file = join_path(self.spec_dir, 'specs')
                with closing(open(specs_file, 'w')) as out:
                    out.write(lines[i] + "\n")
                    out.write("-rpath %s/lib:%s/lib64 \\\n"
                                % (self.prefix, self.prefix))
                    out.write(lines[i+1] + "\n")
                set_install_permissions(specs_file)
