from twisted.internet import reactor, defer
from json import JSONDecoder, JSONEncoder
import channel
import client
from transport import TransportFactory

class Request():
    def __init__(self, attributes):
        self.attributes = attributes
        self.attributes['version'] = '1.0'
        self.attributes['minimumVersion'] ='1.0beta'

    def process(self):
        if not self.attributes['channel'].startswith('/meta/'):
            reactor.callLater(0.01, self._doPublish)

        return channel.get(self.attributes['channel']).publish(self)

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

class Message():
    def __init__(self, httpRequest):
        self.transport = TransportFactory.create(httpRequest)
        self.httpRequest = httpRequest
        self.content = JSONDecoder().decode(self.transport.read())
        self.requests = [Request(data) for data in self.content]

    def process(self):
        responses = defer.DeferredList([request.process() for request in self.requests])
        responses.addCallback(self.response)
        return responses

    def response(self, responses):
        data = []
        for response in responses:
            status, r = response
            data += r
        self.transport.write(data)
