from twisted.internet import reactor, defer
from json import JSONEncoder, JSONDecoder

import connection
import uuid

class Channel():
    def __init__(self, channelId):
        self.id = channelId
        self.subscribers = []

    def publish(self, msg):
        d = defer.Deferred()
        data =  [{ "channel": msg.attributes['channel'],
                   "successful": True,
                   "id": msg.attributes['id'] }]

        receivers = [connection.find(s) for s in self.subscribers]

        for tup in receivers:
            dm, cd = tup
            dd = [{ "id": dm.attributes['id'],
                    "channel": dm.attributes['channel'],
                    "successful": True,
                    "error": "",
                    "clientId": dm.attributes['clientId'],
                    "timestamp": '12:00:00 1970',
                    "advice": { 'reconnect': 'retry' } },
                  { "channel": msg.attributes['channel'],
                    "clientId": msg.attributes['clientId'],
                    "data": msg.attributes['data'],
                    "id": msg.attributes['id'] }]
            cd.callback(dd)

        d.callback(data)
        return d

    def getSubscribers(self):
        return self.subscribers

    def subscribe(self):
        pass

    def unsubscribe(self):
        pass

class Meta(Channel):
    pass
class Service(Channel):
    def __init__(self, serviceId):
        Channel.__init__(self, '/service/' + serviceId)

class Handshake(Meta):
    def __init__(self):
        Channel.__init__(self, '/meta/handshake')

    def publish(self, msg):
        d = defer.Deferred()
        data = [{ "id": msg.attributes['id'],
                  "channel": msg.attributes['channel'],
                  "version": msg.attributes['version'],
                  "minimumVersion": msg.attributes['minimumVersion'],
                  "supportedConnectionTypes": ["long-polling"],
                  "clientId": uuid.uuid4().urn[9:],
                  "successful": True,
                  "authSuccessful": True,
                  "advice": { 'reconnect': 'retry' } }]
        d.callback(data)
        return d

class Connect(Meta):
    def __init__(self):
        Channel.__init__(self, '/meta/connect')

    def publish(self, msg):
        d = defer.Deferred()
        connection.add(msg, d)

        return d

class Disconnect(Meta):
    def __init__(self):
        Channel.__init__(self, '/meta/disconnect')

class Subscribe(Meta):
    def __init__(self):
        Channel.__init__(self, '/meta/subscribe')

    def publish(self, msg):
        d = defer.Deferred()
        clientId = msg.attributes['clientId']
        data = [{ "id": msg.attributes['id'],
                  "channel": msg.attributes['channel'],
                  "clientId": clientId,
                  "subscription": [ msg.attributes['subscription'] ],
                  "successful": True,
                  "error": "" }]

        dm, cd = connection.find(clientId)
        dd = [{ "id": dm.attributes['id'],
                "channel": dm.attributes['channel'],
                "successful": True,
                "error": "",
                "clientId": dm.attributes['clientId'],
                "timestamp": '12:00:00 1970',
                "advice": { 'reconnect': 'retry' } }]
        try:
            cd.callback(dd)
        except:
            connection.remove(dm)

        channel = get(msg.attributes['subscription'])
        channel.subscribers.append(clientId)
        d.callback(data)

        return d

class Unsubscribe(Meta):
    def __init__(self):
        Channel.__init__(self, '/meta/unsubscribe')


channels = { '/meta/handshake': Handshake(),
             '/meta/connect': Connect(),
             '/meta/disconnect': Disconnect(),
             '/meta/subscribe': Subscribe(),
             '/meta/unsubscribe': Unsubscribe() }

def find(channelId):
    try:
        ch = channels[channelId]
    except:
        ch = None

    return ch

def get(channelId):
    ch = find(channelId)

    if ch:
        return ch
    else:
        ch = Channel(channelId)
        channels[channelId] = ch

    return ch

