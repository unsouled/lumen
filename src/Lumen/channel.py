from twisted.internet import reactor
import client

class Channel():
    def __init__(self, channelId):
        self.id = channelId
        self.subscribers = set()

    def publish(self, msg):
        reactor.callLater(0.01, self._doPublish, msg)

        response =  { 'channel': msg.attributes['channel'],
                      'successful': True,
                      'id': msg.attributes['id'] }

        return response

    def _doPublish(self, msg):
        data = [{ 'channel': msg.attributes['channel'],
                  'data': msg.attributes['data'],
                  'id': msg.attributes['id'] }]

        for subscriber in self.subscribers:
            subscriber.publish(data)

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
        response = { 'id': msg.attributes['id'],
                      'channel': msg.attributes['channel'],
                      'version': msg.attributes['version'],
                      'minimumVersion': msg.attributes['minimumVersion'],
                      'supportedConnectionTypes': ["long-polling"],
                      'successful': True,
                      'authSuccessful': True,
                      'advice': { 'reconnect': 'retry' } }
        return response

class Connect(Meta):
    def __init__(self):
        Meta.__init__(self, '/meta/connect')

    def publish(self, msg):
        response = { 'id': msg.attributes['id'],
                     'channel': msg.attributes['channel'],
                     'successful': True,
                     'error': '',
                     'timestamp': '12:00:00 1970',
                     'advice': { 'reconnect': 'retry' } }
        return response

class Disconnect(Meta):
    def __init__(self):
        Meta.__init__(self, '/meta/disconnect')

class Subscribe(Meta):
    def __init__(self):
        Meta.__init__(self, '/meta/subscribe')

    def publish(self, msg):
        reactor.callLater(0.01, self._doPublish, msg)

        response = { 'id': msg.attributes['id'],
                     'channel': msg.attributes['channel'],
                     'successful': True,
                     'error': '',
                     'clientId': msg.attributes['clientId'],
                     'timestamp': '12:00:00 1970',
                     'advice': { 'reconnect': 'retry' } }
        return response

    def _doPublish(self, msg):
        clientId = msg.attributes['clientId']
        subscribe(msg.attributes['subscription'], client.findById(clientId))

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
    chset = expand(ch)
    for ch in chset:
        get(ch).subscribe(c)

def get(channelId):
    try:
        ch = channels[channelId]
    except:
        ch = Channel(channelId)
        channels[channelId] = ch

    return ch
