import sys
from twisted.web import server
from twisted.internet import reactor
import bayeux

port = 8080

def main():
    lumen = server.Site(bayeux.Bayeux())
    reactor.listenTCP(port, lumen)
    reactor.run()

if __name__ == '__main__':
    sys.exit(main())
