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
#     spack install orca
#
# You can edit this file again by typing:
#
#     spack edit orca
#
# See the Spack documentation for more information on packaging.
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
from spack import *


class Orca(Package):
    """An ab initio, DFT and semiempirical SCF-MO package

    ORCA is a flexible, efficient and  easy-to-use general purpose tool for
    quantum chemistry with specific emphasis on spectroscopic properties of
    open-shell molecules.  It features a wide  variety of  standard quantum
    chemical  methods ranging from  semiempirical methods to DFT to single-
    and  multireference correlated  ab initio  methods.  It can  also treat
    environmental and relativistic effects.

    Note:  ORCA  is a licensed  software.  The license  however is free for
    academic users."""

    homepage = "https://orcaforum.cec.mpg.de/"
    url      = "file:///fake/orca-4.0.0.tar.bz"

    version('4.0.0', '5265a28e5abda9fc8874aaacb323264b')

    depends_on('openmpi@2.0.2', when='@4.0.0')

    def install(self, spec, prefix):
        install_tree(
            self.stage.source_path,
            self.prefix.bin)
