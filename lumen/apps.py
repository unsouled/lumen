class App():
  def __init__(self, cert, priv):
    self.cert = cert
    self.priv = priv

apps = {}
apps['my-app'] = App('test.pem', 'test.pem')

def find(appId):
  return apps[appId]
