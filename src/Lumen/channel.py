from twisted.internet import reactor
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
        c = client.findById(clientId)
        reactor.callLater(0.01, c.subscribe, msg.attributes['subscription'])

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
    chs = ['/**', ch, '/' + '/'.join(ch.split('/')[1:-1]) + '/*']
    segments = ch.split('/')[1:-1]
    while segments:
        chs.append('/' + '/'.join(segments) + '/**')
        segments = segments[:-1]
    return chs

def get(channelId):
    try:
        ch = channels[channelId]
    except:
        ch = Channel(channelId)
        channels[channelId] = ch

    return ch
