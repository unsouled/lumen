require 'rubygems'
require 'eventmachine'
require 'faye'
require 'pp'

Faye::Logging.log_level = :debug
Faye.logger = lambda { |m| puts m }

EM.run do
  client = Faye::Client.new("http://localhost:8080/lumen")
  client.subscribe('/test') do |message|
    puts message
  end
end

