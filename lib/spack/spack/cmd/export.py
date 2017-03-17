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
import collections
import os.path

import llnl.util.filesystem as fs
import llnl.util.tty as tty
import spack
import spack.cmd.common.arguments as arguments
import spack.tengine as tengine

description = "export installed specs in a valid 'packages.yaml'"


def setup_parser(subparser):
    subparser.add_argument(
        '--output_dir',
        default=os.path.join(spack.spack_root, 'exports'),
        help='output directory where the exported file will be saved'
    )
    subparser.add_argument(
        '--buildable',
        action='store_true',
        help='if False the exported packages will be marked as not buildable'
    )
    arguments.add_common_arguments(subparser, ['constraint'])


def export(parser, args):

    # Get the list of installed specs that match the query
    query_specs = args.specs()

    # Construct the absolute path for 'packages.yaml'
    basename = 'packages.yaml'
    dir = os.path.abspath(args.output_dir)

    if not os.path.exists(dir):
        fs.mkdirp(dir)

    abspath = os.path.join(dir, basename)

    # Check we are not accidentally overwriting an exported file
    if os.path.exists(abspath):
        msg = "File '{0}' already exists. Quitting.".format(abspath)
        tty.error(msg)

    # Construct the dictionary for template file substitution
    context = {
        'packages': collections.defaultdict(list),
        'buildable': args.buildable
    }
    p = context['packages']
    for s in query_specs:
        p[s.name].append(s)

    # Substitute the context in the template and get the corresponding text
    env = tengine.make_environment()
    template_file = os.path.join('commands', 'export_packages.yaml')
    template = env.get_template(template_file)
    text = template.render(context)

    with open(abspath, 'w') as f:
        f.write(text)
