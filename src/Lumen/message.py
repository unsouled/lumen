from twisted.internet import reactor, defer
from json import JSONEncoder, JSONDecoder
import channel

class Request():
    def __init__(self, attributes):
        self.attributes = attributes
        self.attributes['version'] = '1.0'
        self.attributes['minimumVersion'] ='1.0beta'

    def process(self):
        ch = channel.get(self.attributes['channel'])
        return ch.publish(self)

class Message():
    def __init__(self, httpRequest):
        content = httpRequest.content.read()
        self.httpRequest = httpRequest
        self.content = JSONDecoder().decode(content)

        self.content.reverse() # FIXME: work around!

        print self.content
        self.requests = [ Request(data) for data in self.content]

    def respond(self, results):
        responses = []

        for result in results:
            status, ret = result
            responses += ret

        self.httpRequest.write(JSONEncoder().encode(responses))
        self.httpRequest.finish()

    def process(self):
        responses = [ req.process() for req in self.requests ]
        self.responses = defer.DeferredList(responses)
        self.responses.addCallback(self.respond)
