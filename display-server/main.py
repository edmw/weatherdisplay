#!/usr/bin/python
# coding: utf-8

"""
Create a Weather Display image.

Read data, render image and save to file.

Data will be read from Influx database.
Image will be written in either RGB565 raw or RGB565 raw zipped format.

Try '-h' for usage information.
"""


# 1st Party Modules
from reader import Reader
from renderer import Renderer
from writer import Writer

# 16. Generic Operating System Services
import argparse
import logging
import time
# 23. Internationalization
import locale


DESCRIPTION = """
Create a Weather Display image. Read data, render image and save to file.
"""

EPILOG = """
Data will be read from Influx database.
Image will be written in either RGB565 raw or RGB565 raw zipped format.
"""


class ArgumentParser(argparse.ArgumentParser):
    """ ArgumentParser with human friendly help. """
    def print_help(self, file=None):
        """ Print human friendly help. """
        import humanfriendly.terminal
        humanfriendly.terminal.usage(self.format_help())


def fileFormat(string):
    if not string.upper() in ['RAW565', 'RAW565Z']:
        raise argparse.ArgumentTypeError('Value has to be either "RAW565" or "RAW565Z"')
    return string


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

    group_output = parser.add_argument_group(
        'output options', ''
    )
    group_output.add_argument(
        '--name', action='store', metavar='NAME', default='weather',
        help='output file name (defaults to "weather")'
    )
    group_output.add_argument(
        '--format', action='store', metavar='FORMAT', default='RAW565', type=fileFormat,
        help='output file format (either "RAW565" or "RAW565Z", defaults to "RAW565")'
    )
    group_output.add_argument(
        '--png', action='store_true',
        help='output additional png image'
    )
    group_output.add_argument(
        '--timestamp', action='store_true',
        help='output timestamp file'
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

    data = Reader(
        arguments.db,
        arguments.dbhost,
        arguments.dbport
    ).read()

    image = Renderer().render(data)

    Writer(
        arguments.path
    ).write(
        image,
        file_name=arguments.name,
        file_format=arguments.format
    ).write(
        image if arguments.png else None,
        file_name=arguments.name,
        file_format="PNG"
    ).write_timestamp(
        time.time() if arguments.timestamp else None,
        file_name=arguments.name,
    )


if __name__ == "__main__":
    locale.setlocale(locale.LC_TIME, 'de_DE.UTF-8')
    main()
