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
noNevoa = str(random.randint(50, 100)) #gera id do nó
hidrometrosConectados = [] #lista de hidrometros conectados ness
conexoes = [] #conexoes
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

def subscribe2(client: mqtt_client): #se inscreve no tópico dos hidrometros
    def on_message(client, userdata, msg):  
        global nHidrometros
        global conexoes
        topicoConexoes = 'conexoes/' + noNevoa #tópico que irá informar quais os hidrômetros já conectados          
        topico = msg.topic   
        aux, id = topico.split('/')   #pegando qual é o tópico
        if aux == 'nevoa': #se for o tópico da névoa
            print('\n') 
            print('='*10)               
            print ('TÓPICO DA NEVOA')
            print('\n') 
            print('='*10)   
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
                print('lista de conexões',listaNevoa)               
            else:                                
                listaNevoa.append(mensagem) #caso não exista, ele add. Se existe, ele apenas atualiza, visto que a informação antiga fora apagada
                print('lista atualizada', listaNevoa)                  
        elif aux == 'Hidrometros': #se for o tópico dos hidrômetros  
            print('\n') 
            print('='*10) 
            print('TÓPICO DO HIDRÔMETROS')
            print('\n') 
            print('='*10)         
            idHidro = msg.topic
            aux, id = idHidro.split('/')   #pegando a id do hidrômetro            
            nHidrometros = len(hidrometrosConectados) #atualizando a quantidade de hidrômetros conectaos 
            print('conexoessssssssssssssssss' ,nHidrometros)
            if id not in hidrometrosConectados: #conferindo se já existe essa ID na lista                              
                if id not in conexoes: #verificando se a conexão já não foi feita com outro nó
                    print(id)
                    if nHidrometros != 0: #se ja existem conectados
                        menorNumero = 15 #auxiliar para verificar se este é o nó com menor número de conexões
                        for no in listaNevoa: #percorre a lista
                            id, numeroHidros = no.split(':')
                            if str(noNevoa) != str(id) and str(menorNumero) > str(numeroHidros): #menor numero diferente do atual                            
                                menorNumero = numeroHidros
                        if str(menorNumero) == str(nHidrometros): #verifica se o menor numero de conexões é o deste nó
                            print('Nó com menor número de hidrômetros conectados. Add a esse nó o hidrômetro:', id)
                            hidrometrosConectados.append(id)     #add a lista do nó - a lista de hidrometros conectados           
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
                        hidrometrosConectados.append(id)    #add a lista do nó - a lista de hidrometros conectados           
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
            result2 = client.publish(topicoConexoes, id) #publica na rede névoa toda vez que recebe mensagem dos hidrometros
            #aqui vamos atualizar a lista de hidrômetros conectados ao nó 
            result2 = client.publish(topicoConexoes, id) #publica na rede névoa toda vez que recebe mensagem dos hidrometros
            topicoNevoa = 'nevoa/'+ noNevoa #topico que envia lista com número para demais nós     
            print(f"Recebendo do tópico `{msg.topic}`:")
            nHidrometros = len(hidrometrosConectados) #atualizando a quantidade de hidrômetros conectaos  
            print(nHidrometros, hidrometrosConectados)
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
        else:            
            print('\n') 
            print('='*10) 
            print('TÓPICO CONEXÕES')
            mensagem = msg.payload.decode()                         
            if mensagem not in conexoes:
                conexoes.append(mensagem) 
                print('Novo hidrometro conectado a rede:', mensagem)
                print('lista de hidrometros conectados na rede:', conexoes)   
            else:
                print('recebendo mensagem de hidrometro já na rede')  #isso é pra teste    
            print('='*10) 
            print('\n')          
    client.subscribe("conexoes/#")          
    client.on_message = on_message

def publish(client): #envia para servidor 
    global dado    
    status = 0
    global noNevoa
    topicoNo = 'NoNevoa/'+ noNevoa  #tópico que conecta com o servidor      
    while True:
        for dado in dado: #envio de informações dos hidroômetros para o servidor central       
            info = dado
            info = str(info)
            result = client.publish( topicoNo, info) #enviando para o servidor central           
            # result: [0, 1]
            status = result[0]
        dado = []          # quando acaba de enviar, ele limpa a lista
        time.sleep(3)      #aqui é pra regular a quantidade de tempo que ele vai atualizar   
        if status == 0: #se ele está recebendo callback
            print(f"Enviando para Servidor\n")
            time.sleep(30) #de 30 em 30 segundo, enviamos as informações para o servidor
        else:
            print(f"Erro na rede. Mensagens não estão sendo enviadas para Servidor")   

def subscribe1(client: mqtt_client):
    def on_message(client, userdata, msg):
        print('tópico nevoa')
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