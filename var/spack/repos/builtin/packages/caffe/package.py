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
#
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
#
#     spack install caffe
#
# You can edit this file again by typing:
#
#     spack edit caffe
#
# See the Spack documentation for more information on packaging.
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
from spack import *


class Caffe(Package):
    """Caffe is a deep learning framework made with expression, speed, and modularity in mind. It is developed by the Berkeley Vision and Learning Center (BVLC) and by community contributors. Yangqing Jia created the project during his PhD at UC Berkeley. Caffe is released under the BSD 2-Clause license."""

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "http://caffe.berkeleyvision.org/"
    url      = "https://github.com/BVLC/caffe/archive/rc3.tar.gz"

    version('3', '84e39223115753b48312a8bf48c31f59')
    version('2', 'c331932e34b5e2f5022fcc34c419080f')

    # FIXME: Add additional dependencies if required.
    depends_on('cmake')
    depends_on('lmdb')
    depends_on('leveldb')
    #depends_on('python')
    extends('python')
    depends_on('opencv')
    depends_on('gflags')
    depends_on('glog')
    depends_on('protobuf')
    depends_on('boost+python')
    depends_on('hdf5')
    depends_on('openblas')
    #depends_on('gcc')
    depends_on('py-setuptools')
    depends_on('py-pytest')

    def install(self, spec, prefix):
        with working_dir('spack-build', create=True):
            cmake_args = []
            cmake_args.append("-DCMAKE_INSTALL_PREFIX=%s" % prefix)
            cmake_args.append("-DCPU_ONLY=on")
            cmake_args.append("-DGLOG_INCLUDE_DIR=%s" % spec['glog'].prefix.include)
            cmake_args.append("-DGFLAGS_INCLUDE_DIR=%s" % spec['gflags'].prefix.include)
            cmake_args.append("-DLMDB_INCLUDE_DIR=%s" % spec['lmdb'].prefix.include)
            cmake_args.append("-DPROTOBUF_INCLUDE_DIR=%s" % spec['protobuf'].prefix.include)
            #cmake_args.append("-DPYTHON_INCLUDE_DIR=%s" % spec['python'].prefix.include)
            cmake_args.append("-DBoost_DIR=%s" % spec['boost'].prefix)
            cmake_args.append("-DHDF5_DIR=%s" % spec['hdf5'].prefix)
            cmake_args.append("-DBLAS=open" )
            cmake_args.append("-DCMAKE_CXX_COMPILER=g++")
            cmake_args.append("-DCMAKE_C_COMPILER=gcc")

            cmake('..', *cmake_args)

            make()
            make("install")

