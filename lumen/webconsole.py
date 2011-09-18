import client
import channel
import lumen
import os
#import config

from nevow import loaders, rend, tags
from twisted.web import resource, static
from pkg_resources import resource_filename

class WebConsoleLayout(rend.Page):
    docFactory = loaders.xmlfile(resource_filename(__name__, 'res/index.xml'))
    endpoint = ''
    menus = [{ 'id' : 'dashboard',
               'label': 'Overview',
               'url': endpoint + '/dashboard' },
             { 'id' : 'clients',
               'label': 'Connections',
               'url': endpoint + '/clients' },
             { 'id': 'channels',
               'label': 'Channels',
               'url': endpoint + '/channels' },
             { 'id': 'transports',
               'label': 'Transports',
               'url': endpoint + '/transports' }]

    def __init__(self, data):
        rend.Page.__init__(self, data)

    def find_menu(self, name):
        for m in self.menus:
            if m['id'] == name:
                return m

    def build_menuitem(self, name, selected):
        menu = self.find_menu(name)
        menuitem = tags.li()[tags.a(href=menu['url'])[menu['label']]]
        if selected == name:
            menuitem.attributes['class'] = 'selected'
        return menuitem

    def render_menuitems(self, context, selected):
        return tags.ul(id='menu')[
                [self.build_menuitem(menu['id'], selected) for menu in self.menus]
        ]

    def render_footer(self, context, data):
        return  tags.p() [
                tags.div()['Lumen is running on port %s' % lumen.config['port']],
                tags.div()[
                    tags.a(href='http://github.com/unsouled/lumen')['Github']
                ]
        ]

class ClientsPage(WebConsoleLayout):
    def __init__(self):
        WebConsoleLayout.__init__(self, 'clients')

    def render_title(self, context, data):
        return tags.h2()["Clients"]

    def render_clients_list(self):
        result = tags.table()
        result.children.append(
            tags.tr()[
                tags.th()['id'],
                tags.th()['type'],
                tags.th()['created at'],


            ]
        )
        for clientId, c in client.clients.items():
            result.children.append(
                tags.tr()[
                    tags.td()[clientId],
                    tags.td()[c.typename],
                    tags.td()[c.createdAt.strftime("%A, %d. %B %Y %I:%M%p")],
                ]
            )
        return result

    def render_content(self, context, data):
        return [self.render_clients_list()]

class ChannelsPage(WebConsoleLayout):
    def __init__(self):
        WebConsoleLayout.__init__(self, 'channels')

    def render_title(self, context, data):
        return tags.h2()["Channels"]

    def render_channels_list(self):
        result = tags.table()
        result.children.append(
            tags.tr()[
                tags.th()['id'],
                tags.th()['subscribers'],
            ]
        )
        for clientId, c in channel.channels.items():
            result.children.append(
                tags.tr()[
                    tags.td()[c.id],
                    tags.td()[len(c.subscribers)],
                ]
            )
        return result

    def render_content(self, context, data):
        return [self.render_channels_list()]

class TransportsPage(WebConsoleLayout):
    def __init__(self):
        WebConsoleLayout.__init__(self, 'transports')

    def render_title(self, context, data):
        return tags.h2()['Transports']

    def render_content(self, context, data):
        return [
            tags.h3()['APNS'],
            tags.h4()['Applications'],
        ]

class DashboardPage(WebConsoleLayout):
    def __init__(self):
        WebConsoleLayout.__init__(self, 'dashboard')

    def tail_logs(self, f, window=30):
        BUFSIZ = 1024
        f.seek(0, 2)
        bytes = f.tell()
        size = window
        block = -1
        data = []
        while size > 0 and bytes > 0:
            if (bytes - BUFSIZ > 0):
                # Seek back one whole BUFSIZ
                f.seek(block*BUFSIZ, 2)
                # read BUFFER
                data.append(f.read(BUFSIZ))
            else:
                # file too small, start from begining
                f.seek(0,0)
                # only read what was not read
                data.append(f.read(bytes))
            linesFound = data[-1].count('\n')
            size -= linesFound
            bytes -= BUFSIZ
            block -= 1
        return '\n'.join(''.join(data).splitlines()[-window:])

    def render_title(self, context, data):
        return tags.h2()['Overview']

    def render_bayeux_environments(self):
        return [
            tags.h3()['Bayeux Environmerts'],
            tags.table()[
                tags.tr()[
                    tags.th()['Port'],
                    tags.td()[lumen.config['port']],
                ],
                tags.tr()[
                    tags.th()['Engine'],
                    tags.td()[lumen.config['engine']],
                ]
            ],
        ]

    def render_webconsole_environments(self):
        return [
            tags.h3()['Web console Environments'],
            tags.table()[
                tags.tr()[
                    tags.th()['Port'],
                    tags.td()[lumen.config['cport']],
                ],

            ],
        ]

    def render_logs(self):
        if lumen.config['logpath']:
            logFilePath = os.path.abspath(os.path.join(lumen.config['logpath'], 'lumen.log'))
            logFile = open(logFilePath)
            return [
                  tags.h3()['Logs'],
                  tags.pre(style='border:1px solid #ccc; padding: 0.5em; overflow:auto')[
                      self.tail_logs(logFile)
                  ],
            ]
        else:
            return []

    def render_content(self, context, data):
        return [
            self.render_bayeux_environments(),
            self.render_webconsole_environments(),
            self.render_logs(),
        ]

class WebConsole(resource.Resource):
    class Clients(resource.Resource):
        def render(self, httpRequest):
            return ClientsPage().renderSynchronously()

    class Channels(resource.Resource):
        def render(self, httpRequest):
            return ChannelsPage().renderSynchronously()

    class Transports(resource.Resource):
        def render(self, httpRequest):
            return TransportsPage().renderSynchronously()

    def __init__(self):
        resource.Resource.__init__(self)
        self.putChild('dashboard', self)
        self.putChild('clients', self.Clients())
        self.putChild('channels', self.Channels())
        self.putChild('transports', self.Transports())
        self.putChild('public', static.File('/home/unsouled/lumen/lumen/res/public'))

    def render_GET(self, httpRequest):
        return DashboardPage().renderSynchronously()

