from twisted.web import server, resource
from twisted.internet import reactor
from json import JSONEncoder

class Meta(resource.Resource):
    class Handshake(resource.Resource):
        isLeaf = True

        def render_GET(self, request):
            request.setHeader('Content-type', 'application/json')
            data = [{'channel': '/meta/handshake',
                     'version': '1.0',
                     'minimumVersion': '1.0beta',
                     'supportedConnectionTypes': 
                     ['long-polling', 'callback-polling', 'iframe']}]
            return JSONEncoder().encode(data)

    def __init__(self):
        resource.Resource.__init__(self)
        self.putChild('handshake', Meta.Handshake())

    def getChild(self, name, request):
        if name == '':
            return resource.ErrorPage(404, 'Not Found', 'no meta data')
        return resource.Resource.getChild(self, name, request)

    def render_GET(self, request):
        return 'this is meta'

class Bayeux(resource.Resource):
    def __init__(self):
        resource.Resource.__init__ (self)
        self.putChild('meta', Meta())

    def getChild(self, name, request):
        if name == '':
            return resource.ErrorPage(404, 'Not Found', 'There is no resource.')
        return resource.Resource.getChild(self, name, request)

    def render_GET(self, request):
        return 'Hello, my name is %s' % request.prepath[0]

lumen = server.Site(Bayeux())
reactor.listenTCP(8080, lumen)
reactor.run()
 
