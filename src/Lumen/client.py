from twisted.internet import reactor
from json import JSONEncoder
import uuid
import channel

clients = {}

class Client():
    def __init__(self, clientId):
        self.id = clientId
        self.responses = []
        self.receivedMessages = []
        self.connectRequest = None
        self.channelsSubscribing = set()

    def handleMessage(self, msg):
        reactor.callLater(0.01, self._doHandleMessage, msg)

    def _doHandleMessage(self, msg):
        responses = msg.handle(self)
        chs = [response['channel'] for response in responses]

        if '/meta/disconnect' in chs and self.connectRequest:
            self.responses.extend(self.receivedMessages)
            self.connectRequest.write(JSONEncoder().encode(self.responses))
            self.connectRequest.finish()
        elif '/meta/connect' not in chs:
            msg.httpRequest.write(JSONEncoder().encode(responses))
            msg.httpRequest.finish()
        else:
            self.connectRequest = msg.httpRequest
            self.connectRequest.notifyFinish().addErrback(self.__connectionLost)
            self.responses = responses
            self.publish([])

    def __connectionLost(self, reason):
        print reason
        self.connectRequest = None
        self.responses = []

    def publish(self, msg):
        self.receivedMessages.extend(msg)
        if self.receivedMessages and self.connectRequest:
            self.responses.extend(self.receivedMessages)
            self.connectRequest.write(JSONEncoder().encode(self.responses))
            self.connectRequest.finish()
            self.responses = []
            self.receivedMessages = []
            self.connectRequest = None

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
        msg.httpRequest.write(JSONEncoder().encode(responses))
        msg.httpRequest.finish()

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
    client.clients.pop(clientId)

class ClientFactory():
    @staticmethod
    def create(handshake):
        clientId = generateClientId()
        if 'apns' in handshake.attributes['supportedConnectionTypes']:
            deviceToken = handshake.attributes['deviceToken']
            c = IOSClient(clientId, deviceToken)
        else:
            c = Client(clientId)
        clients[clientId] = c
        return c
