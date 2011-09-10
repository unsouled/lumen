from twisted.web import resource, static
import twisted.web.server
import webconsole
import config
from message import Message
from pkg_resources import resource_filename

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
        self.putChild('public', static.File(resource_filename(__name__, 'res/public')))

    def render_GET(self, request):
        pass
