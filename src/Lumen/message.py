from twisted.internet import reactor
from json import JSONDecoder
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

        ch = self.attributes['channel']
        subscribers = filter(lambda c: c.isSubscribing(ch), client.clients.values())
        for subscriber in subscribers:
            subscriber.publish(data)

class Message():
    def __init__(self, httpRequest):
        content = httpRequest.content.read()
        self.httpRequest = httpRequest
        self.content = JSONDecoder().decode(content)
        print self.content

        self.requests = [Request(data) for data in self.content]

    def handle(self, c):
        responses = []
        while self.requests:
            request = self.requests.pop(0)
            response = request.process()
            response['clientId'] = c.id
            responses.append (response)

        return responses
