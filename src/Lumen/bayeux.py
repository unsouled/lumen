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

<<<<<<< HEAD
class Bayeux(resource.Resource):
=======
            return twisted.web.server.NOT_DONE_YET

        def generateClientId(self):
            return uuid.uuid4().urn[9:]

>>>>>>> 9d09b22c2e06a352d114b09a3f1245f0af005307
    def __init__(self):
        resource.Resource.__init__ (self)
        self.putChild('lumen', Bayeux.Server())

    def render_GET(self, request):
        pass

