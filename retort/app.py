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

import logging

from retort.wrappers import Request, Response

DEFAULT_METHODS = ['GET']

logger = logging.getLogger(__name__)


class Application(object):
    """
    Main application object (emulates the Flask Application API).
    """

    def __init__(self):
        self.routes = {}

        self._404_handler = self._default_404
        self._500_handler = None

    def __call__(self, event, context):
        # Parse the incoming event
        request = Request(**event)

        # Determine route function
        route = self.routes.get(request.path, self._404_handler)

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
    def _default_404(_):
        return Response(
            "Resource does not exist",
            status=404,
            content_type='text/plain'
        )

    def route(self, path, methods=DEFAULT_METHODS):
        """
        Decorator for registering a route.

        >>> handler = Application()
        >>> @handler.route('/path/to/resource')
        >>> def list_resource(request):
        ...     pass

        :param path: Route
        :param methods: HTTP Methods that this route accepts.

        """
        def wrapper(f):
            self.routes[path] = f
        return wrapper

    def register_404(self):
        """
        Register a 404 handler.

        >>> handler = Application()
        >>> @handler.register_404('/path/to/resource')
        >>> def handle_404(request):
        ...     return ""

        """
        def wrapper(f):
            self._404_handler = f
        return wrapper

    def register_500(self):
        """
        Register a 500 handler.

        >>> handler = Application()
        >>> @handler.register_500('/path/to/resource')
        >>> def handle_500(request, ex):
        ...     return ""

        """
        def wrapper(f):
            self._500_handler = f
        return wrapper
