##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
from spack import *
from distutils.dir_util import copy_tree


class Yambo(AutotoolsPackage):
    """Yambo is a FORTRAN/C code for Many-Body calculations in solid
    state and molecular physics.

    Yambo relies on the Kohn-Sham wavefunctions generated by two DFT
    public codes: abinit, and PWscf. The code was originally developed
    in the Condensed Matter Theoretical Group of the Physics Department
    at the University of Rome "Tor Vergata" by Andrea Marini. Previous
    to its release under the GPL license, yambo was known as SELF.
    """

    homepage = "http://www.yambo-code.org/index.php"
    url = "https://github.com/yambo-code/yambo/archive/4.1.3.tar.gz"

    version('4.1.3', 'fe488093f23f0c6c63605826791b1ea4')
    variant('openmp', default=False, description='Builds with OpenMP support')

    resource(
        name='iotk',
        url='https://github.com/yambo-code/yambo/files/783147/iotk-y1.2.1.tar.gz',
        destination='spack-resource-iotk',
        md5='61b52375f4ac0ae1526c399f77f4fef4',
        when='@4.1.3'
    )

    depends_on('mpi')
    depends_on('blas')
    depends_on('lapack')
    depends_on('scalapack')

    depends_on('netcdf~mpi')
    depends_on('netcdf-fortran')
    depends_on('hdf5~mpi')
    depends_on('libxc')
    depends_on('fftw')

    @run_before('configure')
    def filter_configure(self):
        string1 = 'cat config/report'
        string2 = 'cat ' + str(self.build_directory) + '/config/report'
        filter_file(string1, string2, 'configure')

    def configure_args(self):

        spec = self.spec

        scalapack_libs = spec['scalapack'].libs + spec['lapack'].libs

        args = ["--with-netcdf-includedir=%s" %
                spec['netcdf'].prefix.include,
                "--with-netcdf-libs=%s" % spec['netcdf'].libs,
                "--with-netcdff-includedir=%s" %
                spec['netcdf-fortran'].prefix.include,
                "--with-netcdff-libs=%s" % spec['netcdf-fortran'].libs,
                "--with-hdf5-includedir=%s" % spec['hdf5'].prefix.include,
                "--with-hdf5-libs=%s" % spec['hdf5'].libs,
                "--with-blas-libs=%s" % spec['blas'].libs,
                "--with-lapack-libs=%s" % spec['lapack'].libs,
                "--with-scalapack-libs=%s" % str(scalapack_libs),
                "--with-fft-libdir=%s" % spec['fftw'].prefix.lib,
                "--with-fft-includedir=%s" % spec['fftw'].prefix.include,
                "--with-libxc-includedir=%s" % spec['libxc'].prefix.include,
                "--with-libxc-libdir=%s" % spec['libxc'].prefix.lib]

        if '+openmp' in spec:
            args.append("--enable-open-mp")

        return args

    def install(self, spec, prefix):
        make('all', parallel=False)
        copy_tree('bin', prefix.bin)
        copy_tree('lib', prefix.lib)
