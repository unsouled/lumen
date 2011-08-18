from twisted.internet import reactor
from json import JSONDecoder
import channel

class Request():
    def __init__(self, attributes):
        self.attributes = attributes
        self.attributes['version'] = '1.0'
        self.attributes['minimumVersion'] ='1.0beta'

    def process(self):
        if not self.attributes['channel'].startswith('/meta/'):
            reactor.callLater(0.01, self._doPublish)

        return channel.get(self.attributes['channel']).handle(self)

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
        content = httpRequest.content.read()
        self.httpRequest = httpRequest
        self.content = JSONDecoder().decode(content)
        print self.content

        self.requests = [Request(data) for data in self.content]

    def handle(self):
        responses = []
        while self.requests:
            request = self.requests.pop(0)
            responses.append (request.process())

        return responses
