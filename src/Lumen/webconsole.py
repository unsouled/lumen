import client
import channel
import lumen

from nevow import loaders, rend, tags
from twisted.web import resource

class WebConsoleLayout(rend.Page):
    docFactory = loaders.xmlfile('template/index.xml')
    menus = [{ 'id' : 'dashboard',
               'label': 'Overview',
               'url': '/console/dashboard' },
             { 'id' : 'clients',
               'label': 'Clients',
               'url': '/console/clients' },
             { 'id': 'channels',
               'label': 'Channels',
               'url': '/console/channels' },
             { 'id': 'subscriptions',
               'label': 'Subscriptions',
               'url': '/console/subscriptions' },
             { 'id': 'transports',
               'label': 'Transports',
               'url': '/console/transports' }]

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
                tags.div()['Lumen is running on port ' + lumen.config.get('default', 'port')],
                tags.div()[
                    tags.a(href='http://github.com/unsouled/lumen')['Github']
                ]
        ]

class ClientsPage(WebConsoleLayout):
    def __init__(self):
        WebConsoleLayout.__init__(self, 'clients')

    def render_title(self):
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
        return [self.render_title(), self.render_clients_list()]

class ChannelsPage(WebConsoleLayout):
    def __init__(self):
        WebConsoleLayout.__init__(self, 'channels')

    def render_title(self):
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
        return [self.render_title(), self.render_channels_list()]

class SubscriptionsPage(WebConsoleLayout):
    def __init__(self):
        WebConsoleLayout.__init__(self, 'subscriptions')

    def render_content(self, context, data):
        return "This is Subscriptions Page"

class TransportsPage(WebConsoleLayout):
    def __init__(self):
        WebConsoleLayout.__init__(self, 'transports')

    def render_content(self, context, data):
        return "This is Transports Page"

class DashboardPage(WebConsoleLayout):
    def __init__(self):
        WebConsoleLayout.__init__(self, 'dashboard')

    def render_title(self):
        return tags.h2()['Overview']

    def render_bayeux_environments(self):
        return [
            tags.h3()['Bayeux Environmerts'],
            tags.table()[
                tags.tr()[
                    tags.th()['Endpoint'],
                    tags.td()['/' + lumen.config.get('default', 'endpoint')],
                ],
                tags.tr()[
                    tags.th()['Port'],
                    tags.td()[lumen.config.get('default', 'port')],
                ],
                tags.tr()[
                    tags.th()['Engine'],
                    tags.td()[lumen.config.get('default', 'engine')],
                ]
            ],
        ]

    def render_webconsole_environments(self):
        return [
            tags.h3()['Web console Environments'],
            tags.table()[
                tags.tr()[
                    tags.th()['Endpoint'],
                    tags.td()['/' + lumen.config.get('webconsole', 'endpoint')],
                ],
                tags.tr()[
                    tags.th()['Comet Enabled'],
                    tags.td()[lumen.config.get('webconsole', 'cometEnabled')],
                ],

            ],
        ]

    def render_content(self, context, data):
        return [
            self.render_title(),
            self.render_bayeux_environments(),
            self.render_webconsole_environments(),
        ]

class WebConsole(resource.Resource):
    class Clients(resource.Resource):
        def render(self, httpRequest):
            return ClientsPage().renderSynchronously()

    class Subscriptions(resource.Resource):
        def render(self, httpRequest):
            return SubscriptionsPage().renderSynchronously()

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
        self.putChild('subscriptions', self.Subscriptions())
        self.putChild('transports', self.Transports())

    def render(self, httpRequest):
        return DashboardPage().renderSynchronously()

