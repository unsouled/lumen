from twisted.internet import reactor
import response
import uuid

class RequestHandler():
    def __init__(self, request):
        self.request = request
        self.clientId = self.request.clientId

    def _doHandle(self):
        pass

    def handle(self):
        self.response.clientId = self.clientId
        self.response.id = self.request.id

        self._doHandle()

    def _finish(self):
        self.request.httpRequest.write(self.response.toJSON())
        self.request.httpRequest.finish()

class HandshakeHandler(RequestHandler):
    def __init__(self, request):
        RequestHandler.__init__(self, request)
        self.response = response.HandshakeResponse()


    def _doHandle(self):
        print 'handle Handshake request.'
        self._finish()

class ConnectHandler(RequestHandler):
    def __init__(self, request):
        RequestHandler.__init__(self, request)
        self.response = response.ConnectResponse()

    def _doHandle(self):
        print 'handle Connect request.'

class DisconnectHandler(RequestHandler):
    def __init__(self, request):
        RequestHandler.__init__(self, request)
        self.response = response.DisconnectResponse()

    def _doHandle(self):
        print 'handle Disconnect request.'

class SubscribeHandler(RequestHandler):
    def __init__(self, request):
        RequestHandler.__init__(self, request)
        self.response = response.SubscribeResponse()

    def _doHandle(self):
        print 'handle Subscribe request.'

class UnsubscribeHandler(RequestHandler):
    def __init__(self, request):
        RequestHandler.__init__(self, request)
        self.response = response.UnsubscribeResponse()

    def _doHandle(self):
        print 'handle Unsubscribe request.'

class PublishHandler(RequestHandler):
    def __init__(self, request):
        RequestHandler.__init__(self, request)

    def _doHandle(self):
        print 'handle Publish request.'

class RequestHandlerFactory():
    metaHandlers = { '/meta/handshake': HandshakeHandler,
                     '/meta/connect': ConnectHandler,
                     '/meta/disconnect': DisconnectHandler,
                     '/meta/subscribe': SubscribeHandler,
                     '/meta/unsubscribe': UnsubscribeHandler }

    @staticmethod
    def create(request):
        channel = request.channel
        if RequestHandlerFactory.metaHandlers.has_key(channel):
            return RequestHandlerFactory.metaHandlers[channel](request)
        else:
            return PublishHandler(request)

class Responder():
    def __init__(self):
        self.clientId = self.__generateClientId()

    def __generateClientId(self):
        return uuid.uuid4().urn[9:]

    def addRequest(self, request):
        reactor.callLater(0.01, self.__handleRequest, request)

    def __handleRequest(self, request):
        if request.channel == '/meta/handshake':
            request.clientId = self.clientId
        RequestHandlerFactory.create(request).handle()
