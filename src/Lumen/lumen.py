import sys
from twisted.web import server
from twisted.internet import reactor
import bayeux
import config

conf = config.getConfig()
port = int(conf.get('default', 'port'))

def main():
    lumen = server.Site(bayeux.Bayeux())
    reactor.listenTCP(port, lumen)
    reactor.run()

if __name__ == '__main__':
    sys.exit(main())
