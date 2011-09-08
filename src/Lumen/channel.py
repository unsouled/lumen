from twisted.internet import reactor, defer
import client

class Channel():
    def __init__(self, channelId):
        self.id = channelId
        self.subscribers = set()

    def getAllPatternSubscribers(self):
        subscribers = set()
        chs = expand(self.id)
        for ch in chs:
            subscribers = subscribers.union(get(ch).subscribers)
        return subscribers

    def publish(self, msg):
        d = defer.Deferred()
        d.callback([{ 'channel': msg.attributes['channel'],
                'successful': True,
                'id': msg.attributes['id'] }])

        subscribers = self.getAllPatternSubscribers()
        for subscriber in subscribers:
            subscriber.publish(self.id, msg)

        return d

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

    def publish(self, msg):
        d = defer.Deferred()
        c = client.ClientFactory.create(msg)
        d.callback([{ 'id': msg.attributes['id'],
                 'channel': msg.attributes['channel'],
                 'clientId': c.id,
                 'version': msg.attributes['version'],
                 'minimumVersion': msg.attributes['minimumVersion'],
                 'supportedConnectionTypes': ['callback-polling', 'long-polling', 'apns'],
                 'successful': True,
                 'authSuccessful': True,
                 'advice': { 'reconnect': 'retry' } }])
        return d

class Connect(Meta):
    def __init__(self):
        Meta.__init__(self, '/meta/connect')

    def publish(self, msg):
        d = defer.Deferred()
        c = client.clients[msg.attributes['clientId']]
        c.connection = (d, msg)
        c.response()

        return d

class Disconnect(Meta):
    def __init__(self):
        Meta.__init__(self, '/meta/disconnect')

    def publish(self, msg):
        clientId = msg.attributes['clientId']
        c = client.findById(clientId)
        c.disconnect()
        client.remove(clientId)

        d = defer.Deferred()
        d.callback([{ 'id': msg.attributes['id'],
                 'channel': msg.attributes['channel'],
                 'successful': True }])

        return d

class Subscribe(Meta):
    def __init__(self):
        Meta.__init__(self, '/meta/subscribe')

    def publish(self, msg):
        clientId = msg.attributes['clientId']
        c = client.findById(clientId)
        reactor.callLater(0.01, c.subscribe, msg.attributes['subscription'])

        d = defer.Deferred()
        d.callback([{ 'id': msg.attributes['id'],
                 'channel': msg.attributes['channel'],
                 'subscription': msg.attributes['subscription'],
                 'successful': True,
                 'error': ''}])
        return d

class Unsubscribe(Meta):
    def __init__(self):
        Channel.__init__(self, '/meta/unsubscribe')

    def publish(self, msg):
        clientId = msg.attributes['clientId']
        c = client.findById(clientId)
        reactor.callLater(0.01, c.unsubscribe, msg.attributes['subscription'])

        d = defer.Deferred()
        d.callback([{ 'id': msg.attributes['id'],
                 'channel': msg.attributes['channel'],
                 'subscription': msg.attributes['subscription'],
                 'successful': True,
                 'error': '' }])
        return d

channels = { '/meta/handshake': Handshake(),
             '/meta/connect': Connect(),
             '/meta/disconnect': Disconnect(),
             '/meta/subscribe': Subscribe(),
             '/meta/unsubscribe': Unsubscribe() }

def expand(ch):
    chs = ['/**', ch, '/'.join(ch.split('/')[:-1]).__add__('/*').replace('//*', '/*')]
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
