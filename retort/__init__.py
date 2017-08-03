# -*- coding: utf-8 -*-
"""
######
Retort
######

*"I'm not a Bottle or a Flask!"*

A web framework for building applications with AWS Lambda and API Gateway inspired by Flask and Bottle.

"""
from .app import ApiGatewayHandler
from .helpers import redirect
from .wrappers import Request, Response

# HTTP Constants
HTTP_GET = 'get'
HTTP_PUT = 'put'
HTTP_POST = 'post'
HTTP_DELETE = 'delete'
HTTP_OPTIONS = 'options'

__version__ = '0.1'
