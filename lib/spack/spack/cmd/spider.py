import argparse
import collections

import spack
import spack.modules
import llnl.util.tty as tty

description = 'Spider hierarchical modules and print which services should be loaded to get access to a module'  # NOQA: ignore=E501


def setup_parser(subparser):
    subparser.add_argument(
        'search_string',
        nargs=argparse.REMAINDER,
        help='string that matches the modules to be spidered')


def string_match(iterable, search_string):
    for item in iterable:
        if any(x in item.name for x in search_string):
            yield item


def print_spider_result(spec, required_services):
    print('')
    main_module = spack.modules.LmodModule(spec)
    tty.msg(main_module.use_name)
    for item in reversed(required_services):
        if item is not None:
            tty.msg('\t' + spack.modules.LmodModule(item).use_name)


def spider(parser, args):
    # Get the list of installed specs that match the query
    mathing_specs = []
    for spec in string_match(spack.installed_db.query(), args.search_string):
        mathing_specs.append(spec)

    # Construct a dictionary of services that are needed for each of the specs
    required_services = collections.defaultdict(list)
    for item in mathing_specs:
        for service in spack.modules.LmodModule.hierarchy_tokens:
            if service in item and item is not item[service]:
                required_services[item].append(item[service])
        try:
            compiler_query = item.compiler.name + '@' + str(
                item.compiler.version)
            compiler_spec = spack.installed_db.query_one(compiler_query)
            required_services[item].append(compiler_spec)
        except Exception:
            required_services[item]

    # Print the items in the dictionary
    print('The following modules match the query you have submitted:')
    for key, list_of_services in required_services.items():
        print_spider_result(key, list_of_services)
