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
#     spack install bazel
#
# You can edit this file again by typing:
#
#     spack edit bazel
#
# See the Spack documentation for more information on packaging.
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
from spack import *
import subprocess, os
from subprocess import call
from shutil import copytree

class Bazel(Package):
    """Bazel is Google's own build tool, now publicly available in Beta. Bazel has built-in support for building both client and server software, including client applications for both Android and iOS platforms. It also provides an extensible framework that you can use to develop your own build rules. """
    # FIXME: add a proper url for your package's homepage here.
    homepage = "https://bazel.io/"
    url      = "https://github.com/bazelbuild/bazel/archive/0.3.1.tar.gz"

    version('0.3.1' , '5c959467484a7fc7dd2e5e4a1e8e866b')
    version('0.3.0' , '33a2cb457d28e1bee9282134769b9283')
    version('0.2.3' , '393a491d690e43caaba88005efe6da91')
    version('0.2.2b', '75081804f073cbd194da1a07b16cba5f')
    version('0.2.2' , '644bc4ea7f429d835e74f255dc1054e6')

    extends('python')
    depends_on('jdk')

    def install(self, spec, prefix):

       filename = join_path(self.stage.source_path, 'compile.sh')
       filename_cc = join_path(self.stage.source_path, 'tools/cpp/cc_configure.bzl')
       filter_file(r'cd', 'echo', filename)
       compiler = os.environ['SPACK_CC']
       filter_file(r'"gcc": cc','"gcc": "%s"'%compiler , filename_cc)

       

       Executable('./compile.sh')()

       outdir=os.getcwd()+'/output'
       libfiles = os.path.expanduser(outdir)
       copytree(libfiles, prefix.bin)

