import random
import time
from paho.mqtt import client as mqtt_client

#broker = 'broker.emqx.io' broker público, se necessário
broker = 'localhost'
port = 1883
topic = 'NoNevoa/#'
client_id = str(random.randint(0, 100))
username = 'emqx'
password = 'public'
nosConectados = []
listaMedias = []
listaAuxSetores = []



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


def subscribeNevoa(client: mqtt_client):
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
                                listaAuxSetores.clear() #reiniciando para lista 
                                nosConectados.clear() #reiniciando lista
                              
        elif assunto == 'setor': #mensagem de inicialização do setor
            setorNo = msg.payload.decode()
            if setorNo not in nosConectados:
                nosConectados.append(setorNo)
                print(nosConectados)
        elif assunto == 'maiorOcorrencia':
            print('Recebendo hidrometros com maiores ocorrencias do setor:', setor)
    client.subscribe(topic)
    client.on_message = on_message

    def on_message2(client, userdata, msg):           
        topico = msg.topic  
        print('Recebendo mensagem', msg.topic)  
        print(msg.payload.decode())
    client.subscribe('api/#') 
    client.on_message = on_message2 

def subscribeAPI(client: mqtt_client): 
    def on_message(client, userdata, msg):           
        topico = msg.topic  
        print('Recebendo mensagem', msg.topic) 
        print(msg.payload.decode())
    client.subscribe('api/#') 
    client.on_message = on_message 

def publish(client):
    global dado 
    status = 0
    topicoServer = "server/media/geral"  #tópico que conecta com o servidor    
    while True:        
        time.sleep(4)      #aqui é pra regular a quantidade de tempo que ele vai atualizar         
        if status == 0:
            #client.publish(topicoServer, '6') #envia a média desse nó
            print(f"Enviando....\n")
            time.sleep(3) #colocar um tempo maior
        else:
            print(f"Erro na rede. Mensagens não estão sendo enviadas para a névoa")  


def run():
    client = connect_mqtt()
    client.loop_start()
    subscribeNevoa(client) 
    subscribeAPI(client)       
    publish(client) 


if __name__ == '__main__':
    run()