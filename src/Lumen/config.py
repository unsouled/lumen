import ConfigParser
import os
from pkg_resources import resource_filename
from optparse import OptionParser

class Config():
    parser = ConfigParser.ConfigParser()

    def __init__(self, configFile):
        if configFile:
            self.configFile = configFile
        else:
            self.configFile = resource_filename(__name__, 'res/lumen.conf')
        self.parser.read(self.configFile)

    def get(self, section, key):
        return self.parser.get(section, key)

_config = None
def getConfig():
    global _config
    if _config is None:
        optparser = OptionParser()
        optparser.add_option('-c', '--config', dest='conf',
                             help='lumen configuration file path', 
                             metavar='<CONF FILE>')
        (options, args) = optparser.parse_args()
        _config = Config(options.conf)
    return _config
        
