from twisted.internet import reactor
from json import JSONEncoder
import uuid
import channel
from datetime import datetime

clients = {}

class Client():
    def __init__(self, clientId):
        self.id = clientId
        self.responses = []
        self.receivedDatas = []
        self.connectMessage = None
        self.channelsSubscribing = set()
        self.typename = 'comet'
        self.createdAt = datetime.now()

    def __connectionLost(self, reason):
        print reason
        clients.remove(self.id)
        self.connectMessage = None
        self.responses = []

    def publish(self, data):
        self.receivedDatas.extend(data)
        if self.receivedDatas and self.connectMessage:
            self.responses.extend(self.receivedDatas)
            self.connectMessage.response(self.responses)
            self.responses = []
            self.receivedDatas = []
            self.connectMessage = None

    def subscribe(self, ch):
        channel.get(ch).subscribe(self)
        self.channelsSubscribing.add(ch)

    def unsubscribe(self, ch):
        channel.get(ch).unsubscribe(self)

    def disconnect(self):
        for ch in self.channelsSubscribing:
            channel.get(ch).unsubscribe(self)

class IOSClient(Client):
    def __init__(self, clientId, deviceToken):
        Client.__init__(self, clientId)
        self.deviceToken = deviceToken

    def _doHandleMessage(self, msg):
        responses = msg.handle(self)
        msg.response(responses)

        reactor.callLater(0.01, self.__connectToAPNSServer)

    def __connectToAPNSServer(self):
        pass

    def publish(self, msg):
        # using apns
        pass

def generateClientId():
    return uuid.uuid4().urn[9:]

def findById(clientId):
    return clients[clientId]

def remove(clientId):
    clients.pop(clientId)

class ClientFactory():
    @staticmethod
    def create(msg):
        #handshake = msg.requests[0]
        clientId = generateClientId()
        # FIXME
        #if 'apns' in handshake.attributes['supportedConnectionTypes']:
        #    deviceToken = handshake.attributes['deviceToken']
        #    c = IOSClient(clientId, deviceToken)
        #else:
        c = Client(clientId)
        clients[clientId] = c
        return c
