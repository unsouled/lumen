from twisted.internet import reactor
from json import JSONEncoder
import uuid

clients = {}

class Client():
    def __init__(self, clientId):
        self.id = clientId
        self.responses = []
        self.received = []
        self.httpRequest = None

    def handleMessage(self, msg):
        reactor.callLater(0.01, self._doHandle, msg)

    def _doHandle(self, msg):
        responses = msg.handle()
        hasConnect = False
        for response in responses:
            response['clientId'] = self.id
            if response['channel'] == '/meta/connect':
                hasConnect = True

        if not hasConnect:
            httpRequest = msg.httpRequest
            httpRequest.write(JSONEncoder().encode(responses))
            httpRequest.finish()
        else:
            self.httpRequest = msg.httpRequest
            self.responses = responses
            self.publish([])

    def publish(self, msg):
        self.received.extend(msg)
        if self.received and self.httpRequest:
            self.responses.extend(self.received)
            self.httpRequest.write(JSONEncoder().encode(self.responses))
            self.httpRequest.finish()
            self.responses = []
            self.received = []
            self.httpRequest = None

def generateClientId():
    return uuid.uuid4().urn[9:]

def findByMessage(msg):
    try:
        clientId = msg.requests[0].attributes['clientId']
        c = clients[clientId]
    except:
        clientId = generateClientId()
        c = Client(clientId)
        clients[clientId] = c

    return c

def findById(clientId):
    return clients[clientId]
