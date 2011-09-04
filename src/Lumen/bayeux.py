from twisted.web import resource
import twisted.web.server
import dispatcher
import webconsole
import lumen
from message import Message

class Bayeux(resource.Resource):
    class Server(resource.Resource):
        def __init__(self):
            resource.Resource.__init__(self)

        def render(self, httpRequest):
            print 'http request received'
            httpRequest.setHeader('content-type', 'text/json')

            msg = Message(httpRequest)
            msg.process()

            return twisted.web.server.NOT_DONE_YET

    def __init__(self):
        resource.Resource.__init__ (self)
        self.putChild(lumen.config.get('default', 'endpoint'), Bayeux.Server())
        self.putChild(lumen.config.get('webconsole', 'endpoint'), webconsole.WebConsole())

    def render_GET(self, request):
        pass

