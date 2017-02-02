# -*- coding: utf-8 -*-
"""
Application
~~~~~~~~~~~

The main application entry point and dispatching interface.

Usage::

    >>> handler = ApiGatewayHandler()
    >>> # Register routes with application
    >>> @handler.route("/path/to/resource")
    >>> def list_resource(request):
    ...     return None

With the above configuration Lambda is setup to execute `my_module.handler`.

"""
from __future__ import absolute_import, unicode_literals
from ._compat import *

import logging

from .wrappers import Request, Response

HTTP_GET = 'GET'
HTTP_PUT = 'PUT'
HTTP_HEAD = 'HEAD'
HTTP_POST = 'POST'
HTTP_PATCH = 'PATCH'
HTTP_DELETE = 'DELETE'
HTTP_OPTIONS = 'OPTIONS'

DEFAULT_METHODS = [HTTP_GET]

logger = logging.getLogger(__name__)


class ApiGatewayHandler(object):
    """
    API Gateway handler (emulates the Flask Application API).
    """

    def __init__(self, return_options=True):
        """
        Initialise py:class:`ApiGatewayHandler`.

        :param return_options: Specify if server should respond to OPTIONS method.

        """
        self.return_options = return_options

        self.routes = collections.defaultdict(dict)

        self._404_handler = self.handle_404
        self._405_handler = self.handle_405
        self._500_handler = None

    def __call__(self, event, context):
        return self.dispatch_event(event)

    def dispatch_event(self, event):
        """
        Dispatch an event from API Gateway.
        """
        # Parse the incoming event
        request = Request(**event)

        # Determine route handler
        route_methods = self.routes.get(request.path)
        if route_methods:
            route = route_methods.get(request.method, self._405_handler)
        else:
            route = self._404_handler

        # Execute route and handle response
        try:
            response = route(request)
        except Exception as ex:
            if self._500_handler:
                response = self._500_handler(request, ex)
            else:
                raise  # Send it up to Lambda to handle

        # If None is returned default to No Content
        if response is None:
            response = Response(status=204)

        return response.serialize()

    @staticmethod
    def handle_404(_):
        """
        Handle the 404 (Not found) status code.
        """
        return Response(
            "Not Found",
            status=404,
            content_type='text/plain'
        )

    def handle_405(self, request):
        """
        Handle the 405 (Method not allowed) status code.

        This could include returning options.

        """
        if self.return_options and request.method.upper() == HTTP_OPTIONS:
            return Response(
                headers={'Allow': 'OPTIONS, ' + ', '.join(self.routes.get(request.path, {}))}
            )
        else:
            return Response(
                "Method Not Allowed",
                status=405,
                content_type='text/plain'
            )

    def route(self, path, methods=DEFAULT_METHODS):
        """
        Decorator for registering a route.

        >>> handler = ApiGatewayHandler()
        >>> @handler.route('/path/to/resource')
        >>> def list_resource(request):
        ...     pass

        :param path: Route
        :param methods: HTTP Methods that this route accepts.

        """
        def wrapper(f):
            for method in methods:
                self.routes[path][method] = f
            return f
        return wrapper

    def register_404(self, func=None):
        """
        Register a 404 handler.

        >>> handler = ApiGatewayHandler()
        >>> @handler.register_404
        >>> def handle_404(request):
        ...     return ""

        """
        def wrapper(f):
            self._404_handler = f
            return f
        return wrapper(func) if func else wrapper

    def register_500(self, func=None):
        """
        Register a 500 handler.

        >>> handler = ApiGatewayHandler()
        >>> @handler.register_500
        >>> def handle_500(request, ex):
        ...     return ""

        """
        def wrapper(f):
            self._500_handler = f
            return f
        return wrapper(func) if func else wrapper

Application = ApiGatewayHandler
