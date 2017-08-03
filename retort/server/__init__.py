# -*- coding: utf-8 -*-
"""
Server
~~~~~~

This is a builtin development server that simulates requests from API Gateway.

"""
import importlib

try:
    from werkzeug.serving import run_simple
    from werkzeug.wrappers import Request
except ImportError:
    raise ImportError("The werkzeug package is required to use the runserver command.")


STATUS_CODE_MESSAGES = {
    200: 'OK',
    201: 'Created',
    202: 'Accepted',
    203: 'Non-Authoritative Information',
    204: 'No Content',
    205: 'Reset Content',
    206: 'Partial Content',

    300: 'Multiple Choices',
    301: 'Moved Permanently',
    302: 'Found',
    303: 'See Other',
    304: 'Not Modified',
    305: 'Use Proxy',
    307: 'Temporary Redirect',
    308: 'Permanent Redirect',

    400: 'Bad Request',
    401: 'Unauthorized',
    402: 'Payment Required',
    403: 'Forbidden',
    404: 'Not Found',
    405: 'Method Not Allowed',
    406: 'Not Acceptable',
    407: 'Proxy Auth Required',
    408: 'Request Timeout',
    409: 'Conflict',
    410: 'Gone',
    411: 'Length Required',

    500: 'Internal Server Error',
    501: 'Not Implemented',
    502: 'Bad Gateway',
    503: 'Service Unavailable',
    504: 'Gateway Timeout',
}


def import_handler(handler):
    """
    Import handler and module.

    :param handler: String with fully qualified path to handler instance.
    :type handler: str
    :return: tuple of (handler_module, handler_instance)
    :rtype: tuple(module, retort.app.Application)

    """
    module_name, _, instance_name = handler.rpartition('.')
    module = importlib.import_module(module_name)
    return module, getattr(module, instance_name)


class RetortApplication(object):
    def __init__(self, handler, stage_variables=None):
        self.handler = handler
        self.stage_variables = stage_variables or {}

    def generate_event(self, environ):
        """
        Generate an API Gateway event from WSGI environ.
        """
        request = Request(environ)

        return {
            'body': request.data,
            'resource': request.path,
            'requestContext': None,
            'queryStringParameters': dict(i for i in request.args.items()),
            'httpMethod': request.method,
            'pathParameters': None,
            'headers': dict(i for i in request.headers.items() if i[0].isupper()),
            'stageVariables': self.stage_variables,
            'path': request.path,
            'isBase64Encoded': False,
        }

    def handle_exception(self, exception):
        pass

    def process_response(self, response, start_response):
        """
        Process response object into a WSGI response.

        :type response: retort.Response
        :param start_response:
        :return:
        """
        status_code = response['statusCode']
        status = "{} {}".format(status_code, STATUS_CODE_MESSAGES.get(status_code, 'UNKNOWN'))
        headers = [i for i in response['headers'].items()]

        body = response['body']
        if isinstance(body, str):
            body = body.encode('utf8')

        # Do WSGI response
        start_response(status, headers)
        return [body]

    def wsgi_app(self, environ, start_response):
        event = self.generate_event(environ)

        try:
            response = self.handler.dispatch_event(event)
        except Exception as e:
            response = self.handle_exception(e)
            if response is None:
                raise

        return self.process_response(response, start_response)

    def __call__(self, environ, start_response):
        """Shortcut for :attr:`wsgi_app`."""
        return self.wsgi_app(environ, start_response)


def run_server(handler, host=None, port=None, no_reload=False, use_debugger=False):
    """

    :param handler:
    :param host:
    :param port:
    :return:
    """
    handler_module, handler_instance = import_handler(handler)

    if host is None:
        host = '127.0.0.1'
    if port is None:
        port = 5000

    run_simple(host, port, RetortApplication(handler_instance),
               use_reloader=not no_reload, use_debugger=use_debugger)
