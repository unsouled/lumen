class Engine:
    pass

class InMemory(Engine):
    pass

class Redis(Engine):
    pass

class EngineFactory:
    @statiemethod
    def create(engineName):
        if engineName == 'memory':
            return InMemory()
        elif engineName == 'redis':
            return Redis()
