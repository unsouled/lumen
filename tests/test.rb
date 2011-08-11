require 'rubygems'
require 'eventmachine'
require 'faye'

client = Faye::Client.new('http://localhost:8080/lumen')
EM.run {
  client.handshake do
    client.connect
  end
}
