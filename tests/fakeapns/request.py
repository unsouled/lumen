import json

class Request():
    def __init__(self, channel):
        self.attributes = {'channel': channel, 'id': 0}

    def jsonize(self):
        return json.dumps([self.attributes])

class Handshake(Request):
    def __init__(self):
        Request.__init__(self, '/meta/handshake')
        self.attributes['version'] = '1.0'
        self.attributes['minimumVersion'] = '1.0beta'
        self.attributes['supportedConnectionTypes'] = ['long-polling', 
                                                       'callback-polling', 
                                                       'apns']
        self.attributes['deviceToken'] = 'b071e0ecebc859e60310f7671d7d1bd3dbc2b760ed258fbe3d76ec974ccd4e89'
        self.attributes['applicationId'] = 'fakeapns'

class Connect(Request):
    def __init__(self, clientId):
        Request.__init__(self, '/meta/connect')
        self.attributes['clientId'] = clientId
        self.attributes['connectionType'] = 'apns'

class Subscribe(Request):
    def __init__(self, clientId, subscription):
        Request.__init__(self, '/meta/subscribe')
        self.attributes['clientId'] = clientId
        self.attributes['subscription'] = subscription
