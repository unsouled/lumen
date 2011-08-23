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
        reactor.callLater(0.01, self._doHandle, msg)

    def _doHandle(self, msg):
        responses = msg.handle(self)
        chs = [response['channel'] for response in responses]
        if '/meta/connect' not in chs:
            msg.httpRequest.write(JSONEncoder().encode(responses))
            msg.httpRequest.finish()
        else:
            self.connectRequest = msg.httpRequest
            self.responses = responses
            self.publish([])

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
        self.channelsSubscribing.add(ch)

    def unsubscribe(self, ch):
        pass

    def isSubscribing(self, ch):
        for pattern in self.channelsSubscribing:
            if pattern.endswith('/*') or pattern.endswith('/**'):
                if self.__patternMatched(h, pattern):
                    return True
            elif ch == pattern:
                return True

        return False

    def __patternMatched(self, ch, pattern):
        chp = '/' + '/'.join(ch.split('/')[1:-1])
        patternp = '/' + '/'.join(pattern.split('/')[1:-1])
        if pattern.endswith('/*'):
            return chp == patternp
        elif pattern.endswith('/**'):
            return ch.startswith(patternp)

def generateClientId():
    return uuid.uuid4().urn[9:]

def findById(clientId):
    return clients[clientId]
