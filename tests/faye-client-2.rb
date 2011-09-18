require 'rubygems'
require 'eventmachine'
require 'faye'
require 'pp'

Faye::Logging.log_level = :debug
Faye.logger = lambda { |m| puts m }

EM.run do
  client = Faye::Client.new("http://localhost:9090")
#  client.subscribe('/test', false) do |message|
#    puts message
#  end
  client.handshake do
    client.connect do |m|
      puts m
      #client.subscribe('/test', false) do |message|
      #  puts message
      #end
    end
  end
end

