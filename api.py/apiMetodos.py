import random
from paho.mqtt import client as mqtt_client
from datetime import *

#broker = 'broker.emqx.io'
broker = 'localhost'  
port = 1883

client_id =str(random.randint(0, 1000))
username = 'emqx'
password = 'public'
conexoesLista = []
listaAux = []

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Conectado com o broker")
        else:
            print("Falha na conexão\n", rc)

    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

client = connect_mqtt() 
   
def subscribeNhidrometros(client: mqtt_client):
    global conexoesLista
    global listaAux

    def on_message(client, userdata, msg):
        if(msg.payload.decode() != 'unsubscribe'):
            idHidro, litrosUtilizados, *temp = msg.payload.decode().split(',')    #a variável temp é aux para o demsempacotamento c o split
            print(idHidro, litrosUtilizados)      
            listaAux.append(idHidro)
            listaAux.append(float(litrosUtilizados))
            print('Id', idHidro, '\n Litros utilizados:', litrosUtilizados)
            conexoesLista.append(listaAux)
        else:
            client.unsubscribe('nHidrometros/')
            client.disconnect()
            print('Cancelando inscrição')

    client.on_message = on_message
    client.subscribe('nHidrometros/')
    return conexoesLista

    
def enviaTetoMetodo(teto):
    result = client.publish("api/teto", str(teto))
    status = result[0]
    if status == 0:
        return 'Enviado com sucesso'
    else:
        return 'Falha no envio'


#n: é o número dr hidrômetros que você deseja receve
def nHidrometros(n):    
    result = client.publish("api/nHidrometros", str(n)) 
    status = result[0]
    if status == 0:
        print('Enviado com sucesso')
        resultado = subscribeNhidrometros(client)
        client.loop_forever()
        return resultado
    else:
        return 'Falha no envio'

def verificaDebito(idConsultado, setor):
    result = client.publish("api/"+setor "/"+debito, str(idConsultado))
    status = result[0]
    if status == 0:
        print('Enviado com sucesso')
        #resultado = subscribeDebito(client) #ainda fazer
        client.loop_forever()
        #return resultado
    else:
        return 'Falha no envio'