# -*- coding: utf-8 -*-
"""
Application
~~~~~~~~~~~

The main application entry point and dispatching interface.

Usage::

    >>> handler = Application()
    >>> # Register routes with application
    >>> @handler.route("/path/to/resource")
    >>> def list_resource(request):
    ...     return None

With the above configuration Lambda is setup to execute `my_module.handler`.

"""
from __future__ import absolute_import, unicode_literals
from retort.wrappers import Request

DEFAULT_METHODS = ['GET']


class Application(object):
    """
    Main application object (emulates the Flask Application API).
    """

    def __init__(self):
        self.routes = {}

    def __call__(self, event, context):
        request = Request(**event)

        try:
            route = self.routes[request.path]
        except KeyError:
            return {
                'statusCode': 404,
                'body': 'Page not found'
            }

        response = route(request)
        return response.serialize()

    def route(self, path, methods=DEFAULT_METHODS):
        def wrapper(f):
            self.routes[path] = f
        return wrapper
