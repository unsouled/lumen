import sys
from twisted.web import server
from twisted.internet import reactor
import bayeux

def main():
    lumen = server.Site(bayeux.Bayeux())
    reactor.listenTCP(8080, lumen)
    reactor.run()

if __name__ == '__main__':
    sys.exit(main())
