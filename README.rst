======
Retort
======

*"I'm not a Bottle or a Flask!"*

A web framework for building applications with AWS Lambda and API Gateway inspired by Flask and Bottle.

Basics!
=======

A quick example::

    >>> from retort import ApiGatewayHandler, Response

    >>> handler = ApiGatewayHandler

    >>> @handler.route('/hello/')
    >>> def hello_world(request):
    ...     return Response("Hello World")


For debugging use the builtin API Gateway/Lambda emulated server::

    python -m retort runserver my_example.handler

