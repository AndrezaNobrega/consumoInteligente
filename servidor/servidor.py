import random

from paho.mqtt import client as mqtt_client


broker = 'localhost'                                     #inicializar mosquitto através do cmd
port = 1883
topic = 'NoNevoa/#'

# generate client ID with pub prefix randomly
client_id = f'python-mqtt-{random.randint(0, 100)}'
username = 'emqx'
password = 'public'

#método para conexão ao mqtt
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

#método para inscrição ao tópico
def subscribe(client: mqtt_client):
    dado = []
    def on_message(client, userdata, msg):        
        mensagem = msg.payload.decode()            
        dado.append(mensagem)        
        listrosUtilizados, dataH, vazao, id, vaza, *temp = mensagem.split(',')    #a variável temp é aux para o demsempacotamento c o split        
        print('\nLitros utilizados: ' + listrosUtilizados)
        print('\nHorário/Data: ' + dataH)
        print('\nVazão atual: ' + vazao)
        print('\n ID:' + id)
        print('\n Situção de vazamento (0 para vazamento e 1 para não)'+ vaza) 

    client.subscribe(topic)
    client.on_message = on_message


def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()


if __name__ == '__main__':
    run()