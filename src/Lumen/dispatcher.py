import client


def dispatch(msg):
    try:
        clientId = msg.requests[0].attributes['clientId']
        c = client.clients[clientId]
    except:
        c = client.ClientFactory.create(msg.requests[0])
    c.handleMessage(msg)
