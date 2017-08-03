# -*- coding: utf-8 -*-
"""
Helpers
~~~~~~~

A collection of helpers to simplify common web application patterns.

"""
from markupsafe import escape


def redirect(location, code=302, Response=None):
    """
    Return a redirection response object.

    :param location: The location to redirect to.
    :type location: str
    :param code: The status code to use (the default is 302)
    :type code: int
    :param Response: Response class to.
    :type Response: type
    :rtype: Response

    """
    if Response is None:
        from retort.wrappers import Response

    display_location = escape(location)
    response = Response(
        '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">\n'
        '<title>Redirecting...</title>\n'
        '<h1>Redirecting...</h1>\n'
        '<p>You should be redirected automatically to target URL: '
        '<a href="{}">{}</a>.  If not click the link.'.format(escape(location), display_location),
        code, content_type='text/html', headers={
            'Location': location
        }
    )
    return response
