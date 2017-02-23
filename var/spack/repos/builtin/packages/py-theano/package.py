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

class PyTheano(Package):
    """Theano is a Python library that allows you to define, optimize, and evaluate mathematical expressions involving multi-dimensional arrays efficiently."""
    homepage = "http://deeplearning.net/software/theano/"
    url      = "https://github.com/Theano/Theano/archive/rel-0.8.2.tar.gz"

    version('0.8.2', 'a15eb23bc9126d598cf9a5199316167a',pip='Theano',version='0.8.2')
    version('0.8.1', 'f101376043a171d7c007747d1b2640a3',pip='Theano',version='0.8.1')
    version('0.8.0', 'd9f5e9e4fb5610af64ad585e2a59955b',pip='Theano',version='0.8.0')
    version('0.7'  , 'ead841db54205aff182e022e0a1e2d91',pip='Theano',version='0.7')
    version('0.6'  , '338d864eae2084bf96aa6b05b5890332',pip='Theano',version='0.6')

    extends('python')
    depends_on('py-pip')
    depends_on('py-numpy')
    depends_on('py-scipy')
    depends_on('py-nose')
    depends_on('py-six')
    variant('cuda', default=False, description="Enable CUDA support")
    depends_on('cuda', when='+cuda')
    depends_on('libgpuarray',when='+cuda')
    depends_on('cudnn',when='+cuda')


    def install(self, spec, prefix):
        pip('install', *std_pip_args)
