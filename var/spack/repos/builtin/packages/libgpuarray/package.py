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

class Libgpuarray(Package):
    """Libgpuarray goal's is to make a common GPU ndarray(n dimensions array) that can be reused by all projects that is as future proof as possible, while keeping it easy to use for simple need/quick test."""
    homepage = "http://deeplearning.net/software/libgpuarray/"
    url      = "https://github.com/Theano/libgpuarray/archive/v0.6.0-rc2.tar.gz"

    version('0.6.0-rc2', '304963e8d3b01d48a34b0912d77fae3a')
    version('0.6.0-rc1', '23592d7a45f96226b4ab8691c53e0b2d')

    extends('python')
    depends_on('cuda')

    def install(self, spec, prefix):
        cmake('.', *std_cmake_args)

        make()
        make("install")
