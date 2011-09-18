from zope.interface import implements

from twisted.python import usage
from twisted.plugin import IPlugin
from twisted.application.service import IServiceMaker
from twisted.application import internet

import lumen

DEFAULT_BAYEUX_PORT = 9090
DEFAULT_WEBCONSOLE_PORT = 8000

class Options(usage.Options):
    optParameters = [
        ['file', 'f', '/etc/lumen'],
        ['templates', 't', '/usr/share/lumen/templates'],
        ['engine', 'e', 'memory'],
        ['logpath', 'lp', None],
        ['port', 'p', DEFAULT_BAYEUX_PORT],
        ['cport', 'cp', DEFAULT_WEBCONSOLE_PORT],
    ]

def makeService(options):
    """
    Construct a TCPServer from a factory defined in myproject.
    """
    return lumen.makeService(options)
