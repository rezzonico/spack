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


class Simpson(Package):
    """SIMPSON is a general-purpose software package for simulation
    virtually all kinds of solid-state NMR experiments."""
    homepage = "http://nmr.au.dk/software/simpson/"
    url      = "https://github.com/vosegaard/simpson/archive/master.zip"

    version('master', '2ca15dcb94db12d9bbe96ccfe016dd8b')

    depends_on("cmake@2.8.2:")  # build
    depends_on("gsl")
    depends_on("mpi")

    depends_on("tcl")
    depends_on("tk")
    depends_on("blas")
    depends_on("lapack")
    depends_on("nfft")
    depends_on("fftw")

    patch("cmake.patch")

    def install(self, spec, prefix):
        with working_dir('spack-build', create=True):
            cmake('..',
                  '-DTCL_LIBRARY:PATH={0}.{1}'.format(
                      join_path(spec['tcl'].prefix.lib,
                                'libtcl{0}'.format(
                                    spec['tcl'].version.up_to(2))),
                      dso_suffix),
                  '-DSIMPSON_MPI:BOOL=ON',
                  '-DSIMPSON_GSL:BOOL=ON',
                  *std_cmake_args
            )

            make()
            make('install')
