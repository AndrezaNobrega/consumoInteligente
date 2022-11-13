import random
from paho.mqtt import client as mqtt_client
from datetime import *

#broker = 'broker.emqx.io'
broker = 'localhost' #ip do broker
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

 #se inscreve e manipula informações recebidas pelo tópico de nHidrometros/ o qual retorna os n hidrômetros mais utilizados com seus respectivos consumos  
def subscribeNhidrometros(client: mqtt_client):
    global conexoesLista
    global listaAux
    def on_message(client, userdata, msg):
        if(msg.payload.decode() != 'unsubscribe'):
            idHidro, litrosUtilizados, *temp = msg.payload.decode().split(',')    #a variável temp é aux para o demsempacotamento c o split
            print(idHidro, litrosUtilizados)      
            listaAux.append('ID:'+idHidro)
            listaAux.append('Litros Utilizados:'+litrosUtilizados)
            print('Id', idHidro, '\n Litros utilizados:', litrosUtilizados)
            conexoesLista.append(listaAux)
        else:
            client.unsubscribe('nHidrometros/')
            client.disconnect() #desconecta para encerrar a thread e obter o retorno
            print('Cancelando inscrição')

    client.on_message = on_message
    client.subscribe('nHidrometros/')
    return conexoesLista

#se inscreve e manipula informações recebidas pelo tópico debito
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

#envia um novo teto de gastos para o servidor central
def enviaTetoMetodo(teto):
    client = connect_mqtt() 
    result = client.publish("api/teto", str(teto))
    status = result[0]
    if status == 0:
        return 'Enviado com sucesso'
    else:
        return 'Falha no envio'

#Envia para o servidor central
#método retorna os n hidrômetros com o maior consumo
#n: é o número dr hidrômetros que você deseja receber
def nHidrometros(n): 
    listaAux.clear()
    client = connect_mqtt()    
    result = client.publish("api/nHidrometros", str(n)) 
    status = result[0]
    if status == 0:
        print('Enviado com sucesso')
        resultado = subscribeNhidrometros(client)
        client.loop_forever()
        return resultado
    else:
        return 'Falha no envio'

#Envia para o nó responsábel pelo hidrômetro
#verifica se hidrômetro específico está em débito
def verificaDebito(idConsultado, setorConsulta):
    listaAux.clear()
    client = connect_mqtt() 
    result = client.publish("api/"+setorConsulta+ "/debito", str(idConsultado))
    status = result[0]
    if status == 0:
        print('Enviado com sucesso')
        resultado = subscribeDebito(client) #chama o método que se inscreve no tópico
        client.loop_forever()
        return resultado
    else:
        return 'Falha no envio'

#se inscreve e manipula informações recebidas
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

#Envia para o servidor central
#lista o vazamento de todo o projeto
def verificaVazamento():  
    listaAux.clear()
    client = connect_mqtt()   
    result = client.publish("api/vazando", 'consulta') 
    status = result[0]
    if status == 0:
        print('Enviado com sucesso')
        resultado = subscribeVazamento(client)
        client.loop_forever()
        return resultado
    else:
        return 'Falha no envio'

#Envia mensagem para o hidrômetro específico
#bloqueia o hidrômetro com base em sua ID
def bloqueiaHidrometro(id):
    listaAux.clear()
    client = connect_mqtt() 
    mensagemBloqueio = 'bloquear/'+ str(id) 
    result = client.publish("bloqueio/api", mensagemBloqueio)
    status = result[0]
    if status == 0:
        return (id + 'bloqueado com sucesso!')
    else:
        return 'Falha no envio'


#se inscreve e manipula mensagem recebidas pelo tópico de histórico
def subscribeHistorico(client: mqtt_client):
    global listaAux

    def on_message(client, userdata, msg):
        if(msg.payload.decode() != 'unsubscribe'):
            horario, vazao, litrosUtilizads, *temp = msg.payload.decode().split(';')    #a variável temp é aux para o demsempacotamento c o split     
            listaAux.append('litros utilizados:'+horario)
            listaAux.append('horario:'+vazao)
            listaAux.append('vazao:'+litrosUtilizads)
            print(horario, vazao, litrosUtilizads)
            
            conexoesLista.append(listaAux)           
        else:
            client.unsubscribe('historico/')
            client.disconnect() #desconecta para encerrar a thread e obter o retorno
            print('Cancelando inscrição')

    client.on_message = on_message
    client.subscribe('historico/')
    return listaAux

