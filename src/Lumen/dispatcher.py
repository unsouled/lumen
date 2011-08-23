import client

def dispatch(msg):
    try:
        clientId = msg.requests[0].attributes['clientId']
        c = client.clients[clientId]
    except:
        clientId = client.generateClientId()
        c = client.Client(clientId)
        client.clients[clientId] = c
    c.handleMessage(msg)
