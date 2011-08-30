from twisted.internet import reactor
from json import JSONDecoder, JSONEncoder
import channel
import client

class Request():
    def __init__(self, attributes):
        self.attributes = attributes
        self.attributes['version'] = '1.0'
        self.attributes['minimumVersion'] ='1.0beta'

    def process(self):
        if not self.attributes['channel'].startswith('/meta/'):
            reactor.callLater(0.01, self._doPublish)

        return channel.get(self.attributes['channel']).process(self)

    def _doPublish(self):
        data = [{ 'channel': self.attributes['channel'],
                  'data': self.attributes['data'],
                  'id': self.attributes['id'] }]

        subscribers = set()
        chs = channel.expand(self.attributes['channel'])
        for ch in chs:
            subscribers = subscribers.union(channel.get(ch).subscribers)
        for subscriber in subscribers:
            subscriber.publish(data)

class ClientMessage():
    def __init__(self, httpRequest, content):
        self.httpRequest = httpRequest
        self.content = JSONDecoder().decode(content)
        self.requests = [Request(data) for data in self.content]

    def handle(self, c):
        responses = []
        while self.requests:
            request = self.requests.pop(0)
            response = request.process()
            response['clientId'] = c.id
            responses.append (response)

        return responses

class LongPollingMessage(ClientMessage):
    def response(self, data):
        self.httpRequest.write(JSONEncoder().encode(data))
        self.httpRequest.finish()

class CallbackPollingMessage(ClientMessage):
    def __init__(self, httpRequest, content, callback):
        ClientMessage.__init__(self, httpRequest, content)
        self.callback = callback

    def response(self, data):
        data = '%s(%s)' % (self.callback, JSONEncoder().encode(data))
        self.httpRequest.write(data)
        self.httpRequest.finish()

class MessageFactory():
    @staticmethod
    def create(httpRequest):
        if httpRequest.method == 'POST':
            content = httpRequest.content.read()
            return LongPollingMessage(httpRequest, content)
        elif httpRequest.method == 'GET':
            content = httpRequest.args['message'][0]
            callback = httpRequest.args['jsonp'][0]
            return CallbackPollingMessage(httpRequest, content, callback)
