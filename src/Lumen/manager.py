import channel

class Channel():
    channels = { '/meta/handshake': channel.Handshake(),
            '/meta/connect': channel.Connect(),
            '/meta/disconnect': channel.Disconnect(),
            '/meta/subscribe': channel.Subscribe(),
            '/meta/unsubscribe': channel.Unsubscribe() }

    @staticmethod
    def find(channelId):
        try:
            ch = Channel.channels[channelId]
        except:
            ch = None

        return ch

    @staticmethod
    def get(channelId):
        ch = Channel.find(channelId)

        if ch:
            return ch
        else:
            ch = channel.Channel(channelId)
            Channel.channels[channelId] = ch

        return ch

