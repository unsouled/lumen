require 'rubygems'
require 'eventmachine'
require 'faye'
require 'pp'

Faye::Logging.log_level = :info
Faye.logger = lambda { |m| puts m }

EM.run do
  client = Faye::Client.new("http://localhost:8080/lumen")
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

