import ConfigParser

class Config:
    pass

class IniConfig(Config):
    filename = 'lumen.ini'
    parser = ConfigParser.ConfigParser()

    def __init__(self):
        self.parser.read(self.filename)

    def get(self, section, key):
        return self.parser.get(section, key)

class XmlConfig(Config):
    filename = 'lumen.xml'

class YmlConfig(Config):
    filename = 'lumen.yml'

class ConfigFactory():
    @staticmethod
    def create(name):
        return IniConfig()
