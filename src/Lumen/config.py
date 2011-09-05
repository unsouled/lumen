import ConfigParser
import os

class Config:
    pass

class IniConfig(Config):
    filename = 'lumen.ini'
    parser = ConfigParser.ConfigParser()

    def __init__(self):
        appRoot = os.path.abspath(os.path.dirname(__file__) + '/../..')
        configFile = appRoot + '/config/' + self.filename
        print configFile
        self.parser.read(configFile)
        self.set('default', 'APP_ROOT', appRoot)

    def get(self, section, key):
        return self.parser.get(section, key)

    def set(self, section, key, value):
        self.parser.set(section, key, value)

class XmlConfig(Config):
    filename = 'lumen.xml'

class YmlConfig(Config):
    filename = 'lumen.yml'

class ConfigFactory():
    @staticmethod
    def create(name):
        return IniConfig()
