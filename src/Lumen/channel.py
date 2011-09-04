from twisted.internet import reactor, defer
import client

connections = {}

class Channel():
    def __init__(self, channelId):
        self.id = channelId
        self.subscribers = set()

    def publish(self, msg):
        d = defer.Deferred()
        d.callback([{ 'channel': msg.attributes['channel'],
                'successful': True,
                'id': msg.attributes['id'] }])

        for c in self.subscribers:
            try:
                l = connections[c.id]

                for dc, dmsg in l:
                    try:
                        dc.callback([{ 'id': dmsg.attributes['id'],
                                 'channel': dmsg.attributes['channel'],
                                 'successful': True,
                                 'error': '',
                                 'timestamp': '12:00:00 1970',
                                 'data': msg.attributes['data'],
                                 'advice': { 'reconnect': 'retry' } }, msg.attributes])
                    except:
                        del connections[c.id]
            except KeyError:
                pass

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

        if not hasattr(connections,msg.attributes['clientId']):
            connections[msg.attributes['clientId']] = []

        l = connections[msg.attributes['clientId']]
        l.append((d, msg))

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
