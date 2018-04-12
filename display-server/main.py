#!/usr/bin/python
# coding: utf-8

"""
Try 'python weather.py -h' for usage information.
"""

import sys
import os
import locale
import argparse
import logging

from reader import Reader
from renderer import Renderer
from writer import Writer


DESCRIPTION = """
"""

EPILOG = """
"""


class ArgumentParser(argparse.ArgumentParser):
    """ ArgumentParser with human friendly help. """
    def print_help(self, file=None):
        """ Print human friendly help. """
        import humanfriendly.terminal
        humanfriendly.terminal.usage(self.format_help())


def main(args=None):
    """ Main: parse arguments and run. """

    parser = ArgumentParser(
        description=DESCRIPTION,
        epilog=EPILOG,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        '-v', '--verbose', action='store_const',
        dest='loglevel', const=logging.INFO, default=logging.WARN,
        help='enable log messages'
    )
    parser.add_argument(
        '-d', '--debug', action='store_const',
        dest='loglevel', const=logging.DEBUG, default=logging.WARN,
        help='enable debug messages'
    )
    parser.add_argument(
        '-q', '--quiet', action='store_true',
        help='do not print status messages'
    )

    parser.add_argument(
        'path', action='store',
        help='output path'
    )

    group_db = parser.add_argument_group(
        'datasource options', ''
    )
    group_db.add_argument(
        '--db', action='store', metavar='NAME', required=True,
        help='database name for influx db'
    )
    group_db.add_argument(
        '--dbhost', action='store', metavar='HOST', required=True,
        help='hostname for influx db'
    )
    group_db.add_argument(
        '--dbport', action='store', metavar='PORT', required=True,
        help='portnumber for influx db'
    )

    group_db = parser.add_argument_group(
        'output options', ''
    )
    group_db.add_argument(
        '--name', action='store', metavar='NAME', default='weather',
        help='output file name (defaults to "weather")'
    )
    group_db.add_argument(
        '-z', '--zipped', action='store_true', default=False,
        help='write zipped output'
    )

    arguments = parser.parse_args() if args is None else parser.parse_args(args)

    # logging
    import coloredlogs
    coloredlogs.install(
        level=arguments.loglevel,
        format='%(asctime)s - %(filename)s:%(funcName)s - %(levelname)s - %(message)s',
        isatty=True
    )

    # this is the beef

    data = Reader(arguments.db, arguments.dbhost, arguments.dbport).read()
    image = Renderer().render(data)
    Writer(arguments.path).write(image, name=arguments.name, zipped=arguments.zipped)

if __name__ == "__main__":
    locale.setlocale(locale.LC_TIME, 'de_DE.UTF-8')
    main()
