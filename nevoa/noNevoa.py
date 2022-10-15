import random
from paho.mqtt import client as mqtt_client
import time
import paho.mqtt.client as paho

#parâmetros de conexão com o broker
broker = 'broker.emqx.io'
port = 1883
#gerando o ID
client_id = str(random.randint(0, 100))
username = 'emqx'
password = 'public'
dado = [] #bd da nuvem
nHidrometros = 0
hidrometrosConectados = []
listaNevoa = []

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

def subscribe(client: mqtt_client): #se inscreve no tópico dos hidrometros
    def on_message(client, userdata, msg):        
        print(f"Recebendo do tópico `{msg.topic}`:")        
    client.subscribe("Hidrometros/#")          
    client.on_message = on_message
    
def publish(client): #envia para servidor ou para tópico da névoa    
    global dado    
    status = 0
    noNevoa = str(random.randint(1024,5000)) #gera id do nó
    topicoNo = 'NoNevoa/'+ noNevoa  #tópico que conecta com o servidor
    topicoNevoa = 'nevoa/'+ noNevoa #topico que conecta com os demais nós da nevoa
    global nHidrometros
    global hidrometrosConectados
   
    while True:
        nHidrometros = len(hidrometrosConectados) #atualizando a quantidade de hidrômetros conectaos        
        if nHidrometros == 0:
            print("Ainda não há hidrômetros conectados\n")
            result2 = client.publish(topicoNevoa, nHidrometros) #publica no tópico da rede névoa
        else:
            print("Atualizando lista de hidrômetros conectados\n")
            mensagem = str(noNevoa + ': ' + str(nHidrometros)) #essa nevoa possui x hidrômetros conectados                           
            result2 = client.publish(topicoNevoa, mensagem) #publica no tópico da rede névoa  
            nHidrometros = int(nHidrometros)          
        print('Enviando para o tópico da nevoa')
        for dado in dado:            
            info = dado
            info = str(info)
            result = client.publish( topicoNo, info) #enviando para o servidor central           
            # result: [0, 1]
            status = result[0]
        dado = []          # quando acaba de enviar, ele limpa a lista
        time.sleep(3)      #aqui é pra regular a quantidade de tempo que ele vai atualizar   
        if status == 0:
            print(f"Enviando para Servidor\n")
            time.sleep(6) #MUDAR PARA 30S NOVAMENTE
        else:
            print(f"Erro na rede. Mensagens não estão sendo enviadas para Servidor")   

def subscribe1(client: mqtt_client):
    global dado    
    global hidrometrosConectados
    global nHidrometros
    listaNevoa = []  
    def on_message(client, userdata, msg):           
        topico = msg.topic
        aux, id = topico.split('/')   #pegando qual é o tópico
        if aux == 'nevoa': #se for o tópico da névoa             
           print ('TÓPICO DA NEVOA')  
           mensagem = msg.payload.decode()           
           listaNevoa.append(mensagem)
           print('Nós: número de hidrômetros conectados')
           '''trabalhar essa lista para o balanceamento da névoa
                colocar: uma lista será a lista de nós na rede
                verificar se dentro dessa lista já lista já temos um valor
                se não, append, se sim, iremos atualizar o valor
                
                para o balanceamento:
                verificar se o meu número é o menor, se sim, continuo ouvindo e guardando as infos, se não, apenas escuto, não guardo as infos'''
           print(listaNevoa)
        else: #tópico dos hidrometros
            print('TÓPICO DO HIDRÔMETROS')
            idHidro = msg.topic
            aux, id = idHidro.split('/')   #pegando a id do hidrômetro
            if id not in hidrometrosConectados: #conferindo se já existe essa ID na lista
                hidrometrosConectados.append(id)                
                print('hidrometros conectados', nHidrometros , '\n')                  
            mensagem = msg.payload.decode()
            dado.append(mensagem)        
            listrosUtilizados, dataH, vazao, id, vaza, *temp = mensagem.split(',')    #a variável temp é aux para o demsempacotamento c o split        
            print('\nLitros utilizados: ' + listrosUtilizados)
            print('\nHorário/Data: ' + dataH)
            print('\nVazão atual: ' + vazao)
            print('\n ID:' + id)
            print('\n Situção de vazamento (0 para vazamento e 1 para não)'+ vaza , '\n')       
    client.subscribe("nevoa/#")     
    client.on_message = on_message

def run():
    client = connect_mqtt()
    client.loop_start()
    subscribe(client)
    subscribe1(client)    
    publish(client) 

if __name__ == '__main__':
    run()