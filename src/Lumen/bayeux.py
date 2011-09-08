from twisted.web import resource
import twisted.web.server
import webconsole
import config
from message import Message

class Bayeux(resource.Resource):
    class Server(resource.Resource):
        def __init__(self):
            resource.Resource.__init__(self)

        def render(self, httpRequest):
            httpRequest.setHeader('content-type', 'text/json')

            msg = Message(httpRequest)
            msg.process()

            return twisted.web.server.NOT_DONE_YET

    def __init__(self):
        resource.Resource.__init__ (self)
        self.putChild(config.getConfig().get('default', 'endpoint'), Bayeux.Server())
        self.putChild(config.getConfig().get('webconsole', 'endpoint'), webconsole.WebConsole())

    def render_GET(self, request):
        pass
