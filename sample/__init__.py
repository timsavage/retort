from retort import ApiGatewayHandler, Response, HTTP_POST

handler = ApiGatewayHandler()


@handler.route('/hello/')
def hello_world(request):
    return Response("Hi", content_type='text/plain')


@handler.route('/hello/post/', [HTTP_POST])
def hello_post(request):
    return Response("Hi post.", content_type='text/plain')
