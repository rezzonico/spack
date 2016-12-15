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


class Php(AutotoolsPackage):
    """PHP interpreter"""

    homepage = "https://secure.php.net/"
    url      = "http://ch1.php.net/distributions/php-5.6.29.tar.bz2"

    version('5.6.29', 'b2772a0bdada0e20f4e1937f71416bcc')

    variant('extensions', default='curl,gd,zlib,iconv,pcntl,mbstring',
            values=('curl', 'gd', 'zlib', 'iconv', 'pcntl', 'mbstring'),
            exclusive=False,
            description='List of builtin extensions that should be activated')

    depends_on('curl', when='extensions=curl')
    depends_on('libgd', when='extensions=gd')
    depends_on('jpeg', when='extensions=gd')
    depends_on('libpng', when='extensions=gd')
    depends_on('libxpm', when='extensions=gd')
    depends_on('zlib', when='extensions=gd') # according to the doc
                                             # this is required when
                                             # libpng is used
    depends_on('zlib', when='extensions=zlib')
    depends_on('libiconv', when='extensions=iconv')


    def configure_args(self):
        args = [] #self.with_or_without('extensions')
        if 'extensions=curl' in self.spec:
            args.append('--with-curl={0}'.format(self.spec['curl'].prefix))

        if 'extensions=gd' in self.spec:
            args.append('--with-gd={0}'.format(self.spec['libgd'].prefix))
            args.append('--with-jpeg-dir={0}'.format(self.spec['jpeg'].prefix))
            args.append('--with-png-dir={0}'.format(self.spec['libpng'].prefix))
            args.append('--with-xpm-dir={0}'.format(self.spec['libxpm'].prefix))
            args.append('--with-zlib-dir={0}'.format(self.spec['zlib'].prefix))

        if 'extensions=zlib' in self.spec:
            args.append('--with-zlib={0}'.format(self.spec['zlib'].prefix))

        if 'extensions=iconv' in self.spec:
            args.append('--with-iconv-dir={0}'.format(self.spec['libiconv'].prefix))

        if 'extensions=pcntl' in self.spec:
            args.append('--enable-pcntl')

        if 'extensions=mbstring' in self.spec:
            args.append('--enable-mbstring')


        return args
