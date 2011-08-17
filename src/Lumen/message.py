from twisted.internet import reactor, defer
from json import JSONEncoder, JSONDecoder
import channel

class Request():
    def __init__(self, attributes):
        self.attributes = attributes
        self.attributes['version'] = '1.0'
        self.attributes['minimumVersion'] ='1.0beta'

    def process(self):
        if self.attributes['channel'].startswith('/meta/'):
            ch = channel.get(self.attributes['channel'])
            ret = ch.publish(self)
        else:
            chs = channel.expand(self.attributes['channel'])
            for ch in chs:
                ret = channel.get(ch).publish(self)
        ret['channel'] = self.attributes['channel']
        return ret

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
