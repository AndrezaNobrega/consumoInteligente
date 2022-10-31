import random
import time
from paho.mqtt import client as mqtt_client
import time
import hidrometro
import datetime

# parametros broker
'''broker = 'broker.emqx.io'''
username = 'emqx'
password = 'public'''
broker = 'localhost'                        #inicializar mosquitto através do cmd
port = 1883


#gerando ID
hidrometroiD = str(random.randint(1024,5000))
setor = str(input('Digite o setor do seu hidrometro:'))
topic = 'Hidrometros/'+ setor+'/'+ str(hidrometroiD) 

#variáveis p inicialização do hidrômetro
litroConsumidos = 0
status = False
pressao = 1 #aqui é a pressão que está sendo exercida no hidrometro
hidrometro1 = hidrometro.Hidrometro(hidrometroiD, setor) #cria objeto
vazao = 0 #inicializando variável
pressao = str(random.randint(0,9)) #fica sendo gerado um valor entre 0 e 10, caso esse valor seja zero, significa que há algum problema nos canos

'''Ao inicializar o hidrometro, precisamos inserir se ele terá um alto, baixo ou médio grau de gasto, a partir daí será gerado pelo próprio hidrometro
com base na sua faixa de gasto'''
grau = input('Digite o grau do gasto para o hidrometro:\n [1] para baixo \n [2] para médio \n [3] para alto \n Digite aqui:')

def getData():
        data = datetime.datetime.now() #pega o horário atual
        dataAux = str(data) #convertendo horário para string
        dataAux= dataAux[:16] #recortando horas e segundos da String
        return dataAux

def vazamento(pressao):    
    if pressao == 0:
        return '0' #significa que está ocorrendo um vazamento
    else:
        return '1' #não há vazamento

'''Método que ao inicializar o hidrometro, pode ser inicializado com muito, pouco ou médio gasto'''
def geraVazao(grau):
    if grau == '1':
        return random.randint(1,10)
    elif grau == '2':
        return random.randint(11,25)
    elif grau == '3':
        return random.randint(25,50)

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

'''Primeiro, definimos um loop de tempo.
Neste loop, e definimos a função cliente MQTT para enviar mensagens para o tópico a cada segundo'''
def publish(client):
    global litroConsumidos
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

def run():
    client = connect_mqtt()
    client.loop_start()
    subscribe(client)        
    publish(client) 

if __name__ == '__main__':
    run()