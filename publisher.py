import paho.mqtt.client as mqtt

# This is the Publisher

client = mqtt.Client()
client.connect('192.168.240.1',1883,60)
client.publish('test/topic', 'Hello world!');
