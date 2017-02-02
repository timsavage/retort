from retort import ApiGatewayHandler, Response

handler = ApiGatewayHandler()


@handler.route('/hello/')
def hello_world(request):
    return Response("Hi", content_type='text/plain')
