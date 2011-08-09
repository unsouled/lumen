from message import Message

class Response(Message):
    def __init__(self, channel):
        Message.__init__(self, channel)

    def toArray(self):
        return [
                {
                    "id": self.id,
                    "channel": self.channel,
                    }
                ]

class HandshakeResponse(Response):
	def __init__(self):
		Response.__init__(self, '/meta/handshake')
		self.supportedConnectionTypes = ["long-polling","callback-polling"]
		self.clientId = self.generateClientId()
		self.successful = True
		self.authSuccessful = True
		self.advice = { 'reconnect': 'retry' }
	
	def generateClientId(self):
		return 'someGeneratedClientId'

	def toArray(self):
		return [
				{
					"id": self.id,
					"channel": self.channel,
					"version": self.version,
					"minimumVersion": self.minimumVersion,
					"supportedConnectionTypes": self.supportedConnectionTypes,
					"clientId": self.clientId,
					"successful": self.successful,
					"authSuccessful": self.authSuccessful,
					"advice": self.advice
					}
				]

class ConnectResponse(Response):
	def __init__(self, clientId):
		Response.__init__(self, '/meta/connect')
		self.successful = True
		self.error = ''
		self.clientId = clientId
		self.timestamp =  '12:00:00 1970'
		self.advice =  { "reconnect": "retry" }

	def toArray(self):
		return [
			{
				"channel": self.channel,
				"successful": self.successful,
				"error": self.error,
				"clientId": self.clientId,
				"timestamp": self.timestamp,
				"advice": self.advice
				}
			]


class DisconnectResoponse(Response):
	def __init__(self):
		self.channel = '/meta/disconnect'

	def toArray(self):
		return [
			{
				"channel": self.channel,
				"clientId": self.clientId,
				"successful": self.successful
				}
			]

class SubscribeResoponse(Response):
	def __init__(self):
		self.channel = '/meta/subscribe'

	def toArray(self):
		return [
			{
				"channel": self.channel,
				"clientId": self.clientId,
				"subscription": self.subscription,
				"successful": self.successful,
				"error": self.error,
				}
			]

class UnsubscribeResponse(Response):
	def __init__(self):
		self.channel = '/meta/unsubscribe'

	def toArray(self):
		return [
			{
				"channel": self.channel,
				"clientId": self.clientId,
				"subscription": self.subscription,
				"successful": self.successful,
				"error": self.error,
				}
			]

