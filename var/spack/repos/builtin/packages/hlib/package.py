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

class Hlib(Package):
    """HLib is a program library for hierarchical matrices and H2-matrices."""
    homepage = "http://www.hlib.org/"
    url      = "http://fake-url-here-add-it-to-mirror/HLib-1.3p19.tar.gz"

    version('1.3p19', 'f59741a4a56dccbe91f6c38cdfb6f66b')

    variant('netcdf', default=False, description="Enable NetCDF support")
    variant('gtk',    default=False, description="Enable GTK support")

    depends_on('blas')
    depends_on('lapack')
    depends_on('netcdf', when='+netcdf')
    depends_on('gtk',    when='+gtk')
    
    def install(self, spec, prefix):
        configure_args = [
            '--enable-examples',
            '--enable-optimize',
            "--with-blas-ldflags=%s" % self.spec['blas'].blas_ld_flags,
            'LDFLAGS=-lm',
        ]

        if not '+gtk' in spec:
	    configure_args.append('--disable-gtktest')

        configure('--prefix=%s' % prefix, *configure_args)

        make()
        make("install")
