import urllib2
import request
import json

def sendRequest(data):
    host = 'http://localhost:1234/lumen'
    req = urllib2.Request(host, data, {'Content-Type': 'application/json'})
    response_stream = urllib2.urlopen(req)
    response = response_stream.read()
    return response

if __name__ == '__main__':
    channel = '/com/lumen/test'

    clientId = json.loads(sendRequest(request.Handshake().jsonize()))[0]['clientId']
    sendRequest(request.Subscribe(clientId, channel).jsonize())
    sendRequest(request.Connect(clientId).jsonize())
