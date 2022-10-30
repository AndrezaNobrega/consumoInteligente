import random
import time
from paho.mqtt import client as mqtt_client
#broker = 'broker.emqx.io'
broker = 'localhost'  
port = 1883

client_id =str(random.randint(0, 1000))
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

def enviaTetoMetodo(teto):
    result = client.publish("api/teto", str(teto))
    status = result[0]
    if status == 0:
        return 'Enviado com sucesso'
    else:
        return 'Falha no envio'

def subscribe(client: mqtt_client, setor, hidrometroID):
    def on_message(client, userdata, msg):
        mensagem = msg.payload.decode() 
        listrosUtilizados, dataH, vazao, id, vaza, *temp = mensagem.split(',')    #a variável temp é aux para o demsempacotamento c o split
        print('horário', dataH)
        print('Consumo', listrosUtilizados)        
        time.sleep(2) 
    client.subscribe('Hidrometros/'+ setor + '/'+ hidrometroID)
    client.on_message = on_message




subscribe(client, '2', '4696')
client.loop_forever()