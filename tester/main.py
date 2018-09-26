#!/usr/bin/python3

import sys
from tkinter import *
import paho.mqtt.client as mqtt
import yaml

with open("../configuration.yaml", 'r') as ymlfile:
    cfg = yaml.load(ymlfile)

if "mqtt" not in cfg or \
        "base_topic" not in cfg["mqtt"] or\
        "light_topic" not in cfg["mqtt"] or\
        "server" not in cfg["mqtt"]:
    print("Configuration file is invalid. Needs mqtt base_topic, light_topic and server")
    sys.exit(1)

window = Tk()
window.title("MQTT visualiser")
canvas = Frame(window, height=300, width=300)
canvas.pack()
color_label = Label(window, height=1, width=7, text="#")
color_label.pack()

def on_connect(client, userdata, flags, rc):
    print("Connected to mqtt broker with result code "+str(rc))

    client.subscribe(cfg["mqtt"]["light_topic"])


def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    color_label.configure(text=msg.payload)
    canvas.configure(background=msg.payload)


client = mqtt.Client()
if "user" in cfg["mqtt"] and "password" in cfg["mqtt"]:
    print("Set server user and password")
    client.username_pw_set(cfg["mqtt"]["user"], cfg["mqtt"]["password"])

client.on_connect = on_connect
client.on_message = on_message

client.connect(cfg["mqtt"]["server"])

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_start()


window.mainloop()
