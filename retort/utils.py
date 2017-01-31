"""
Utils
~~~~~

Utility functions used to perform common operations.

"""
from __future__ import absolute_import, unicode_literals
from .py2 import *
import random
import string

random = random.SystemRandom()

DEFAULT_STRING_POOL = string.ascii_letters + string.digits + "-_"


class RandomString(object):
    """
    Generate a random string
    """
    def __init__(self, string_pool=DEFAULT_STRING_POOL, length=16):
        self._string_pool = string_pool
        self.length = length

    def __call__(self, length=None):
        return ''.join(random.choice(self._string_pool) for _ in range(length or self.length))
