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
nHidrometros = 0 #número de hidrômetro conectados
noNevoa = str(random.randint(1024,5000)) #gera id do nó
hidrometrosConectados = [] #lista dos hidrômetros, contendo também a ID
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

#se inscreve no tópico que envia as conexões
def subscribe2(client: mqtt_client):
    def on_message(client, userdata, msg):
        print(f"Recebendo do tópico `{msg.topic}`:")
    client.subscribe("conexoes/#")
    client.on_message = on_message

    
def publish(client): #envia para servidor ou para tópico da névoa    
    global dado    
    status = 0
    global noNevoa
    topicoNo = 'NoNevoa/'+ noNevoa  #tópico que conecta com o servidor
    topicoNevoa = 'nevoa/'+ noNevoa #topico que conecta com os demais nós da nevoa
    global nHidrometros
    global hidrometrosConectados
   
    while True:
        nHidrometros = len(hidrometrosConectados) #atualizando a quantidade de hidrômetros conectaos        
        if nHidrometros == 0:
            print("Ainda não há hidrômetros conectados\n")
            mensagem = str(noNevoa + ': ' + str(nHidrometros)) #mesmo sem hidrometros, se conhece o id do nó em sua rede                         
            result2 = client.publish(topicoNevoa, mensagem) #publica no tópico da rede névoa  
            nHidrometros = int(nHidrometros)          
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
            time.sleep(30) #MUDAR PARA 30S NOVAMENTE
        else:
            print(f"Erro na rede. Mensagens não estão sendo enviadas para Servidor")   

def subscribe1(client: mqtt_client):
    global dado    
    global hidrometrosConectados
    global nHidrometros
    global listaNevoa    
    def on_message(client, userdata, msg):
        global noNevoa           
        topico = msg.topic
        aux, id = topico.split('/')   #pegando qual é o tópico
        if aux == 'nevoa': #se for o tópico da névoa             
           print ('TÓPICO DA NEVOA')  
           mensagem = msg.payload.decode()           
           if len(listaNevoa) != 0: #tratamento da lista de nós
                idNevoa, nConexoes = mensagem.split(':')
                indice = 0
                for no in listaNevoa:
                    id, numeroHidros = no.split(':')
                    if id == idNevoa: #verificamentos se já existe esse id na lista
                        listaNevoa.pop(indice) #se já existe, apagamos
                    indice =+ 1 #para pegar o indice que será deletado
                novoIndice = (idNevoa+ ':' + nConexoes)
                listaNevoa.append(novoIndice) #caso não exista, ele add. Se existe, ele apenas atualiza, visto que a informação antiga fora apagada
                print('lista atualizada', listaNevoa)
           else:                                
                listaNevoa.append(mensagem) #caso não exista, ele add. Se existe, ele apenas atualiza, visto que a informação antiga fora apagada
                print('lista atualizada', listaNevoa)           
        else: #tópico dos hidrometros
            print('TÓPICO DO HIDRÔMETROS')        
            idHidro = msg.topic
            aux, id = idHidro.split('/')   #pegando a id do hidrômetro
            if id not in hidrometrosConectados: #conferindo se já existe essa ID na lista
                if nHidrometros != 0: #se ja existem conectados
                    menorNumero = 15 #auxiliar para verificar se este é o nó com menor número de conexões
                    for no in listaNevoa: #percorre a lista
                        id, numeroHidros = no.split(':')
                        if str(noNevoa) != str(id) and numeroHidros < menorNumero: #menor numero diferente do atual
                            menorNumero = numeroHidros
                    if menorNumero < nHidrometros:
                        print('Nó com menor número de hidrômetros conectados. Add a esse nó o hidrômetro:', id)
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
                else:
                    print('Lista vazia, portanto add:',id )                    
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
            else:
                print('\nRecebendo do hidrometro já conectado:',id ) 
                mensagem = msg.payload.decode()
                dado.append(mensagem)        
                listrosUtilizados, dataH, vazao, id, vaza, *temp = mensagem.split(',')    #a variável temp é aux para o demsempacotamento c o split        
                print('\nLitros utilizados: ' + listrosUtilizados)
                print('\nHorário/Data: ' + dataH)
                print('\nVazão atual: ' + vazao)
                print('\n ID:' + id)
                print('\n Situção de vazamento (0 para vazamento e 1 para não)'+ vaza , '\n')  
            '''devemos enviar a lista completa, pois os outros nós precisam saber em quais nós os hidrômetros estão conectados
            para que assim não se conecte de novo com esse.'''

    client.subscribe("nevoa/#")     
    client.on_message = on_message

def run():
    client = connect_mqtt()
    client.loop_start()
    subscribe(client)
    subscribe1(client)
    subscribe2(client)     
    publish(client) 

if __name__ == '__main__':
    run()