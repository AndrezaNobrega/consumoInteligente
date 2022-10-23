import random
import time

from paho.mqtt import client as mqtt_client


broker = 'broker.emqx.io'
port = 1883
topic = 'NoNevoa/#'
client_id = str(random.randint(0, 100))
username = 'emqx'
password = 'public'
dado = []


def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Conectado ao broker")
        else:
            print("Não foi possível se conectar ao broker, verifique sua conexão com a internet", rc)

    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        global dado        
        mensagem = msg.payload.decode()            
        dado.append(mensagem) 
        print(mensagem)
    client.subscribe(topic)
    client.on_message = on_message

def publish(client):
    global dado 
    status = 0
    topicoServer = "server/media/geral"  #tópico que conecta com o servidor    
    while True:
        print('-'*10)
        print('-'*10)
        time.sleep(4)      #aqui é pra regular a quantidade de tempo que ele vai atualizar         
        if status == 0:
            client.publish(topicoServer, '6') #envia a média desse nó
            print(f"Enviando para Servidor\n")
            time.sleep(3) #colocar um tempo maior
        else:
            print(f"Erro na rede. Mensagens não estão sendo enviadas para Servidor")  


def run():
    client = connect_mqtt()
    client.loop_start()
    subscribe(client)        
    publish(client) 


if __name__ == '__main__':
    run()