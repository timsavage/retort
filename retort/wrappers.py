# -*- coding: utf-8 -*-
"""
Wrappers
~~~~~~~~

Wrappers around the request and response context.

"""
from __future__ import absolute_import, unicode_literals
from ._compat import *


class BaseRequest(object):
    """
    Context object for a request event from an API Gateway configured as a Proxy.
    """
    def __init__(self, body=None, resource=None, requestContext=None, queryStringParameters=None, httpMethod=None,
                 pathParameters=None, headers=None, stageVariables=None, path=None, isBase64Encoded=None):
        self.body = body
        self.resource = resource
        self.context = requestContext
        self.query_params = queryStringParameters or {}
        self.method = httpMethod
        self.path_params = pathParameters or {}
        self.headers = headers
        self.stage_variables = stageVariables or {}
        self.path = path

        self.params = collections.ChainMap(stageVariables, pathParameters, queryStringParameters, headers)


class Request(BaseRequest):
    pass


# HACK: API Gateway only accepts a Hash Map of headers to set multiple cookies some workarounds
# are required, rolling through different upper-case patterns to generate "unique" values.
COOKIE_HEAP = (
    'set-cookie', 'Set-cookie', 'sEt-cookie', 'seT-cookie', 'set-Cookie', 'set-cOokie', 'set-coOkie',
    'set-cooKie', 'set-cookIe', 'set-cookiE', 'SEt-cookie', 'sET-cookie', 'seT-Cookie', 'set-COokie',
    'set-cOOkie', 'set-coOKie', 'set-cooKIe', 'set-cookIE', 'SET-cookie', 'sET-Cookie', 'seT-COokie',
    'set-COOkie', 'set-cOOKie', 'set-coOKIe', 'set-cooKIE', 'SET-Cookie', 'sET-COokie', 'seT-COOkie',
    'set-COOKie', 'set-cOOKIe', 'set-coOKIE',
)


class BaseResponse(object):
    """
    Generate a response for API Gateway proxy

    :param body: HTTP Body
    :param status: HTTP status code
    :param content_type: Content type
    :param headers: Dict of additional headers

    """
    status_code = 200
    default_mimetype = 'text/plain'

    def __init__(self, body='', status=None, content_type=None, headers=None):
        self.body = body
        if status is not None:
            self.status_code = status
        self.headers = headers or {}
        self.headers['Content-Type'] = content_type or self.default_mimetype
        self.cookies = cookies.SimpleCookie()

    def serialize(self):
        response_headers = self.headers.copy()

        # Generate set-cookie headers
        for header, c in zip(COOKIE_HEAP, self.cookies.values()):
            response_headers[header] = str(c.output(header=''))

        return {
            'statusCode': self.status_code,
            'headers': response_headers,
            'body': self.body,
        }

    def set_cookie(self, key, value='', max_age=None, expires=None, path='/',
                   domain=None, secure=False, httponly=False):
        self.cookies[key] = value
        if path is not None:
            self.cookies[key]['path'] = path
        if domain is not None:
            self.cookies[key]['domain'] = domain
        if secure:
            self.cookies[key]['secure'] = True
        if httponly:
            self.cookies[key]['httponly'] = True

        self.cookies[key] = value


class Response(BaseResponse):
    default_mimetype = 'text/html'
