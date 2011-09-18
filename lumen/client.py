from twisted.internet import reactor
import uuid
import channel
from datetime import datetime
import apns
import config
import glob
import os
import hashlib

clients = {}

class Client():
    def __init__(self, clientId):
        self.id = clientId
        self.connection = None
        self.channelsSubscribing = set()
        self.typename = 'comet'
        self.createdAt = datetime.now()
        self.messages = []

    def publish(self, channelId, msg):
        self.messages.append((channelId, msg))
        self.response()

    def response(self):
        if self.connection and self.messages:
            d = self.connection[0]
            cmsg = self.connection[1]
            data = [{'id': cmsg.attributes['id'],
                     'channel': cmsg.attributes['channel'],
                     'successful': True,
                     'error': '',
                     'timestamp': '12:00:00 1970',
                     'advice': { 'reconnect': 'retry' } }]
            while self.messages:
                channelId, msg = self.messages.pop(0)
                msg.attributes['data']['channel'] = channelId
                data.append(msg.attributes)
            d.callback(data)
            self.connection = None

    def subscribe(self, ch):
        channel.get(ch).subscribe(self)
        self.channelsSubscribing.add(ch)

    def unsubscribe(self, ch):
        channel.get(ch).unsubscribe(self)

    def disconnect(self):
        for ch in self.channelsSubscribing:
            channel.get(ch).unsubscribe(self)

class IOSClient(Client):
    def __init__(self, clientId, deviceToken, appId):
        Client.__init__(self, clientId)
        self.typename = 'apns'
        self.deviceToken = deviceToken
        self.appId = appId

    def _doHandleMessage(self, msg):
        responses = msg.handle(self)
        msg.response(responses)

        reactor.callLater(0.01, self.__connectToAPNSServer)

    def response(self):
        if self.connection:
            d = self.connection[0]
            cmsg = self.connection[1]
            data = [{'id': cmsg.attributes['id'],
                     'channel': cmsg.attributes['channel'],
                     'successful': True,
                     'error': '',
                     'timestamp': '12:00:00 1970',
                     'advice': { 'reconnect': 'retry' } }]
            d.callback(data)

    def publish(self, channelId, msg):
        msg.attributes['data']['channel'] = channelId
        cert, priv = self.__findCertificationFiles(channelId)
        apns.push(self.deviceToken, msg.attributes, cert, priv)

    def __findCertificationFiles(self, channelId):
        certdir = config.getConfig().get('default', 'certdir')
        appdir = hashlib.md5(self.appId).hexdigest()
        cert = '%s/%s/cert.pem' % (certdir, appdir)
        priv = '%s/%s/priv.pem' % (certdir, appdir)
        return cert, priv

def generateClientId():
    return uuid.uuid4().urn[9:]

def findById(clientId):
    return clients[clientId]

def remove(clientId):
    clients.pop(clientId)

class ClientFactory():
    @staticmethod
    def create(msg):
        clientId = generateClientId()
        if 'apns' in msg.attributes['supportedConnectionTypes']:
           deviceToken = msg.attributes['deviceToken']
           appId = msg.attributes['applicationId']
           c = IOSClient(clientId, deviceToken, appId)
        else:
            c = Client(clientId)
        clients[clientId] = c
        return c
