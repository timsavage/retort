"""
Py27
~~~~

Even though Lambda only officially supports Python 2.7 this library is being developed Python 3.x first. This module
provides Python 2.7 fall-backs where possible.

This library assumes Python 2.7 if the version is less than 3.

"""
from __future__ import unicode_literals
import sys

__all__ = ('py2', 'range')

py2 = sys.version_info[0] < 3

if py2:
    range = xrange
