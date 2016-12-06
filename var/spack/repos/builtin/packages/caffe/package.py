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


class Caffe(Package):
    """Caffe is a deep learning framework made with expression, speed, and modularity in mind. It is developed by the Berkeley Vision and Learning Center (BVLC) and by community contributors. Yangqing Jia created the project during his PhD at UC Berkeley. Caffe is released under the BSD 2-Clause license."""

    homepage = "http://caffe.berkeleyvision.org/"

    version('rc3', '84e39223115753b48312a8bf48c31f59',url="https://github.com/BVLC/caffe/archive/rc3.tar.gz")
    version('rc2', 'c331932e34b5e2f5022fcc34c419080f',url="https://github.com/BVLC/caffe/archive/rc2.tar.gz")

    variant('cuda', default=False, description='Compile with CUDA Toolkit')
    depends_on('cmake')
    depends_on('lmdb')
    depends_on('leveldb')
    extends('python')
    depends_on('opencv')
    depends_on('gflags')
    depends_on('glog')
    depends_on('protobuf')
    depends_on('boost+python')
    depends_on('hdf5')
    depends_on('blas')
    depends_on('lapack')
    depends_on('py-setuptools')
    depends_on('py-pytest')
    depends_on('cuda@7.5.18', when='+cuda')
    depends_on('cudnn@7.0', when='+cuda')

    def install(self, spec, prefix):
        with working_dir('spack-build', create=True):
            cmake_args = []
            cmake_args.append("-DCMAKE_INSTALL_PREFIX=%s" % prefix)
            cmake_args.append("-DGLOG_INCLUDE_DIR=%s" % spec['glog'].prefix.include)
            cmake_args.append("-DGFLAGS_INCLUDE_DIR=%s" % spec['gflags'].prefix.include)
            cmake_args.append("-DLMDB_INCLUDE_DIR=%s" % spec['lmdb'].prefix.include)
            cmake_args.append("-DPROTOBUF_INCLUDE_DIR=%s" % spec['protobuf'].prefix.include)
            cmake_args.append("-DBoost_DIR=%s" % spec['boost'].prefix)
            cmake_args.append("-DHDF5_DIR=%s" % spec['hdf5'].prefix)
            if 'mkl' in spec:
              cmake_args.append("-DBLAS=mkl")
            elif 'openblas' in spec:
              cmake_args.append("-DBLAS=open")
            elif 'atlas' in spec:
              cmake_args.append("-DBLAS=atlas")
            else:
              raise AssertionError("Possible lapack options: openblas, atlas, mkl")
              
            cmake_args.append("-DCMAKE_CXX_COMPILER=%s" % spack_cxx)
            cmake_args.append("-DCMAKE_C_COMPILER=%s"% spack_cc)
            if '+cuda' in spec:
              cmake_args.append("-DCUDA_TOOLKIT_ROOT_DIR=%s"%spec['cuda'].prefix)
              cmake_args.append("-DCPU_ONLY=off")
              cmake_args.append("-DCUDA_CUDA_LIBRARY=%s"%spec['cuda'].prefix.lib+'/libculibos.a')#join_path does not work
              cmake_args.append("-DCUDNN_LIBRARY=%s"%spec['cudnn'].prefix.lib+'/libcudnn.so')
              cmake_args.append("-DCUDNN_INCLUDE=%s"%spec['cudnn'].prefix.include)
            else: 
              cmake_args.append("-DCPU_ONLY=on")
               
            cmake('..', *cmake_args)
            make()
            make("install")

