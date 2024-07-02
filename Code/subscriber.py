import paho.mqtt.client as mqtt
from gpiozero import RGBLED
from colorzero import Color
import time

# This is the Subscriber with led & motor connected
led = RGBLED(18,23,24)
fan = LED(4)

def changeLedColor(color):
  try:
    led.setColor(color)
  except:
    print("Invalid color or action received")


def on_connect(client, userdata, flags, rc):
  print('Connected with result code '+str(rc))
  client.subscribe('test/topic')

def on_message(client, userdata, msg):
  decodedmsg = msg.payload.decode().lower() #add to this for led & motor with if statements and gpio
  splitMsg = decodedmsg.split(" ")
  hardware = splitMsg[0]
  action = splitMsg[1]
  if(hardware == "led"):
    print("Turning LED to "+ action + " state")
    if(action == "on"):
      led.on()
    elif(action == "off"):
      fan.off()
    else:
      print("Unrecognized motor action");

  elif(hardware == "motor"):
    print("Turning Motor to "+ action + " state")
    if(action == "on"):
      fan.on()
    elif(action == "off"):
      fan.off()
    else:
      print("Unrecognized motor action");

client = mqtt.Client()
client.connect('192.168.240.1',1883,60)
client.on_connect = on_connect
client.on_message = on_message

client.loop_forever()
