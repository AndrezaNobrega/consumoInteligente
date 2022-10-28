import random
import time

from paho.mqtt import client as mqtt_client


#broker = 'broker.emqx.io'
broker = 'localhost'  
port = 1883

client_id = random.randint(0, 1000)
username = 'emqx'
password = 'public'

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

client = connect_mqtt()   
def enviaTeto():         
    teto = input('Digite aqui o teto de gastos que deseja estabelecer')
    result = client.publish("api/teto", str(teto))

enviaTeto()