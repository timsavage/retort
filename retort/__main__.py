# -*- coding: utf-8 -*-
"""
CLI
~~~

Retort contains a CLI for common functions

"""
from __future__ import absolute_import, unicode_literals

import argparse

import retort


def get_args(args=None):
    """
    Setup and parse command line arguments
    """
    parser = argparse.ArgumentParser('retort', version=retort.__version__)

    sub_parsers = parser.add_subparsers(dest='command')

    sub_parser = sub_parsers.add_parser('runserver')
    sub_parser.add_argument('HANDLER',
                            help='Module that contains your request handler.')
    sub_parser.add_argument('--host', dest='host',
                            help='Hostname to bind server to.')
    sub_parser.add_argument('--port', type=int, dest='port',
                            help='Port to bind server to.')
    sub_parser.add_argument('--noreload', action='store_true', dest='no_reload',
                            help='Disable automatic reloading.')
    sub_parser.add_argument('--debug', action='store_true', dest='debug',
                            help='Enable debugging.')

    return parser.parse_args(args)


def run_server(args):
    import retort.server
    retort.server.run_server(args.HANDLER, args.host, args.port, args.no_reload, args.debug)


def main(args=None):
    args = get_args(args)

    # Execute command
    {
        'runserver': run_server
    }[args.command](args)


if __name__ == '__main__':
    main()
