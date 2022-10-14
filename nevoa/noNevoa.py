import random
from paho.mqtt import client as mqtt_client
import time


#parâmetros de conexão com o broker
broker = 'broker.emqx.io'
port = 1883
topic = "Hidrometros/#"  #recebendo todos os hidrômetros
#gerando o ID
client_id = f'python-mqtt-{random.randint(0, 100)}'
username = 'emqx'
password = 'public'

dado = []



def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Conectado ao broker com sucesso ")
        else:
            print("Erro na conexão %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def subscribe(client: mqtt_client):
    global dado
    hidrometrosConectados = [] #lista dos hidrometros conectados
    def on_message(client, userdata, msg):        
        print(f"Recebendo do tópico `{msg.topic}`:")
        idHidro = msg.topic
        aux, id = idHidro.split('/')   #pegando a id do hidrômetro
        if id not in hidrometrosConectados: #conferindo se já existe essa ID na lista
            hidrometrosConectados.append(id)  
            print('hidrometros conectados', hidrometrosConectados)   
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

def publish(client):
    global dado    
    status = 0
    hidrometroiD = str(random.randint(1024,5000))
    topicoNo = 'NoNevoa/'+ str(hidrometroiD)  
    while True:
        for dado in dado:            
            info = dado
            info = str(info)
            result = client.publish( topicoNo, info)
            # result: [0, 1]
            status = result[0]
        dado = []          # quando acaba de enviar, ele limpa a lista
        time.sleep(3)      #aqui é pra regular a quantidade de tempo que ele vai atualizar   
        if status == 0:
            print(f"Enviando para `{topic}`")
            time.sleep(30)
        else:
            print(f"Erro na rede. Mensagens não estão sendo enviadas para {topic}")
        


def run():
    client = connect_mqtt()
    client.loop_start()
    subscribe(client)
    publish(client) 

if __name__ == '__main__':
    run()