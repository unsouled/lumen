from twisted.internet import reactor, defer
from json import JSONEncoder, JSONDecoder

import client
import connection
import uuid

class Channel():
    def __init__(self, channelId):
        self.id = channelId
        self.subscribers = set()

    def publish(self, msg):
        data = [{ 'channel': msg.attributes['channel'],
                  'data': msg.attributes['data'],
                  'id': msg.attributes['id'] }]

        for subscriber in self.subscribers:
            subscriber.publish(data)

        response =  { 'channel': msg.attributes['channel'],
                      'successful': True,
                      'id': msg.attributes['id'] }

        return response

    def subscribe(self, client):
        self.subscribers.add(client)

    def unsubscribe(self, client):
        self.subscribers.remove(client)

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
        clientId = msg.attributes['clientId']
        response = { 'id': msg.attributes['id'],
                     'channel': msg.attributes['channel'],
                     'successful': True,
                     'error': '',
                     'clientId': clientId,
                     'timestamp': '12:00:00 1970',
                     'advice': { 'reconnect': 'retry' } }

        subscribe(msg.attributes['subscription'], client.findById(clientId))
        return response

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

def subscribe(ch, client):
    chset = expand(ch)
    for ch in chset:
        get(ch).subscribe(client)

def get(channelId):
    try:
        ch = channels[channelId]
    except:
        ch = Channel(channelId)
        channels[channelId] = ch

    return ch
