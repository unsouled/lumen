from twisted.internet.defer import Deferred
import response

class Responder():
    def __init__(self, clientId):
        self.clientId = clientId

    def addRequest(self, request):
        self.handler = Deferred()
        self.handler.addCallback(self.handleRequest)
        self.handler.callback(request)

    def handleRequest(self, request):
        if request.channel == '/meta/handshake':
            res = response.HandshakeResponse()
            res.clientId = self.clientId
            res.id = request.id
            request.httpRequest.write(res.toJSON())
            request.httpRequest.finish()
        elif request.channel == '/meta/connect':
            res = response.ConnectResponse(request.clientId)
            res.id = request.id
