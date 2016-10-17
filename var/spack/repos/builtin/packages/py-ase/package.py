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


class PyAse(Package):
    """ASE is an Atomic Simulation Environment written in the Python
    programming language with the aim of setting up, steering, and analyzing
    atomistic simulations.
    """

    homepage = 'https://wiki.fysik.dtu.dk/ase'
    url = 'https://pypi.python.org/packages/fc/7b/558e7321f7a879c034ead5d10789b9d6f41beabaee0b156e807c19422ad0/ase-3.11.0.tar.gz'

    version('3.11.0', 'd7afe49d5beb1b1c38d60b1e3dd4e763')

    variant('scipy', default=True, description='Activate SciPy dependency')
    variant('matplotlib', default=True, description='Activate Matplotlib dependency')

    extends('python')
    depends_on('py-numpy')
    depends_on('py-scipy', when='+scipy')
    depends_on('py-matplotlib', when='+matplotlib')

    def install(self, spec, prefix):
        python('setup.py', 'install', '--prefix=%s' % prefix)
