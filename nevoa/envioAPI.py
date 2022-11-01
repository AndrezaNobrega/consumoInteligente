import random
import time
from paho.mqtt import client as mqtt_client
import time
import hidrometro
import datetime

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Conexão estabelecida com o broker com sucesso")
        else:
            print("Erro na conexão %d\n", rc)

    client = mqtt_client.Client(hidrometroiD)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def publish(client):
    vaza = 0
    id = str(hidrometro1.getId()) 
    global pressao
    global vazao
    global status
    global grau  
    global topic  
    while True:
        if status == False:            
            vazao = geraVazao(grau)                       
            data = getData() #pegando o momento da consumo        
            print('A vazão atual é de:', vazao) 
            litroConsumidos = int(litroConsumidos + vazao)
            print('Temos', litroConsumidos, 'L consumidos')  
            litroConsumidos = str(litroConsumidos)
            vazao = str(vazao)
            pressao = str(random.randint(0,9)) #gerando uma pressão 
            vaza = vazamento(pressao)
            infoHidro = litroConsumidos + ',' + data + ',' +vazao+ ',' +id+ ',' +vaza+ ','
            print('___________','Enviando para a névoa','_______________________________') 
            result = client.publish(topic, infoHidro)
            print(hidrometroiD)
            litroConsumidos = int(litroConsumidos)
            vazao = int(vazao)          
            # result: [0, 1]
            statusEnvio = result[0]
            time.sleep(2)
        else:
            print('*'*40)
            print('*'*40)
            print('Seu hidrometro está bloqueado, realize o pagamento.')
            vazao = 0
            print('*'*40)
            print('*'*40) 
            time.sleep(2)              
            data = getData() #pegando o momento da consumo        
            print('A vazão atual é de:', vazao) 
            litroConsumidos = int(litroConsumidos + vazao)
            print('Temos', litroConsumidos, 'L consumidos')  
            litroConsumidos = str(litroConsumidos)
            vazao = str(vazao)
            pressao = str(random.randint(0,9)) #gerando pressao 
            vaza = vazamento(pressao)
            infoHidro = litroConsumidos + ',' + data + ',' +vazao+ ',' +id+ ',' +vaza+ ','
            print('Enviando para a névoa')
            result = client.publish(topic, infoHidro)
            statusEnvio = result[0]
            print('___________','Enviando para a névoa','_______________________________')  
            print ('\n ID:', id ,'\nLitros utilizados:', litroConsumidos, '\nData do envio:', data, '\nVazão atual:',vazao) #visualização do envio
            print('______________________________________________________________________')                                
            litroConsumidos = int(litroConsumidos)
            vazao = int(vazao)                
            time.sleep(2)            
            statusEnvio = result[0]                   
        if statusEnvio == 0: #caso esteja enviando
            if status == False:                
                vazao = geraVazao(grau)                           
                data = getData() #pegando o momento da consumo        
                print('A vazão atual é de:', vazao) 
                litroConsumidos = int(litroConsumidos + vazao)
                print('Temos', litroConsumidos, 'L consumidos')  
                litroConsumidos = str(litroConsumidos)
                vazao = str(vazao) 
                vaza = vazamento(pressao)
                infoHidro = litroConsumidos + ',' + data + ',' +vazao+ ',' +id+ ',' +vaza+ ','
                print('Enviando para a névoa')
                result = client.publish(topic, infoHidro) #tópico ta aqui
                statusEnvio = result[0]
                print('___________','Enviando para a névoa','_______________________________') 
                print ('\n ID:', id ,'\nLitros utilizados:', litroConsumidos, '\nData do envio:', data, '\nVazão atual:',vazao) #visualização do envio
                print('______________________________________________________________________')                                
                litroConsumidos = int(litroConsumidos)
                vazao = int(vazao)                
                time.sleep(2)
            else:
                print('*'*40)
                print('*'*40)
                print('Seu hidrometro está bloqueado, realize o pagamento.')
                vazao = 0
                print('*'*40)   
                print('*'*40)            
                data = getData() #pegando o momento da consumo        
                print('A vazão atual é de:', vazao) 
                litroConsumidos = int(litroConsumidos + vazao)
                print('Temos', litroConsumidos, 'L consumidos')  
                litroConsumidos = str(litroConsumidos)
                vazao = str(vazao) 
                vaza = vazamento(pressao)
                infoHidro = litroConsumidos + ',' + data + ',' +vazao+ ',' +id+ ',' +vaza+ ','
                print('___________','Enviando para a névoa','_______________________________')                 
                result = client.publish(topic, infoHidro)
                statusEnvio = result[0]                
                print ('\n ID:', id ,'\nLitros utilizados:', litroConsumidos, '\nData do envio:', data, '\nVazão atual:',vazao) #visualização do envio
                print('______________________________________________________________________')                                
                litroConsumidos = int(litroConsumidos)
                vazao = int(vazao)                
                time.sleep(2)                  
        else: #não está enviando
            print(f"ERRO FALHA NO ENVIO PARA: {topic}")
            print('Consulte sua rede')


#hidrometro pode ser bloqueado/desbloqeuado
def subscribe(client: mqtt_client):   
    def on_message(client, userdata, msg):        
        global hidrometroiD, setor, status, vazao
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
        topico = msg.topic
        topico, setor = topico.split('/')
        mensagem = msg.payload.decode()
        acao, id = mensagem.split('/')
        if id == hidrometroiD: #verifica se a mensagem de bloqueio é para este hidrômetro
            if acao == 'bloquear':
                status = True
                vazao = 0
                print('*'*40)   
                print('*'*40)
                print('Seu hidrometros foi bloqueado.')
                print('*'*40)   
                print('*'*40)
            elif acao == 'desbloquear':
                status = False
                print('*'*40)   
                print('*'*40)
                print('Seu hidrometro foi desbloqueado')
                print('*'*40)   
                print('*'*40)
                print(mensagem) #teste
    client.subscribe("bloqueio/"+ setor)
    client.on_message = on_message


