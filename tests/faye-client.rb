require 'rubygems'
require 'eventmachine'
require 'faye'

Faye::Logging.log_level = :info
Faye.logger = lambda { |m| puts m }

EM.run do
  client = Faye::Client.new("http://localhost:8080/lumen")

  client.publish('/test', { :message => 'ya ho!'})
end

