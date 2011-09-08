from twisted.internet import reactor
import uuid
import channel
from datetime import datetime
import apns

clients = {}

class Client():
    def __init__(self, clientId):
        self.id = clientId
        self.connection = None
        self.channelsSubscribing = set()
        self.typename = 'comet'
        self.createdAt = datetime.now()
        self.messages = []

    def publish(self, msg):
        self.messages.append(msg)
        self.response()

    def response(self):
        if self.connection and self.messages:
            d = self.connection[0]
            cmsg = self.connection[1]
            data = [{'id': cmsg.attributes['id'],
                     'channel': cmsg.attributes['channel'],
                     'successful': True,
                     'error': '',
                     'timestamp': '12:00:00 1970',
                     'advice': { 'reconnect': 'retry' } }]
            while self.messages:
                data.append(self.messages.pop(0).attributes)
            d.callback(data)
            self.connection = None

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
        self.typename = 'apns'
        self.deviceToken = deviceToken

    def _doHandleMessage(self, msg):
        responses = msg.handle(self)
        msg.response(responses)

        reactor.callLater(0.01, self.__connectToAPNSServer)

    def publish(self, msg):
#        apns.push(self.deviceToken, msg.attributes, cert, priv)
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
