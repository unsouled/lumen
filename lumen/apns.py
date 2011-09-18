import json
import struct
from OpenSSL import SSL
from twisted.internet import reactor
from twisted.internet.protocol import ClientFactory, Protocol
from twisted.internet.ssl import ClientContextFactory

APNS_SERVER_HOSTNAME = 'gateway.push.apple.com'
APNS_SERVER_PORT = 2195

class APNSClientContextFactory(ClientContextFactory):
    def __init__(self, certFile, privFile):
        self.ctx = SSL.Context(SSL.SSLv3_METHOD)
        self.ctx.use_certificate_file(certFile)
        self.ctx.use_privatekey_file(privFile)

    def getContext(self):
        return self.ctx

class APNSClientFactory(ClientFactory):
    def __init__(self, deviceToken, payload):
        ClientFactory.__init__(self)
        self.deviceToken = deviceToken
        self.payload = payload

    def buildProtocol(self, addr):
        print "Connected to APNS Server %s:%u" % (addr.host, addr.port)
        return APNSProtocol(self.deviceToken, self.payload)

    def clientConnectionLost(self, connector, reason):
        print "Lost connection. Reason: %s" % reason

    def clientConnectionFailed(self, connector, reason):
        print "Connection failed. Reason: %s" % reason

class APNSProtocol(Protocol):
    def __init__(self, deviceToken, payload):
        Protocol.__init__(self)
        self.deviceToken = deviceToken
        self.paylaod = payload

    def connectionMade(self):
        self.sendMessage(self.deviceToken.decode('hex'), self.payload)

    def sendMessage(self, deviceToken, payload):
        fmt = "!BH%dsH%ds" % (len(deviceToken), len(payload))
        command = 0
        msg = struct.pack(fmt, command, len(deviceToken), deviceToken, len(payload), payload)
        self.transport.write(msg)

def push(deviceToken, payload, certFile, privFile):
    payload = json.dumps({'aps': {'alert': payload}})
    reactor.connectSSL(APNS_SERVER_HOSTNAME,
            APNS_SERVER_PORT,
            APNSClientFactory(deviceToken, payload),
            APNSClientContextFactory(certFile, privFile))
