from message import Message
from json import JSONDecoder

class Request(Message):
    def __init__(self, channel, httpRequest, data):
        Message.__init__(self, channel)
        self.httpRequest = httpRequest
        self.data = data
        self.id = data['id']

class HandshakeRequest(Request):
    def __init__(self, httpRequest, data):
        Request.__init__(self, '/meta/handshake', httpRequest, data)
        self.supportedConnectionTypes = self.data['supportedConnectionTypes']

    def toArray(self):
        return [{ "id": self.id,
                  "channel": self.channel,
                  "version": self.version,
                  "minimumVersion": self.minimumVersion,
                  "supportedConnectionTypes": self.supportedConnectionTypes }]

class ConnectRequest(Request):
    def __init__(self, httpRequest, data):
        Request.__init__(self, '/meta/connect', httpRequest, data)
        self.clientId = self.data['clientId']
        self.connectionType = 'long-polling'

    def toArray(self):
        return [{ "id": self.id,
                  "channel": self.channel,
                  "clientId": self.clientId,
                  "connectionType": self.connectionType }]

class DisconnectRequest(Request):
    def __init__(self, httpRequest, data):
        Request.__init__(self, '/meta/disconnect', httpRequest, data)

    def toArray(self):
        return [{ "channel": self.channel,
                  "clientId": self.clientId }]

class SubscribeRequest(Request):
    def __init__(self, httpRequest, data):
        Request.__init__(self, '/meta/subscribe', httpRequest, data)

    def toArray(self):
        return [{ "channel": self.channel,
                  "clientId": self.clientId,
                  "subscription": self.subscription }]

class UnsubscribeRequest(Request):
    def __init__(self, httpRequest, data):
        Request.__init__(self, '/meta/unsubscribe', httpRequest, data)

    def toArray(self):
        return [{ "channel": self.channel,
                  "clientId": self.clientId,
                  "subscription": self.subscription }]

class PublishRequest(Request):
    def __init__(self, channel, httpRequest, data):
        Request.__init__(self, channel, httpRequest, data)

    def toArray(self):
        return [{ "channel": self.channel,
                  "clientId": self.clientId }]

class RequestFactory():
    metaRequests = { '/meta/handshake': HandshakeRequest,
                     '/meta/connect': ConnectRequest,
                     '/meta/disconnect': DisconnectRequest,
                     '/meta/subscribe': SubscribeRequest, 
                     '/meta/unsubscribe': UnsubscribeRequest }

    @staticmethod
    def create(httpRequest):
        content = httpRequest.content.read()
        data = JSONDecoder().decode(content)[0]
        channel = data['channel']
        if RequestFactory.metaRequests.has_key (channel):
            return RequestFactory.metaRequests[channel](httpRequest, data)
        else:
            return PublishRequest(channel, httpRequest)
