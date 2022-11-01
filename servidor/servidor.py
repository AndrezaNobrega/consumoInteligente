import random
import time
from paho.mqtt import client as mqtt_client
import pandas as pd


#broker = 'broker.emqx.io' broker público, se necessário
broker = 'localhost'
port = 1883
topic = 'NoNevoa/#'
client_id = str(random.randint(0, 100))
username = 'emqx'
password = 'public'
nosConectados = []
listaMedias = [] #médias dos hidrometros lista
listaAuxSetores = [] #lista dos setores conectados
conexoesLista = [] #lista dos hidrometros conectados

#quando a API enviar a requisição, ele vai retornar essas infos aqui
maiorGasto_DataFrame = []


#recebe como parâmetro a matriz do nó
#retornaDataFrame com última ocorrência de cada ID
def elencandoMaiorGasto(db):
    listaHidrometros = []
    unicaOcorencia = []
    aux = 0
    for hidrometro in db: #para criar uma lista com a última ocorrência daquele hidrômetro
        id = hidrometro[0]    
        if id not in listaHidrometros: 
            listaHidrometros.append(id)
            unicaOcorencia.append(hidrometro)
            print(listaHidrometros)            
            aux = listaHidrometros.index(id)
            time.sleep(0.1)
        else:
            aux = listaHidrometros.index(id)
            unicaOcorencia.pop(aux)
            unicaOcorencia.append(hidrometro) 
            listaHidrometros.pop(aux)
            listaHidrometros.append(id)  
            time.sleep(0.1)            
    tabelaDB =  pd.DataFrame(unicaOcorencia, columns= ['ID', 'Litros Utilizados']) #dataFrame com os hidrometros
    ordenado = tabelaDB.sort_values('Litros Utilizados', ascending=False)
    print('PRINT TABELA DE HIDRÔMETROS DE FORMA ORDENADA \n', ordenado)
    return tabelaDB

'''
 Conexão feita com o Broker
 '''
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
        print('Recebendo')
    client.subscribe(topic)
    client.on_message = on_message

def subscribeAPI(client: mqtt_client): 
    def on_message(client, userdata, msg):                  
        print('Recebendo..')
    client.subscribe('api/#') 
    client.on_message = on_message 

def maiorGasto(maiorGasto_DataFrame, client, n):
    contador = 0
    hidroAux = 0
    ordenado = maiorGasto_DataFrame.sort_values('Litros Utilizados', ascending=False)
    print('dataframe ordenado', ordenado)
    listaOrdenado = ordenado.values.tolist()
    if int(n) > len(listaOrdenado):        
        for hidro in listaOrdenado:
            if len(listaOrdenado)> contador:
                contador=+1
                print('ID:', hidro[0], 'Litros utilizados:', hidro[1])
                hidroAux = str(hidro[0])+ ',' + str(hidro[1]) + ',' #para facilitar a parte do envio
                client.publish("nHidrometros/", hidroAux)
            else:
                print('Cancelando inscrição')
                client.publish('nHidrometros/', 'unsubscribe') #se atingiu o número, cancelará a inscrição          

    for hidro in listaOrdenado:
        if contador != n:
            contador =+1
            print('ID:', hidro[0], 'Litros utilizados:', hidro[1])
            hidroAux = str(hidro[0])+ ',' + str(hidro[1]) + ',' #para facilitar a parte do envio
            client.publish("nHidrometros/", hidroAux)
        else:
            break
    print('Cancelando inscrição')
    client.publish('nHidrometros/', 'unsubscribe') #se atingiu o número, cancelará a inscrição
        
    

def subscribeGasto(client: mqtt_client):
    def on_message(client, userdata, msg):
        print(f"Recebendo do {msg.topic}`")
        global nosConectados
        global listaMedias
        global listaAuxSetores
        global conexoesLista
        global maiorGasto_DataFrame
        topico = msg.topic
        print (topico)                   
        *topico, assunto, setor = topico.split('/')   #pegando qual é o tópico
        if assunto == 'media': #quando recebe medias
            media = msg.payload.decode()  
            if setor not in listaAuxSetores:
                listaAuxSetores.append(setor)                
                mediaNo = float(media) 
                print('A média do setor', setor, 'é: ',mediaNo)
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
                                client.publish("server/geral/media", somatoriaMedias) #envia a media geral de todos os hidrômetros de volta para os nós
                                listaAuxSetores.clear() #para refazer a o ciclo
                                listaMedias.clear()
                              
        elif assunto == 'setor': #mensagem de inicialização do setor
            setorNo = msg.payload.decode()
            if setorNo not in nosConectados:
                nosConectados.append(setorNo)
                print(nosConectados)
        elif assunto == 'maiorOcorrencia':
            print('Recebendo hidrometros com maiores ocorrencias do setor:', setor)

        elif assunto == 'api':
            if setor == 'teto': #quando recebe requisição para enviar teto para todos os n
                teto = msg.payload.decode()
                print('O novo teto é:', teto)
                client.publish("server/geral/teto", teto) #envia a media geral de todos os hidrômetros de volta para os nós
            if setor == 'nHidrometros':  #requisição de N hidrometros
                nHidrometros = msg.payload.decode() 
                print(nHidrometros) #aqui vamos verificar quantos hidrômetros são 
                maiorGasto(maiorGasto_DataFrame, client, nHidrometros) #tratamento
                

        elif assunto == 'maisGasto': 
            listaAux = [] #lista que será utilizada quando receber o hidrômetros mais gastos
            mensagem = msg.payload.decode()    
            print('Mais gasto manipulação')        
            print('MENSAGEM RECEBIDA', mensagem)
            idHidro, litrosUtilizados, *temp = mensagem.split(',')    #a variável temp é aux para o demsempacotamento c o split            
            listaAux.append(idHidro)
            listaAux.append(float(litrosUtilizados))
            print('Id', idHidro, '\n Litros utilizados:', litrosUtilizados)
            conexoesLista.append(listaAux)
            maiorGasto_DataFrame = elencandoMaiorGasto(conexoesLista) #sempre que recebo uma nova lista, esta df eh atualizado
            print('Recebendo lista com hidrômetros com mais gasto')                
    client.subscribe('maisGasto/Hidrometros')
    client.on_message = on_message

def publish(client):
    global dado 
    status = 0
    topicoServer = "server/geral/media"  #tópico que conecta com o servidor    
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
    subscribeGasto(client)       
    publish(client) 


if __name__ == '__main__':
    run()