##############################################################################
# Copyright (c) 2013-2017, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
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
from distutils.dir_util import copy_tree


class Oommf(Package):
    """OOMMF is a project in the Applied and Computational Mathematics Division
       (ACMD) of ITL/NIST, in close cooperation with uMAG, aimed at developing 
       portable, extensible public domain programs and tools for micromagnetics.
       This code forms a completely functional micromagnetics package, with the
       additional capability to be extended by other programmers so that people
       developing new code can build on the OOMMF foundation. OOMMF is written 
       in C++, a widely-available, object-oriented language that can produce 
       programs with good performance as well as extensibility. For portable 
       user interfaces, we make use of Tcl/Tk so that OOMMF operates across 
       a wide range of Unix, Windows, and MacOSX platforms. The main 
       contributors to OOMMF are Mike Donahue, and Don Porter."""

    homepage = "http://math.nist.gov/oommf/"
    url      = "http://math.nist.gov/oommf/dist/oommf20a0_20170929.tar.gz"

    version('2.0a0_20170929', '4317ed01ee277b32d73e36a4fc151d8d')

    def install(self, spec, prefix):
        distclean = Executable("./oommf.tcl pimake distclean")
        distclean()
        upgrade = Executable("./oommf.tcl pimake upgrade")
        upgrade()
        pimake = Executable("./oommf.tcl pimake")
        pimake()
        mkdirp(prefix.bin)
        copy_tree(".", prefix.bin)

    def setup_environment(self, spack_env, run_env):
        run_env.prepend_path('PATH', self.spec.prefix)
