from twisted.web import resource
from json import JSONEncoder, JSONDecoder
import uuid
import message
import request
import response

from json import JSONEncoder, JSONDecoder

class RequestParser():
	@staticmethod
	def parse(content):
		data = JSONDecoder().decode(content)[0]

		channel = data['channel']

		if (channel == '/meta/handshake'):
			req = request.HandshakeRequest()
		elif (channel == '/meta/connect'):
			req = request.ConnectRequest(data['clientId'])
		elif (channel == '/meta/disconnect'):
			req = request.DisconnectRequest()
		elif (channel == '/meta/subscribe'):
			req = request.SubscribeRequest()
		elif (channel == '/meta/unsubscribe'):
			req = request.UnsubscribeRequest()
		else:
			req = request.PublishRequest(channel)

		return req

class Handler():
	def __init__(self, request):
		self.request = request
	
	def process(self):
		if (self.request.channel == '/meta/handshake'):
			res = response.HandshakeResponse()
		elif (self.request.channel == '/meta/connect'):
			res = responseConnectResponse(self.request.clientId)

		return res

class Lumen(resource.Resource):
	def render(self, request):
		print 'request received'
		content = request.content.read()
		req = RequestParser.parse(content)
		res = Handler(req).process()
		print res.toJSON()
		return res.toJSON()

class Bayeux(resource.Resource):
	def __init__(self):
		resource.Resource.__init__ (self)
		self.putChild('lumen', Lumen())

		def render_GET(self, request):
			pass
