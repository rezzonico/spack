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


class PyNumpy(Package):
    """NumPy is the fundamental package for scientific computing with Python.
    It contains among other things: a powerful N-dimensional array object,
    sophisticated (broadcasting) functions, tools for integrating C/C++ and
    Fortran code, and useful linear algebra, Fourier transform, and random
    number capabilities"""
    homepage = "http://www.numpy.org/"
    url      = "https://pypi.python.org/packages/source/n/numpy/numpy-1.9.1.tar.gz"

    version('1.11.0', 'bc56fb9fc2895aa4961802ffbdb31d0b')
    version('1.10.4', 'aed294de0aa1ac7bd3f9745f4f1968ad')
    version('1.9.2',  'a1ed53432dbcd256398898d35bc8e645')
    version('1.9.1',  '78842b73560ec378142665e712ae4ad9')

    variant('blas',   default=True)
    variant('lapack', default=True)

    extends('python')
    depends_on('py-nose')
    depends_on('py-setuptools')
    depends_on('blas',   when='+blas')
    depends_on('lapack', when='+lapack')

    def patch(self):
        # Modified acording to
        # https://software.intel.com/en-us/articles/numpyscipy-with-intel-mkl
        if self.compiler.name == 'intel':
            filter_file(
                r'-fomit-frame-pointer -openmp -xSSE4.2',
                r'-fomit-frame-pointer -{0}openmp -xHost'.format(
                    'q' if self.compiler.version >= Version('15.0.0') else ''),
                'numpy/distutils/intelccompiler.py')

            filter_file(r'-xSSE4.2', r'-xHost',
                        'numpy/distutils/fcompiler/intel.py')

            if self.compiler.version >= Version('15.0.0'):
                filter_file(r'-openmp',
                            r'-qopenmp',
                            'numpy/distutils/fcompiler/intel.py')

        with open('site.cfg', 'w') as f:        
            if 'openblas' in self.spec:
                f.write('[openblas]\n')
                f.write('libraries=openblas\n')
                f.write('library_dirs={0}\n'.format(
                    self.spec['openblas'].prefix.lib))
                f.write('include_dirs={0}\n'.format(
                    self.spec['openblas'].prefix.include))
                f.write('rpath={0}\n'.format(
                    self.spec['openblas'].prefix.lib))
            elif 'atlas' in self.spec:
                f.write('[atlas]\n')
                f.write('library_dirs={0}\n'.format(
                    self.spec['atlas'].prefix.lib))
                f.write('include_dirs={0}\n'.format(
                    self.spec['atlas'].prefix.include))
            elif 'mkl' in self.spec:
                f.write('[mkl]\n')
                f.write('library_dirs={0}\n'.format(
                    join_path(self.spec['mkl'].prefix.lib, 'intel64')))
                f.write('include_dirs={0}\n'.format(
                    self.spec['mkl'].prefix.include))
                f.write('rpath={0}\n'.format(
                    join_path(self.spec['mkl'].prefix.lib, 'intel64')))
                f.write('mkl_libs=mkl_rt\n')
                f.write('lapack_libs=\n')
            else:
                libraries    = []
                library_dirs = []

                if '+blas' in self.spec:
                    libraries.append('blas')
                    library_dirs.append(self.spec['blas'].prefix.lib)
                if '+lapack' in self.spec:
                    libraries.append('lapack')
                    library_dirs.append(self.spec['lapack'].prefix.lib)

                if libraries:
                    f.write('[DEFAULT]\n')
                    f.write('libraries={0}\n'.format(
                            ','.join(libraries)))
                    f.write('library_dirs={0}\n'.format(
                            ':'.join(library_dirs)))
                    f.write('rpath={0}\n'.format(
                            ':'.join(library_dirs)))

    def install(self, spec, prefix):
        compiler_opts = []
        if spec.compiler.name == 'intel':
            compiler_opts = ['--compiler=intelem', '--fcompiler=intelem']

        python('setup.py', 'config')
        python('setup.py', 'build', *compiler_opts)
        python('setup.py', 'install', '--prefix={0}'.format(prefix))
