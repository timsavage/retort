from retort.app import Application
from retort.wrappers import Response

handler = Application()


@handler.route('/hello/')
def hello_world(request):
    return Response("Hi", content_type='text/plain')
