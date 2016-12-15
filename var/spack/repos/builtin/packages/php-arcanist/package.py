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
import os


class PhpArcanist(Package):
    """Command line interface for Phabricator"""

    homepage = "https://github.com/phacility/arcanist"
    url      = "https://github.com/phacility/arcanist/archive/conduit-6.tar.gz"

    version('master', git='https://github.com/phacility/arcanist.git', branch='master', preferred=True)
    version('6', 'd537169cda0d5d8bfe24a5a688944b33')
    version('5', '8e22d9dee3464016cccb93cfb3f7f674')

    depends_on('php')
    depends_on('php-libphutil')

    def install(self, spec, prefix):
        for path in os.listdir('.'):
            if(os.path.isdir(path)):
                relpath = os.path.relpath(path)
                install_tree(path, join_path(prefix, relpath))

