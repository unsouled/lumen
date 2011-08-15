connections = {}

def find(clientId):
    return connections[clientId]

def add(message, d):
    print 'connection added'
    connections[message.attributes['clientId']] = (message, d)

def remove(message):
    del connections[message.attributes['clientId']]
