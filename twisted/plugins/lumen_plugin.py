from twisted.application.service import ServiceMaker

lumen = ServiceMaker(
        'lumen', 'lumen.tap', 'Run a lumen service', 'lumen')
