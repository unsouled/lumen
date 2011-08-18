import client

class Channel():
    def __init__(self, channelId):
        self.id = channelId
        self.subscribers = set()

    def process(self, msg):
        return { 'channel': msg.attributes['channel'],
                 'successful': True,
                 'id': msg.attributes['id'] }

    def subscribe(self, c):
        self.subscribers.add(c)

    def unsubscribe(self, c):
        self.subscribers.remove(c)

class Meta(Channel):
    def __init__(self, channelId):
        Channel.__init__(self, channelId)

class Service(Channel):
    def __init__(self, serviceId):
        Channel.__init__(self, '/service/' + serviceId)

class Handshake(Meta):
    def __init__(self):
        Meta.__init__(self, '/meta/handshake')

    def process(self, msg):
        return { 'id': msg.attributes['id'],
                 'channel': msg.attributes['channel'],
                 'version': msg.attributes['version'],
                 'minimumVersion': msg.attributes['minimumVersion'],
                 'supportedConnectionTypes': ["long-polling"],
                 'successful': True,
                 'authSuccessful': True,
                 'advice': { 'reconnect': 'retry' } }

class Connect(Meta):
    def __init__(self):
        Meta.__init__(self, '/meta/connect')

    def process(self, msg):
        return { 'id': msg.attributes['id'],
                 'channel': msg.attributes['channel'],
                 'successful': True,
                 'error': '',
                 'timestamp': '12:00:00 1970',
                 'advice': { 'reconnect': 'retry' } }

class Disconnect(Meta):
    def __init__(self):
        Meta.__init__(self, '/meta/disconnect')

class Subscribe(Meta):
    def __init__(self):
        Meta.__init__(self, '/meta/subscribe')

    def process(self, msg):
        clientId = msg.attributes['clientId']
        subscribe(msg.attributes['subscription'], client.findById(clientId))

        return { 'id': msg.attributes['id'],
                 'channel': msg.attributes['channel'],
                 'successful': True,
                 'error': '',
                 'clientId': msg.attributes['clientId'],
                 'timestamp': '12:00:00 1970',
                 'advice': { 'reconnect': 'retry' } }

class Unsubscribe(Meta):
    def __init__(self):
        Channel.__init__(self, '/meta/unsubscribe')


channels = { '/meta/handshake': Handshake(),
             '/meta/connect': Connect(),
             '/meta/disconnect': Disconnect(),
             '/meta/subscribe': Subscribe(),
             '/meta/unsubscribe': Unsubscribe() }

def expand(ch):
    chset = set([ch])
    segments = ch.split('/')
    segments[-1] = '*'
    chset.add('/'.join(segments))

    while len(segments) > 1:
        segments[-1] = '**'
        chset.add('/'.join(segments))
        segments.pop()

    return chset

def subscribe(ch, c):
    get(ch).subscribe(c)

def get(channelId):
    try:
        ch = channels[channelId]
    except:
        ch = Channel(channelId)
        channels[channelId] = ch

    return ch
