from twisted.web import resource
import twisted.web.server
from message import MessageFactory
import dispatcher

class Bayeux(resource.Resource):
    class Server(resource.Resource):
        def __init__(self):
            resource.Resource.__init__(self)

        def render(self, httpRequest):
            print 'http request received'
            print httpRequest
            httpRequest.setHeader('content-type', 'text/json')

            msg = MessageFactory.create(httpRequest)
            dispatcher.dispatch(msg)

            return twisted.web.server.NOT_DONE_YET

    def __init__(self):
        resource.Resource.__init__ (self)
        self.putChild('lumen', Bayeux.Server())

    def render_GET(self, request):
        pass

