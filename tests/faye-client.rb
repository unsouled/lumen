require 'rubygems'
require 'eventmachine'
require 'faye'

Faye::Logging.log_level = :info
Faye.logger = lambda { |m| puts m }

EM.run do
  client = Faye::Client.new("http://unsouled.net:9090/")
  client.publish('/test', { :body => 'ya ho!'})
end

