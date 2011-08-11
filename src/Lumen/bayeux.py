from twisted.web import resource
from twisted.internet import reactor
import twisted.web.server
import uuid

from request import RequestFactory
from responder import Responder

class Lumen(resource.Resource):
    def __init__(self):
        resource.Resource.__init__(self)
        self.responders = {}

    def render(self, httpRequest):
        httpRequest.setHeader('Content-type', 'text/json')

        request = RequestFactory.create(httpRequest)
        if request.channel == '/meta/handshake':
            clientId = self.generateClientId()
            self.responders[clientId] = Responder(clientId)
        else:
            clientId = request.clientId
        self.responders[clientId].addRequest(request)

        return twisted.web.server.NOT_DONE_YET

    def generateClientId(self):
        return uuid.uuid4().urn[9:]

class Bayeux(resource.Resource):
    def __init__(self):
        resource.Resource.__init__ (self)
        self.putChild('lumen', Lumen())

    def render_GET(self, request):
        pass
