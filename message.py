from json import JSONEncoder

class Message():
	def __init__(self, channel):
		self.channel = channel
		self.version = '1.0'
		self.minimumVersion ='1.0beta'

	def id(self):
		pass

	def channel(self):
		pass

	def client(self):
		pass
	
	def toJSON(self):
		return JSONEncoder().encode(self.toArray())
