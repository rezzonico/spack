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
import os
import shutil
import sys
import collections
import argparse

import llnl.util.tty as tty
import spack.cmd
from llnl.util.filesystem import mkdirp
from spack.modules import module_types
from spack.util.string import *

from spack.cmd.uninstall import ask_for_confirmation

description = "Manipulate module files"


# Qualifiers to be used when querying the db for specs
constraint_qualifiers = {
    'refresh': {
        'installed': True,
        'known': True
    },
    'find': {
    },
    'load-list':{
    },
    'rm': {
    }
}


class ConstraintAction(argparse.Action):
    qualifiers = {}

    def __call__(self, parser, namespace, values, option_string=None):
        # Query specs from command line
        d = self.qualifiers.get(namespace.subparser_name, {})
        specs = [s for s in spack.installed_db.query(**d)]
        values = ' '.join(values)
        if values:
            specs = [x for x in specs if x.satisfies(values, strict=True)]
        namespace.specs = specs

# TODO : this needs better wrapping to be extracted
ConstraintAction.qualifiers.update(constraint_qualifiers)


def _add_common_arguments(subparser):
    type_help = 'Type of module files'
    subparser.add_argument('-m', '--module-type', help=type_help, default='tcl', choices=module_types)
    constraint_help = 'Optional constraint to select a subset of installed packages'
    subparser.add_argument('constraint', nargs='*', help=constraint_help, action=ConstraintAction)


def setup_parser(subparser):
    sp = subparser.add_subparsers(metavar='SUBCOMMAND', dest='subparser_name')
    # spack module refresh
    refresh_parser = sp.add_parser('refresh', help='Regenerate all module files.')
    refresh_parser.add_argument('--delete-tree', help='Delete the module file tree before refresh', action='store_true')
    _add_common_arguments(refresh_parser)
    refresh_parser.add_argument(
        '-y', '--yes-to-all', action='store_true', dest='yes_to_all',
        help='Assume "yes" is the answer to every confirmation asked to the user.'
    )

    # spack module find
    find_parser = sp.add_parser('find', help='Find module files for packages.')
    _add_common_arguments(find_parser)

    # spack module rm
    rm_parser = sp.add_parser('rm', help='Find module files for packages.')
    _add_common_arguments(rm_parser)
    rm_parser.add_argument(
        '-y', '--yes-to-all', action='store_true', dest='yes_to_all',
        help='Assume "yes" is the answer to every confirmation asked to the user.'
    )


class MultipleMatches(Exception):
    pass


class NoMatch(Exception):
    pass


def find(mtype, specs, args):
    """
    Look at all installed packages and see if the spec provided
    matches any.  If it does, check whether there is a module file
    of type <mtype> there, and print out the name that the user
    should type to use that package's module.
    """
    if len(specs) == 0:
        raise NoMatch()

    if len(specs) > 1:
        raise MultipleMatches()

    mod = module_types[mtype](specs.pop())
    if not os.path.isfile(mod.file_name):
        tty.die("No %s module is installed for %s" % (mtype, spec))

    print(mod.use_name)


def rm(mtype, specs, args):
    module_cls = module_types[mtype]
    modules = [module_cls(spec) for spec in specs if os.path.exists(module_cls(spec).file_name)]

    if not modules:
        tty.msg('No module file matches your query')
        return

    # Ask for confirmation
    if not args.yes_to_all:
        tty.msg('You are about to remove the following module files:\n')
        for s in modules:
            print(s.file_name)
        print('')
        ask_for_confirmation('Do you want to proceed ? ')

    # Remove the module files
    for s in modules:
        s.remove()


def refresh(mtype, specs, args):
    """
    Regenerate all module files for installed packages known to
    spack (some packages may no longer exist).
    """
    # Prompt a message to the user about what is going to change
    if not specs:
        tty.msg('No package matches your query')
        return

    if not args.yes_to_all:
        tty.msg('You are about to regenerate the {name} module files for the following specs:\n'.format(name=mtype))
        for s in specs:
            print(s.format(color=True))
        print('')
        ask_for_confirmation('Do you want to proceed ? ')

    cls = module_types[mtype]

    # Detect name clashes
    writers = [cls(spec) for spec in specs]
    file2writer = collections.defaultdict(list)
    for item in writers:
        file2writer[item.file_name].append(item)

    if len(file2writer) != len(writers):
        message = 'Name clashes detected in module files:\n'
        for filename, writer_list in file2writer.items():
            if len(writer_list) > 1:
                message += '\nfile : {0}\n'.format(filename)
                for x in writer_list:
                    message += 'spec : {0}\n'.format(x.spec.format(color=True))
        tty.error(message)
        tty.error('Operation aborted')
        raise SystemExit(1)

    # Proceed regenerating module files
    tty.msg('Regenerating {name} module files'.format(name=mtype))
    if os.path.isdir(cls.path) and args.delete_tree:
        shutil.rmtree(cls.path, ignore_errors=False)
    mkdirp(cls.path)
    for x in writers:
        x.write(overwrite=True)

# Dictionary of callbacks based on the value of subparser_name
callbacks = {
    'refresh': refresh,
    'find': find,
    'rm': rm
}


def module(parser, args):
    module_type = args.module_type
    constraint = args.constraint
    try:
        callbacks[args.subparser_name](module_type, args.specs, args)
    except MultipleMatches:
        message = 'the constraint \'{query}\' matches multiple packages, and this is not allowed in this context'
        tty.error(message.format(query=constraint))
        for s in args.specs:
            sys.stderr.write(s.format(color=True) + '\n')
        raise SystemExit(1)
    except NoMatch:
        message = 'the constraint \'{query}\' match no package, and this is not allowed in this context'
        tty.die(message.format(query=constraint))
