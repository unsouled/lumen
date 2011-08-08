from twisted.web import server, resource
from twisted.internet import reactor
import bayeux

lumen = server.Site(bayeux.Bayeux())
reactor.listenTCP(8080, lumen)
reactor.run()
