import channel
import json
from twisted.web import http
from twisted.internet import defer
from transport import TransportFactory

import logging
from twisted.python import log

class Message():
    """
    Bayeux Message ( http://svn.cometd.com/trunk/bayeux/bayeux.html#toc_25 )
    """

    def __init__(self, attributes):
        self.attributes = attributes
        self.attributes['version'] = '1.0'
        self.attributes['minimumVersion'] ='1.0beta'

    def process(self):
        return channel.get(self.attributes['channel']).publish(self)

class Request(http.Request):
    """
    Bayeux Request

    This contains multiple Bayeux messages.
    """

    def __init__(self, channel, queued):
        http.Request.__init__(self, channel, queued)

    def response(self, responses):
        data = []
        for _, r in responses:
            data += r
        print self.transport
        self.bayeuxTransport.write(data)

    def process(self):
        self.bayeuxTransport = TransportFactory.create(self)
        content = json.loads(self.bayeuxTransport.read())
        self.messages = [Message(data) for data in content]

        responses = defer.DeferredList([message.process() for message in self.messages])
        responses.addCallback(self.response)

    def connectionLost(self, reason):
        log.msg(reason)

class Bayeux(http.HTTPChannel):
    """
    Bayeux Protocol ( http://svn.cometd.com/trunk/bayeux/bayeux.html )
    """

    requestFactory = Request

    def connectionMade(self):
        http.HTTPChannel.connectionMade(self)

    def lineReceived(self, line):
        http.HTTPChannel.lineReceived(self, line)

    def headerReceived(self, line):
        http.HTTPChannel.headerReceived(self, line)

    def requestDone(self, request):
        http.HTTPChannel.requestDone(self, request)

    def allContentReceived(self):
        http.HTTPChannel.allContentReceived(self)

    def rawDataReceived(self, data):
        http.HTTPChannel.rawDataReceived(self, data)

    def allHeadersReceived(self):
        http.HTTPChannel.allHeadersReceived(self)

    def timeoutConnection(self):
        http.HTTPChannel.timeoutConnection(self)

    def readConnectionLost(self):
        http.HTTPChannel.readConnectionLost(self)

    def writeConnectionLost(self):
        http.HTTPChannel.writeConnectionLost(self)

    def connectionLost(self, reason):
        http.HTTPChannel.connectionLost(self, reason)

class BayeuxServerFactory(http.HTTPFactory):
    protocol = Bayeux

