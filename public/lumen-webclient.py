from twisted.web import resource, static
from twisted.web import server
from twisted.internet import reactor

class WebClient(resource.Resource):
    def __init__(self):
        resource.Resource.__init__(self)
        self.putChild('public', static.File('.'))

if __name__ == '__main__':
    webclient = server.Site(WebClient())
    reactor.listenTCP(8080, webclient)
    reactor.run()
