"""
Utils
~~~~~

Utility functions used to perform common operations.

"""
import base64
import os


def token(bit_depth: int=64, encoder=base64.b32encode) -> str:
    """
    Generate a random token of a certain bit depth and strip any padding.
    """
    # Fast divide by 8 ;)
    chars = bit_depth >> 3
    if bit_depth == chars << 3:
        data = os.urandom(chars)
        return encoder(data).decode().rstrip('=')
    raise ValueError("Bit depth must be a multiple of 8")
