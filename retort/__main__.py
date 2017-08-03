# -*- coding: utf-8 -*-
"""
CLI
~~~

Retort contains a CLI for common functions

"""
from pyapp.app import CliApplication, add_argument

import retort


app = CliApplication(retort, "retort")


@app.command(cli_name='runserver')
@add_argument('HANDLER', help='Module that contains your request handler.')
@add_argument('--host', dest='host', help='Hostname to bind server to.')
@add_argument('--port', type=int, dest='port', help='Port to bind server to.')
@add_argument('--noreload', action='store_true', dest='no_reload', help='Disable automatic reloading.')
@add_argument('--debug', action='store_true', dest='debug', help='Enable debugging.')
def run_server(args):
    import retort.server
    retort.server.run_server(args.HANDLER, args.host, args.port, args.no_reload, args.debug)


if __name__ == '__main__':
    app.dispatch()
