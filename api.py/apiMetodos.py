import random
from paho.mqtt import client as mqtt_client
from datetime import *






#broker = 'broker.emqx.io'
broker = 'localhost'  
port = 1883

client_id =str(random.randint(0, 1000))
username = 'API'
password = 'public'
conexoesLista = []
listaAux = []
listaIDs = []

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Conectado com o broker")
        else:
            print("Falha na conexão\n", rc)

    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

client = connect_mqtt() 
   
def subscribeNhidrometros(client: mqtt_client):
    global conexoesLista
    global listaAux

    def on_message(client, userdata, msg):
        if(msg.payload.decode() != 'unsubscribe'):
            idHidro, litrosUtilizados, *temp = msg.payload.decode().split(',')    #a variável temp é aux para o demsempacotamento c o split
            print(idHidro, litrosUtilizados)      
            listaAux.append(idHidro)
            listaAux.append(float(litrosUtilizados))
            print('Id', idHidro, '\n Litros utilizados:', litrosUtilizados)
            conexoesLista.append(listaAux)
        else:
            client.unsubscribe('nHidrometros/')
            client.disconnect() #desconecta para encerrar a thread e obter o retorno
            print('Cancelando inscrição')

    client.on_message = on_message
    client.subscribe('nHidrometros/')
    return conexoesLista


def subscribeDebito(client: mqtt_client):
    global listaAux

    def on_message(client, userdata, msg):
        if(msg.payload.decode() != 'unsubscribe'):
            status = msg.payload.decode()   #a variável temp é aux para o demsempacotamento c o split               
            listaAux.append(status)            
        else:
            client.unsubscribe('debito/')
            client.disconnect() #desconecta para encerrar a thread e obter o retorno
            print('Cancelando inscrição')

    client.on_message = on_message
    client.subscribe('debito/')
    return listaAux

def enviaTetoMetodo(teto):
    result = client.publish("api/teto", str(teto))
    status = result[0]
    if status == 0:
        return 'Enviado com sucesso'
    else:
        return 'Falha no envio'


#n: é o número dr hidrômetros que você deseja receve
def nHidrometros(n):    
    result = client.publish("api/nHidrometros", str(n)) 
    status = result[0]
    if status == 0:
        print('Enviado com sucesso')
        resultado = subscribeDebito(client)
        client.loop_forever()
        return resultado
    else:
        return 'Falha no envio'


def verificaDebito(idConsultado, setorConsulta):
    result = client.publish("api/"+setorConsulta+ "/debito", str(idConsultado))
    status = result[0]
    if status == 0:
        print('Enviado com sucesso')
        resultado = subscribeDebito(client) #ainda fazer
        client.loop_forever()
        return resultado
    else:
        return 'Falha no envio'

def subscribeVazamento(client: mqtt_client):
    global listaIDs
    global listaAux

    def on_message(client, userdata, msg):
        if(msg.payload.decode() != 'unsubscribe'): #enquanto a mensasgem recebida é diferente de unsubscribe, significa que ainda há conteúdo
            idVazamento = msg.payload.decode()         
            listaAux.append(idVazamento) 
            listaIDs.append(listaAux)
            print(listaIDs)
        else:
            client.unsubscribe('vazando/')
            client.disconnect() #desconecta para encerrar a thread e obter o retorno
            print('Cancelando inscrição')

    client.on_message = on_message
    client.subscribe('vazando/')
    return listaIDs

#lista o vazamento de todo o projeto
def verificaVazamento():    
    result = client.publish("api/vazando", 'consulta') 
    status = result[0]
    if status == 0:
        print('Enviado com sucesso')
        resultado = subscribeVazamento(client)
        client.loop_forever()
        return resultado
    else:
        return 'Falha no envio'

#bloqueia o hidrômetro com base em sua ID
def bloqueiaHidrometro(id):
    mensagemBloqueio = 'bloquear/'+ str(id) 
    result = client.publish("bloqueio/api", mensagemBloqueio)
    status = result[0]
    if status == 0:
        return (id + 'bloqueado com sucesso!')
    else:
        return 'Falha no envio'
