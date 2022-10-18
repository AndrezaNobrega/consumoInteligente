import random
from paho.mqtt import client as mqtt_client
import time

#parâmetros de conexão com o broker
broker = 'broker.emqx.io'
port = 1883
username = 'emqx'
password = 'public'
#gerando o ID
client_id = str(random.randint(0, 100))
dado = [] #bd da nuvem
nHidrometros = 0
hidrometrosConectados = []
setorNevoa = str(input('Digite aqui o setor do seu nó: \n'))

#Conecta-se ao broker
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

'''Manipula mensagens recebidas pelo tópico dos hidrômetros'''
def recebeHidrometros(client, msg):
    idHidro = msg.topic
    print('Recebendo mensagem', msg.topic)
    aux, setorHidrometro ,  id = idHidro.split('/')   #pegando a id do hidrômetro
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
    return dado 

#inscreve-se no tópico do servidor e trata as mensagens, de acordo com o tópico que está sendo recebido
def subscribeServer(client: mqtt_client): 
    global dado    
    global hidrometrosConectados
    global nHidrometros
    listaNevoa = [] 
    def on_message(client, userdata, msg):
        topico = msg.topic        
        aux, setorHidrometro,  id = topico.split('/')   #pegando qual é o tópico
        if aux == 'nevoa': #se for o tópico da névoa             
           print ('TÓPICO DA NEVOA')  
           mensagem = msg.payload.decode()           
           listaNevoa.append(mensagem)
           print('Nós: número de hidrômetros conectados')
        else: #tópico dos hidrometros
            print('TÓPICO DO HIDRÔMETROS')
            dado = recebeHidrometros(client, msg)        
    client.subscribe("nevoa/#")          
    client.on_message = on_message

#envia para servidor ou para tópico da névoa       
def publish(client):
    global dado    
    status = 0
    noNevoa = str(random.randint(1024,5000)) #gera id do nó
    topicoNo = 'NoNevoa/'+ noNevoa  #tópico que conecta com o servidor
    topicoNevoa = 'nevoa/'+ noNevoa #será usado para enviar mensagens os hidrometros 
    while True:
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
            time.sleep(30) #MUDAR PARA 30S NOVAMENTE
        else:
            print(f"Erro na rede. Mensagens não estão sendo enviadas para Servidor")  


def subscribeHidrometros(client: mqtt_client): 
    def on_message(client, userdata, msg):           
        topico = msg.topic  
        print('Recebendo mensagem', msg.topic)  
    client.subscribe('Hidrometros/'+setorNevoa+'/#') 
    client.on_message = on_message 

def run():
    client = connect_mqtt()
    client.loop_start()   # type: ignore
    subscribeHidrometros(client)
    subscribeServer(client)    
    publish(client) 

if __name__ == '__main__':
    run()