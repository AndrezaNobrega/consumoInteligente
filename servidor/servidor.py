import random
import time

from paho.mqtt import client as mqtt_client



broker = 'localhost'                                     #inicializar mosquitto através do cmd
port = 1883
topic = 'NoNevoa/#'

# generate client ID with pub prefix randomly
client_id = f'python-mqtt-{random.randint(0, 100)}'
username = 'emqx'
password = 'public'
nosConectados = []
listaMedias = []
listaAuxSetores = []

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
    def on_message(client, userdata, msg):
        global nosConectados
        global listaMedias
        global listaAuxSetores
        topico = msg.topic
        print (topico)                   
        *topico, assunto, setor = topico.split('/')   #pegando qual é o tópico
        if assunto == 'media': #quando recebe medias
            media = msg.payload.decode()  
            if setor not in listaAuxSetores:
                listaAuxSetores.append(setor)                
                mediaNo = float(media) 
                print(mediaNo)
                listaMedias.append(mediaNo)
                if listaAuxSetores == nosConectados: #aqui verifica se todos os nós inicializados já enviaram suas médias
                                print('Enviando media geral para hidrometros')
                                numeroSetores = len(nosConectados)
                                somatoriaMedias = 0
                                for media in listaMedias:
                                    somatoriaMedias+= media
                                    print(somatoriaMedias)
                                somatoriaMedias = somatoriaMedias/numeroSetores #aqui para tirarmos a media
                                print('MEDIA GERAL:', somatoriaMedias)
                                client.publish("server/media/geral", somatoriaMedias) #envia a media geral de todos os hidrômetros de volta para os nós
                                listaAuxSetores.clear()
                              
        elif assunto == 'setor': #mensagem de inicialização do setor
            setorNo = msg.payload.decode()
            if setorNo not in nosConectados:
                nosConectados.append(setorNo)
                print(nosConectados)
        elif assunto == 'maiorOcorrencia':
            print('Recebendo hidrometros com maiores ocorrencias do setor:', setor)
    client.subscribe(topic)
    client.on_message = on_message

def publish(client):
    global dado 
    status = 0
    topicoServer = "server/media/geral"  #tópico que conecta com o servidor    
    while True:        
        time.sleep(4)      #aqui é pra regular a quantidade de tempo que ele vai atualizar         
        if status == 0:
            #client.publish(topicoServer, '6') #envia a média desse nó
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