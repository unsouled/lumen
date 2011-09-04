from json import JSONEncoder

class Transport():
    pass

class LongPolling(Transport):
    def __init__(self, httpRequest):
        self.httpRequest = httpRequest

    def read(self):
        self.content = self.httpRequest.content.read()
        return self.content

    def write(self, data):
        self.httpRequest.write(JSONEncoder().encode(data))
        self.httpRequest.finish()

class CallbackPolling(Transport):
    def __init__(self, httpRequest):
        self.httpRequest = httpRequest

    def read(self):
        self.content = self.httpRequest.args['message'][0]
        self.callback = self.httpRequest.args['jsonp'][0]
        return self.content

    def write(self, data):
        data = '%s(%s)' % (self.callback, JSONEncoder().encode(data))
        self.httpRequest.write(data)
        self.httpRequest.finish()

class TransportFactory():
    @staticmethod
    def create(httpRequest):
        if httpRequest.method == 'POST':
            return LongPolling(httpRequest)
        elif httpRequest.method == 'GET':
            return CallbackPolling(httpRequest)

