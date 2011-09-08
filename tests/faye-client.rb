require 'rubygems'
require 'eventmachine'
require 'faye'

Faye::Logging.log_level = :info
Faye.logger = lambda { |m| puts m }

EM.run do
  client = Faye::Client.new("http://localhost:1234/lumen")

  client.publish('/test', { :body => 'ya ho!'})
end

