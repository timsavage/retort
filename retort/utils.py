"""
Utils
~~~~~

Utility functions used to perform common operations.

"""
from __future__ import absolute_import, unicode_literals
from ._compat import *

import string

# Replace random with System random (derived from urandom)
import random
random = random.SystemRandom()

DEFAULT_STRING_POOL = string.ascii_letters + string.digits + "-_"


class RandomString(object):
    """
    Generate a random string
    """
    def __init__(self, default_length=16, chars=DEFAULT_STRING_POOL):
        self.chars = chars
        self.length = default_length

    def __call__(self, length=None):
        return ''.join(random.choice(self.chars) for _ in range(length or self.length))

random_string = RandomString()
