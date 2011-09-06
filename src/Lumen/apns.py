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
    def buildProtocol(self, addr):
        print "Connected to APNS Server %s:%u" % (addr.host, addr.port)
        return APNSProtocol()

    def clientConnectionLost(self, connector, reason):
        print "Lost connection. Reason: %s" % reason

    def clientConnectionFailed(self, connector, reason):
        print "Connection failed. Reason: %s" % reason

class APNSProtocol(Protocol):
    def connectionMade(self):
        deviceToken = self.factory.deviceToken.decode('hex')
        payload = self.factory.payload
        self.sendMessage(deviceToken, payload)

    def sendMessage(self, deviceToken, payload):
        fmt = "!cH32sH%ds" % len(payload)
        command = '\x00'
        msg = struct.pack(fmt, command, len(deviceToken), deviceToken, len(payload), payload)
        self.transport.write(msg)

def push(deviceToken, payload, cetFile, privFile):
    reactor.connectSSL(APNS_SERVER_HOSTNAME,
            APNS_SERVER_PORT,
            APNSClientFactory(deviceToken, payload),
            APNSClientContextFactory(certFile, privFile))
