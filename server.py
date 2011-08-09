from twisted.web import server, resource
from twisted.internet import reactor
from json import JSONEncoder, JSONDecoder
import uuid

class Message():
    def __init__(self, channel):
        self.channel = channel
        self.version = '1.0'
        self.minimumVersion ='1.0beta'

    @staticmethod
    def parse(content):
        data = JSONDecoder().decode(content)[0]

        channel = data['channel']

        if (channel == '/meta/handshake'):
            req = HandshakeRequest()
        elif (channel == '/meta/connect'):
            req = ConnectRequest(data['clientId'])

        return req

    def toJSON(self):
        return JSONEncoder().encode(self.toArray())

class Request(Message):
    def __init__(self, channel):
        Message.__init__(self, channel)

class Response(Message):
    def __init__(self, channel):
        Message.__init__(self, channel)

class HandshakeRequest(Request):
    def __init__(self):
        Request.__init__(self, '/meta/handshake')

    def toArray(self):
        return [
                {
                    "channel": self.channel,
                    "version": self.version,
                    "minimumVersion": self.minimumVersion,
                    "supportedConnectionTypes": self.supportedConnectionTypes
                    }
                ]

class ConnectRequest():
    def __init__(self, clientId):
        Request.__init__(self, '/meta/connect')
        self.clientId = clientId

    def toArray(self):
        return [
            {
                "channel": self.channel,
                "clientId": self.clientId,
                "connectionType": self.connectionType
                }
            ]

class HandshakeResponse(Response):
    def __init__(self):
        Response.__init__(self, '/meta/handshake')
        self.supportedConnectionTypes = ["long-polling","callback-polling"]
        self.clientId = self.generateClientId()
        self.successful = True
        self.authSuccessful = True
        self.advice = { 'reconnect': 'retry' }

    def generateClientId(self):
        return 'someGeneratedClientId'

    def toArray(self):
        return [
                {
                    "channel": self.channel,
                    "version": self.version,
                    "minimumVersion": self.minimumVersion,
                    "supportedConnectionTypes": self.supportedConnectionTypes,
                    "clientId": self.clientId,
                    "successful": self.successful,
                    "authSuccessful": self.authSuccessful,
                    "advice": self.advice
                    }
                ]

class ConnectResponse():
    def __init__(self, clientId):
        Response.__init__(self, '/meta/connect')
        self.successful = True
        self.error = ''
        self.clientId = clientId
        self.timestamp =  '12:00:00 1970'
        self.advice =  { "reconnect": "retry" }

    def toArray(self):
        return [
            {
                "channel": self.channel,
                "successful": self.successful,
                "error": self.error,
                "clientId": self.clientId,
                "timestamp": self.timestamp,
                "advice": self.advice
                }
            ]

class Handler():
    def __init__(self, request):
        self.request = request

    def process(self):
        if (self.request.channel == '/meta/handshake'):
            res = HandshakeResponse()
        elif (self.request.channel == '/meta/connect'):
            res = ConnectResponse(self.request.clientId)

        return res

class Lumen(resource.Resource):
    def render(self, request):
        print 'request received'
        content = request.content.read()
        req = Message.parse(content)
        res = Handler(req).process()
        print res.toJSON()
        return res.toJSON()

class Bayeux(resource.Resource):
    def __init__(self):
        resource.Resource.__init__ (self)
        self.putChild('lumen', Lumen())

    def render_GET(self, request):
        pass

lumen = server.Site(Bayeux())
reactor.listenTCP(8080, lumen)
reactor.run()
