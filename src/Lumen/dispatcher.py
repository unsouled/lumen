import client

def dispatch(msg):
    try:
        channel =  msg.requests[0].attributes['channel']
        if channel == '/meta/handshake':
            c = client.ClientFactory.create(msg)
        else:
            clientId = msg.requests[0].attributes['clientId']
            c = client.clients[clientId]
        c.handleMessage(msg)
    except:
        msg.httpRequest.finish()