#Envia para o setor responsável    
#verifica o histórico de um hidrômetro específico
# idConsultado: é necessário informar o seu id
# setorConsulta: é necessário informar o setor que será consultado
def verificaHistorico(idConsultado, setorConsulta):
    listaAux.clear()
    client = connect_mqtt() 
    result = client.publish("api/"+setorConsulta+ "/historico", str(idConsultado))
    status = result[0]
    if status == 0:
        print('Enviado com sucesso')
        resultado = subscribeHistorico(client) #ainda fazer
        client.loop_forever()
        return resultado
    else:
        return 'Falha no envio'


#se inscreve e manipula informações recebidas pelo tópico valorConta
def subscribeValorConta(client: mqtt_client):
    global listaAux

    def on_message(client, userdata, msg):
        if(msg.payload.decode() != 'unsubscribe'):
            status = msg.payload.decode()   #a variável temp é aux para o demsempacotamento c o split               
            listaAux.append(status)            
        else:
            client.unsubscribe('valorConta/')
            client.disconnect() #desconecta para encerrar a thread e obter o retorno
            print('Cancelando inscrição')

    client.on_message = on_message
    client.subscribe('valorConta/')
    return listaAux

#Envia para o setor responsável
#verifica se hidrômetro específico está em débito
def verificaValorConta(idConsultado, setorConsulta):
    listaAux.clear()
    client = connect_mqtt() 
    result = client.publish("api/"+setorConsulta+ "/valorConta", str(idConsultado))
    status = result[0]
    if status == 0:
        print('Enviado com sucesso')
        resultado = subscribeValorConta(client) #chama o método que se inscreve no tópico
        client.loop_forever()
        return resultado
    else:
        return 'Falha no envio'

#se inscreve e manipula informações recebidas pelo tópico consumo
def subscribeConsumo(client: mqtt_client):
    global listaAux

    def on_message(client, userdata, msg):        
        if(msg.payload.decode() != 'unsubscribe'):
            status = msg.payload.decode()   #a variável temp é aux para o demsempacotamento c o split     
            print(status)          
            listaAux.append(status)            
        else:
            client.unsubscribe('consumo/')
            client.disconnect() #desconecta para encerrar a thread e obter o retorno
            print('Cancelando inscrição')

    client.on_message = on_message
    client.subscribe('consumo/')
    return listaAux

#Envia para o setor responsável pelo nó
#verifica o total de litros consumidos de um hidrômetro específico
def verificaConsumo(idConsultado, setorConsulta):
    listaAux.clear()
    client = connect_mqtt() 
    result = client.publish("api/"+setorConsulta+ "/consumo", str(idConsultado))
    status = result[0]
    if status == 0:
        print('Enviado com sucesso')
        resultado = subscribeConsumo(client) #chama o método que se inscreve no tópico
        client.loop_forever()
        return resultado
    else:
        return 'Falha no envio'

#Esse faz o envio para o hidrômetro e para o nó responsável 
#desbloqueia o hidrômetro com base em sua ID, também, muda a data de pagamento
def desbloqueiaHidrometro(id, setorConsulta):
    listaAux.clear()
    client = connect_mqtt() 
    mensagemBloqueio = 'desbloquear/'+ str(id)  #envia mensagem de desbloqueio
    result = client.publish("bloqueio/api", mensagemBloqueio)

    data = datetime.now() + timedelta(minutes= 10) #hora que será o próximo pagamento
    dataAux = str(data) #convertendo horário para string
    dataAux= dataAux[:16] #recortando horas e segundos da String

    mensagemPagamento = id +';' + dataAux
    result = client.publish("api/"+setorConsulta+ "/pagamento", mensagemPagamento) #envia novo momento de pagamento para o bd
    status = result[0]
    if status == 0:
        return (id + 'desbloqueado com sucesso!')
    else:
        return 'Falha no envio'
