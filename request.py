from message import Message

class Request(Message):
	def __init__(self, channel):
		Message.__init__(self, channel)

class HandshakeRequest(Request):
	def __init__(self):
		Request.__init__(self, '/meta/handshake')

	def toArray(self):
		return [
				{
                    "id": self.id,
					"channel": self.channel,
					"version": self.version,
					"minimumVersion": self.minimumVersion,
					"supportedConnectionTypes": self.supportedConnectionTypes
					}
				]

class ConnectRequest(Request):
	def __init__(self, clientId):
		Request.__init__(self, '/meta/connect')
		self.clientId = clientId
		self.connectionType = 'long-polling'

	def toArray(self):
		return [
			{
				"channel": self.channel,
				"clientId": self.clientId,
				"connectionType": self.connectionType
				}
			]

class DisconnectRequest(Request):
	def __init__(self):
		Request.__init__(self, '/meta/disconnect')

	def toArray(self):
		return [
			{
				"channel": self.channel,
				"clientId": self.clientId
				}
			]

class SubscribeRequest(Request):
	def __init__(self):
		Request.__init__(self, '/meta/subscribe')

	def toArray(self):
		return [
			{
				"channel": self.channel,
				"clientId": self.clientId,
				"subscription": self.subscription
				}
			]

class UnsubscribeRequest(Request):
	def __init__(self):
		Request.__init__(self, '/meta/unsubscribe')

	def toArray(self):
		return [
			{
				"channel": self.channel,
				"clientId": self.clientId,
				"subscription": self.subscription,
				}
			]

class PublishRequest(Request):
    def __init__(self, channel):
        Request.__init__(self, channel)
    def toArray(self):
        return [
                {
                    "channel": self.channel,
                    "clientId": self.clientId,
                    }
                ]
