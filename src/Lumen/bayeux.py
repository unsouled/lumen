from twisted.web import resource
from twisted.internet import reactor
import twisted.web.server

from request import RequestFactory
from responder import Responder

import message

class Bayeux(resource.Resource):
    class Server(resource.Resource):
        def __init__(self):
            resource.Resource.__init__(self)
            self.responders = {}

        def render(self, httpRequest):
            print 'http request received'
            print httpRequest
            httpRequest.setHeader('content-type', 'text/json')

            msg = message.Message(httpRequest)
            msg.process()

            return twisted.web.server.NOT_DONE_YET

    def __init__(self):
        resource.Resource.__init__ (self)
        self.putChild('lumen', Bayeux.Server())

    def render_GET(self, request):
        pass

