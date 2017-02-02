# -*- coding: utf-8 -*-
"""
######
Retort
######

*"I'm not a Bottle or a Flask!"*

A web framework for building applications with AWS Lambda and API Gateway inspired by Flask and Bottle.

"""
from __future__ import absolute_import, unicode_literals

from .app import Application
from .helpers import redirect
from .wrappers import Request, Response

__version__ = '0.1'
