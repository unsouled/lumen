import sys
import logging
import os

from twisted.application import internet, service
from twisted.internet import epollreactor
epollreactor.install()

from twisted.internet import reactor
from twisted.python import log
from twisted.python.logfile import DailyLogFile
from twisted.web import server

config = {}

def makeService(_config):
    global config
    config = _config

    if config['logpath'] != None:
        logFilePath = os.path.abspath(config['logpath'])
        logFile = DailyLogFile.fromFullPath(logFilePath)
    else:
        logFile = sys.stdout

    log.startLogging(logFile)

    lumenService = service.MultiService()

    # Bayeux Service
    import bayeux
    bayeuxFactory = bayeux.BayeuxServerFactory()
    bayeuxService = internet.TCPServer(config['port'], bayeuxFactory)
    bayeuxService.setServiceParent(lumenService)

    # WebConsole Service
    import webconsole
    site = server.Site(webconsole.WebConsole())
    webConsoleService = internet.TCPServer(config['webport'], site)
    webConsoleService.setServiceParent(lumenService)

    application = service.Application("lumen")
    lumenService.setServiceParent(application)

    return lumenService
