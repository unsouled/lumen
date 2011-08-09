from twisted.web import resource
from json import JSONEncoder, JSONDecoder
import uuid
import message
import request
import response

from json import JSONEncoder, JSONDecoder

class RequestParser():
    @staticmethod
    def parse(content):
        data = JSONDecoder().decode(content)[0]

        channel = data['channel']

        if (channel == '/meta/handshake'):
            req = request.HandshakeRequest()
            req.id = data['id']
            req.supportedConnectionTypes = data['supportedConnectionTypes']
        elif (channel == '/meta/connect'):
            req = request.ConnectRequest(data['clientId'])
        elif (channel == '/meta/disconnect'):
            req = request.DisconnectRequest()
        elif (channel == '/meta/subscribe'):
            req = request.SubscribeRequest()
        elif (channel == '/meta/unsubscribe'):
            req = request.UnsubscribeRequest()
        else:
            req = request.PublishRequest(channel)

        return req

class Handler():
    def __init__(self, request):
        self.request = request

    def process(self):
        if (self.request.channel == '/meta/handshake'):
            res = response.HandshakeResponse()
        elif (self.request.channel == '/meta/connect'):
            res = response.ConnectResponse(self.request.clientId)
        else:
            res = response.Response(self.request.channel)

        res.id = self.request.id

        if (hasattr(self.request, 'clientId')):
            res.clientId = self.request.clientId

        return res

class Lumen(resource.Resource):
    def render(self, request):
        content = request.content.read()
        req = RequestParser.parse(content)
        res = Handler(req).process()
        request.setHeader('Content-type', 'text/json')
        print " => " + req.toJSON()
        print " <= " + res.toJSON()
        return res.toJSON()

class Bayeux(resource.Resource):
    def __init__(self):
        resource.Resource.__init__ (self)
        self.putChild('lumen', Lumen())

    def render_GET(self, request):
        pass
