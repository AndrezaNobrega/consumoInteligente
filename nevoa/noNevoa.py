import random
from paho.mqtt import client as mqtt_client
import time
import pandas as pd
from datetime import datetime, timedelta




#import manipularBanco

#parâmetros de conexão com o broker
'''broker = 'broker.emqx.io''' #broker público
broker = 'localhost'
port = 1883
username = 'NoNevoa'   #172.16.103.14
password = 'public'

global setorNevoa

#gerando o ID
client_id = str(random.randint(0, 100))
dado = [] #bd da nuvem
nHidrometros = 0
hidrometrosConectados = []
tetoGasto = 0 #deve ser modificado pela API
listaHidrometrosBloqueados = [] #hidrometros bloqueados por ultrapassarem a média geral
listaPagamentos = [] #lista com o momento de pagamentos para cada hidrômetro
listaTeto = [] #lista de hidrômetros que foram bloqueado por ultrapassarem o teto de gastos

setorNevoa = str(input('Digite aqui o setor do seu nó: \n'))



#recebe como parâmetro a matriz do nó
#retornaDataFrame com última ocorrência de cada ID
def ultimaoOcorrencia(db):
    listaHidrometros = []
    unicaOcorencia = []
    aux = 0
    for hidrometro in db: #para criar uma lista com a última ocorrência daquele hidrômetro
        id = hidrometro[3]    
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
    #transforma em dataFrame         
    tabelaDB =  pd.DataFrame(unicaOcorencia, columns= ['Litros Utilizados', 'Horário', 'Vazao atual', 'ID', 'Situacao', 'Data de pagamento'])    
    tabelaDB.to_excel("dadosGerais.xlsx", index=True)
    #dataFrame com a última ocrrência de cada ID
    print('PRINT TABELA DB \n',tabelaDB)
    return tabelaDB

#método que retorna se o usuário está em débito ou não
#id: a id que deseja pesquisa
def verificaDebito(id, client):    
    result = pd.read_excel("pagamentos.xlsx", index_col=0)  #lê a base de dados
    pesquisa = 'ID ==' + str(id)
    filtered_df = result.query(pesquisa) #pesquisa o id pedido

    if filtered_df.empty == True: #se o id não está em pagamentos, significa que é sua primeira conta, então a informação está em dados gerais
       
        result = pd.read_excel("historicoGeralNo.xlsx", index_col=0)  #lê a base de dados
        
        #pesquisa de acordo com o id e pega a linha mais recente
        pesquisa = 'ID ==' + str(id)
        filtered_df = result.query(pesquisa)
        if filtered_df.empty == False:
            filtered_df.sort_values('Litros Utilizados', ascending=False)    
            filtered_df.iloc[0]
            
            
            horario = filtered_df['Data de pagamento'].tolist() #pega apenas o horário
            print('O pagamento deve ser efetuado', horario)
            horario = str(horario)
            ano = int(2022)
            mes = int(horario[7:9])   
            dia = int(horario[10:12])    
            hora = int(horario[13:15])   
            minuto = int(horario[16:18])   

            inicio = datetime(year=ano, month=mes, day=dia, hour=hora, minute=minuto, second=0)

            resultado = datetime.now() - inicio
            
            if resultado == timedelta(minutes = 0) or resultado > timedelta(minutes = 0): #se o resultado é == 0, significa que está no momento exado de pagamentp
                print('O usuário', id, 'está em débito')   # se o resultado é >, significa que está atrasado
                client.publish('debito/', 'Está em débito')
                time.sleep(0.4)
                client.publish('debito/', 'unsubscribe')

            else:
                print(id, ' está quitado')
                client.publish('debito/', 'Usuário Quitado')
                time.sleep(0.4)
                client.publish('debito/', 'unsubscribe')
        else:
            print(id, 'não está registrado no banco de dados. \n Verifique.')
            client.publish('debito/', 'Usuário não registrado')
            time.sleep(0.4)
            client.publish('debito/', 'unsubscribe')
    else:
        horario = filtered_df['Data de pagamento'].tolist() #pega apenas o horário
        print('O pagamento deve ser efetuado', horario)
        horario = str(horario)
        ano = int(2022)
        mes = int(horario[7:9])   
        dia = int(horario[10:12])    
        hora = int(horario[13:15])   
        minuto = int(horario[16:18])   

        inicio = datetime(year=ano, month=mes, day=dia, hour=hora, minute=minuto, second=0)

        resultado = datetime.now() - inicio
        
        if resultado == timedelta(minutes = 0) or resultado > timedelta(minutes = 0): #se o resultado ==0, é o momento exato de pagamento
            print('O usuário', id, 'está em débito')   #se é maior que zero, significa que está atrasada a conta
            client.publish('debito/', 'Está em débito')
            time.sleep(0.4)
            client.publish('debito/', 'unsubscribe')

        else:
            print(id, ' está quitado')
            client.publish('debito/', 'Usuário Quitado')
            time.sleep(0.4)
            client.publish('debito/', 'unsubscribe')

            
#retorna o histórico de id específico    
def retornaHistorico(id, client):   
    result = pd.read_excel("historicoGeralNo.xlsx", index_col=0)  #lê a base de dados   

    pesquisa = 'ID ==' + str(id)
    filtered_df = result.query(pesquisa)
    print(filtered_df)    
    historico = filtered_df.values.tolist() #transforma o histórico em lista
    if len(historico) == 0:
        print('Não existe hidrômetro matriculado com este ID')
        client.publish('historico/', 'Não existe hidrômetro matriculado com este ID' + ';'+ id + ';'+ 'x' + ';')
    else:
        for coluna in historico:  
            print(coluna)                      
            linhaHistorico = str(coluna[0]) + ';'+ str(coluna[1]) + ';'+  str(coluna[2])
            print('enviando para a api', linhaHistorico)
            client.publish('historico/', linhaHistorico)
            
    client.publish('historico/', 'unsubscribe') #quando acaba de enviar o conteúdo, envia uma mensagem para cancelar a inscrição

#retorna a média do nó/ utiliza o dataFrame para isso
def mediaNo(tabelaDB):
    media = tabelaDB['Litros Utilizados'].median()
    print('A média de litros utilizados é: ', media)
    return media

#bloqueia o hidrômetro por média geral do sistema
def bloqueioMediaGeral(tabelaDB, mediaGeral, client):
    topicoNevoa = 'bloqueio/'+ setorNevoa #será usado para enviar mensagens os hidrometros #bloqueio/desbloqueio  
    print('bloqueio media geral')    
    bloqueioTabelaMediaGeral = tabelaDB.loc[tabelaDB['Litros Utilizados'] > mediaGeral, ['ID']] #filtramos com a média geral
    idMediaGeral = bloqueioTabelaMediaGeral['ID'].tolist() #pega a lista dos ID dos hidrômetros que passaram da média geral
    print(idMediaGeral, 'DEVEM SER BLOQUEADOS POR MÉDIA GERAL')
    for id in idMediaGeral:
        print('Bloqueando por média geral:', id)
        mensagemBloqueio = 'bloquear/'+ str(id) 
        client.publish(topicoNevoa, mensagemBloqueio) #bloquearHidro
    return idMediaGeral

#médoto para desbloquear os hidrômetros que haviam sido bloqueados no ciclo anterior
def desbloqueioMedia(listaIdsBloqueados, client):
    topicoNevoa = 'bloqueio/'+ setorNevoa #será usado para enviar mensagens os hidrometros #bloqueio/desbloqueio 
    for id in listaIdsBloqueados:
        print('Desbloqueando hidrômetros:', id)
        mensagemBloqueio = 'desbloquear/'+ str(id) 
        client.publish(topicoNevoa, mensagemBloqueio) #desbloquearHidro

#retorna lista elencando os que mais gastaram
def maiorGasto(tabelaDB):
    listaTratada = []
    hidroAux = 0
    ordenado = tabelaDB.sort_values('Litros Utilizados', ascending=False)
    print('dataframe ordenado', ordenado)
    listaOrdenado = ordenado.values.tolist()
    for hidro in listaOrdenado:
        print('ID:', hidro[3], 'Litros utilizados:', hidro[0])
        hidroAux = str(hidro[3])+ ',' + str(hidro[0]) + ',' #para facilitar a parte do envio
        listaTratada.append(hidroAux)
    return listaTratada

#bloqueia hidrômetros por seu teto de gastos
#tabelaDB: dataframe com todos os hidrometros conectados ao programa
#client: cliente mqtt que irá enviar a mensagem de bloqueio para os hidrômetros que ultrapassaram o valor
def bloqueioTetoGasto(tabelaDB, tetoGasto, client):    
    topicoNevoa = 'bloqueio/'+ setorNevoa #será usado para enviar mensagens os hidrometros #bloqueio/desbloqueio    
    print('BLOQUEIO TETO DE GASTOS COM HIDRÔMETROS QUE GASTARAM MAIS QUE ', tetoGasto, 'liros')
    tetoGasto = float(tetoGasto)
    bloqueioTabelaTestoGasto = tabelaDB.loc[tabelaDB['Litros Utilizados'] > tetoGasto, ['ID']] #aqui irá retornar o ID] #filtramos com o teto de gasto #o teto de gasto deve ser verificado ta todo momemento
    idTetoGastos = bloqueioTabelaTestoGasto['ID'].tolist() #retorna uma lista com apenas o ID do filtro já feito
    print('Lista hidrômetros que ultrapassaram valor de bloqueio', idTetoGastos)
    for id in idTetoGastos:
        print('Bloqueando', id)
        mensagemBloqueio = 'bloquear/'+ str(id) 
        print('________________________________________________________________________________')  
        print(mensagemBloqueio)    
        print('________________________________________________________________________________')  
        client.publish(topicoNevoa, mensagemBloqueio) #bloquearHidro
    return idTetoGastos



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

    listaAuxPagamento = []
    listaAux = []
    idHidro = msg.topic    
    aux, setorHidrometro ,  id = idHidro.split('/')   #pegando a id do hidrômetro

    if id not in hidrometrosConectados: #conferindo se já existe essa ID na lista
        hidrometrosConectados.append(id)                
        print('hidrometros conectados', len(hidrometrosConectados) , '\n')
        #print('hidrometros conectados', nHidrometros, '\n')
    mensagem = msg.payload.decode()            
    listrosUtilizados, dataH, vazao, id, vaza, dataPagamento,  *temp = mensagem.split(',')    #a variável temp é aux para o demsempacotamento c o split
    listaAux.append(float(listrosUtilizados))
    listaAux.append(dataH)
    listaAux.append(int(vazao))
    listaAux.append(id)
    listaAux.append(vaza) 
    listaAux.append(dataPagamento)  
    print('\n')  
    print('\n---- ID:' + id, '---------------------------------------------------')    
    print('\nLitros utilizados: ' + listrosUtilizados)
    print('\nHorário/Data: ' + dataH)
    print('\nVazão atual: ' + vazao)    
    print('\n Situção de vazamento (0 para vazamento e 1 para não):'+ vaza , '\n')
    print('\n') 
    if vaza == 0: #se o hidrômetro está vazando, já envia para o servidor central
        client.publish('NoNevoa/vazando', str(id)) 
    dado.append(listaAux)    
    return dado 

#esse método serve para o servidor central verificar se todos os nós conectados enviaram suas médias, para que assim ele consiga calcular a média geral de forma correta
# ao inicializar ele envia, e ao receber a média também, pois o ciclo está se reiniciando.
def inicializacao(client):
    topicoNo = 'NoNevoa/setor/'+ setorNevoa  #tópico que conecta com o servidor  
    client.publish(topicoNo, setorNevoa) #envia a média desse nó

#retorna o consumo do hidrômetro específico 
def retornaConsumo(id, client):    
    result = pd.read_excel("historicoGeralNo.xlsx", index_col=0)  #lê a base de dados   
    print('puxou', result)

    pesquisa = 'ID ==' + str(id)
    filtered_df = result.query(pesquisa)
    ordenado = filtered_df.sort_values('Litros Utilizados', ascending=False) #ordena para pegar o valor mais recente    
    indice = ordenado.iloc[1]     
    
    if indice.empty == True:
        print('Não existe hidrômetro matriculado com este ID')
        client.publish('consumo/', 'Não existe hidrômetro matriculado com este ID' + ';'+ id + ';'+ 'verifique' + ';')
    else:
        resultado = indice.values.tolist()    
        resultado = resultado[0] #pega o valor específico
        resultado = str(resultado)
        print('Valor total do gasto', resultado)
        client.publish('consumo/', resultado)
            
    client.publish('consumo/', 'unsubscribe') #quando acaba de enviar o conteúdo, envia uma mensagem para cancelar a inscrição


#busca o valor da conta de hidrômetro específico 
def retornaValorConta(id, client):    
    result = pd.read_excel("historicoGeralNo.xlsx", index_col=0)  #lê a base de dados  
    print(result) 

    pesquisa = 'ID ==' + str(id)
    filtered_df = result.query(pesquisa)
    ordenado = filtered_df.sort_values('Litros Utilizados', ascending=False) #ordena para pegar o valor mais recente
    indice = ordenado.iloc[0]
    resultado = indice.values.tolist()
    totalLitros = resultado[0] #pega o valor específico
    resultado = str(resultado)
    if len(resultado) == 0:
        print('Não existe hidrômetro matriculado com este ID')
        client.publish('valorConta/', 'Não existe hidrômetro matriculado com este ID' + ';'+ id + ';'+ 'verifique' + ';')
    else:
        totalLitros = int(totalLitros)
        metrosC = totalLitros/1000
        if totalLitros <= 6000:
            valorReais = 28,82
        if metrosC > 7 and 10:
            valorReais = (metrosC - 6)*1.17 + 28.82
        if metrosC > 11 and 15:
            valorReais = (metrosC - 11)*7.4 + 28.82
        if metrosC > 16 and 20:
            valorReais = (metrosC - 16)*8 + 28.82
        if metrosC > 21 and 25:
            valorReais = (metrosC - 21)*10.51 + 28.82
        if metrosC > 26 and 30:
            valorReais = (metrosC - 26)*11.71 + 28.82
        if metrosC > 31 and 40:
            valorReais = (metrosC - 31)*12.90 + 28.82
        if metrosC > 41 and 50:
            valorReais = (metrosC - 41)*14.79 + 28.82
        if metrosC > 50:
            valorReais = (metrosC - 50)*17.78 + 28.82
        resultado = valorReais[:4]
        resultado = str(resultado)
        print('Valor total do gasto', resultado)
        client.publish('valorConta/', resultado)
            
    client.publish('valorConta/', 'unsubscribe') #quando acaba de enviar o conteúdo, envia uma mensagem para cancelar a inscrição


#inscreve-se no tópico do servidor e trata as mensagens, de acordo com o tópico que está sendo recebido
def subscribeServer(client: mqtt_client): 
    def on_message(client, userdata, msg):
        global tetoGasto
        global dado    
        global hidrometrosConectados
        global nHidrometros
        global listaHidrometrosBloqueados
        global listaPagamentos
        global listaTeto
        topico = msg.topic 
        print('*'*15)
        print ('TÓPICO:', topico)   
        print('*'*15)    
        aux, setorHidrometro,  id = topico.split('/')   #para tratamento

        if aux == 'server': #verfica a mensagem foi recebida pelo server
            print('________________________________________________________________________________') 
            print('--------------------------Tópico servidor  ------------------------------------') 
            print('_______________________________________________________________________________')  
            if id == 'media': 
                mediaGeral = msg.payload.decode()
                mediaGeral = int(mediaGeral[:-2]) #tira o ponto e zero
                if len(listaHidrometrosBloqueados) != 0: #para desbloquear os hidrômetros que já foram bloqueados
                    print('________________________________________________________________________________') 
                    print('--------------------------Desbloqueio do ciclo anterior-------------------------') 
                    print('________________________________________________________________________________')  
                    desbloqueioMedia(listaHidrometrosBloqueados, client)
                    if len(listaTeto)!= 0:
                        desbloqueioMedia(listaTeto, client)
                    print('________________________________________________________________________________') 
                    print('--------------------------BLOQUEIO POR MÉDIA GERAL------------------------------') 
                    print('____________________________________________MEDIA GERAL:', mediaGeral, '________')                  
                    tabela = ultimaoOcorrencia(dado)
                    listaHidrometrosBloqueados = bloqueioMediaGeral(tabela, mediaGeral, client)           
                    inicializacao(client) #após bloquear os hidrômetros, ele envia de novo para recomeçar o ciclo
                else:
                    print('________________________________________________________________________________') 
                    print('--------------------------BLOQUEIO POR MÉDIA GERAL------------------------------') 
                    print('____________________________________________MEDIA GERAL:', mediaGeral, '________') 
                    tabela = ultimaoOcorrencia(dado)
                    listaHidrometrosBloqueados = bloqueioMediaGeral(tabela, mediaGeral, client)           
                    inicializacao(client) #após bloquear os hidrômetros, ele envia de novo para recomeçar o ciclo
            elif id == 'teto':
                teto = msg.payload.decode()
                print('O teto de gastos foi alterado para', teto)
                tetoGasto = teto
                tabela = ultimaoOcorrencia(dado)
                print('tabela conectados ao nó: ',tabela)
                listaTeto = bloqueioTetoGasto(tabela, tetoGasto, client) #quando recebe o novo teto de gastos, ele puxa a tabela de ocorrências dos hidrômetros. A partir daí, já acontece  bloqueio
                #todos os hidrômetros que foram bloqueados, são add à lista de hidrômetros bloqueados, para que a cada ciclo ocorra a verficação
        elif aux == 'api':
            print('________________________________________________________________________________') 
            print('-------------------------  Requisição API   ------------------------------------') 
            print('________________________________________________________________________________')  
            if id == 'debito': #verifica se o usuário está em débito
                idPedido = msg.payload.decode()   
                verificaDebito(idPedido, client)
            if id == 'historico': #quando é pedido o histórico de um usuário específico
                idPedido = msg.payload.decode()
                retornaHistorico(idPedido, client)
            if id == 'consumo': #litros consumidos   
                idPedido = msg.payload.decode()
                print(idPedido)  
                retornaConsumo(idPedido, client)               
            if id == 'valorConta': #valor da conta
                print('pedido valor da conta')
                idPedido = msg.payload.decode()
                print(idPedido) 
                retornaValorConta(idPedido, client) 
            if id == 'pagamento': #um pagamento foi efetuado 
                listaP = []
                mensagem = msg.payload.decode() #mensagem
                id, data = mensagem.split(';')
                print('O novo horário de pagamento do', id, 'é às', data)
                listaP.append(id)
                listaP.append(data)
                listaPagamentos.append(listaP) #appenda o novo horário de pagamento
                tabelaDB =  pd.DataFrame(listaPagamentos, columns= ['ID', 'Data de pagamento'])    
                tabelaDB.to_excel("pagamentos.xlsx", index=True)

        else: #tópico dos hidrometros
            print('________________________________________________________________________________') 
            print('--------------------------Tópico hidrômetros------------------------------------') 
            print('_______________________________________________________________________________')  
            dado = recebeHidrometros(client, msg)
            tabelaHistorico =  pd.DataFrame(dado, columns= ['Litros Utilizados', 'Horário', 'Vazao atual', 'ID', 'Situacao', 'Data de pagamento']) 
            tabelaHistorico.to_excel('historicoGeralNo.xlsx', index = True) #envia para o arquivo
            

    
            #esse trecho do código verifica o tempo todo se os hidrômetros conectados ultrapassaram o valor do teto de gasto
            if tetoGasto != 0: #0 é o valor de inicialização, portanto aqui estamos verificando se foi alterado ou não. Se ele já foi alterado, o bloqueio pelo teto já ocorre assim que recebe o hidrômetro
                tabela = ultimaoOcorrencia(dado)
                listaTeto = bloqueioTetoGasto(tabela, tetoGasto, client)  
    
    

    client.subscribe("server/geral/#")          
    client.on_message = on_message

#envia para servidor central a média do hidrômetro    
def publish(client):
    global dado   
    global setorNevoa 
    status = 0
    topicoNo = 'NoNevoa/media/'+ setorNevoa  #tópico que conecta com o servidor    
    while True:
        time.sleep(4)      #aqui é pra regular a quantidade de tempo que ele vai atualizar         
        if status == 0:
            tabela = ultimaoOcorrencia(dado)
            listaMaiorGasto =  maiorGasto(tabela) #pegamos uma lista com hirômetros elencados com maior gasto
            for indice in listaMaiorGasto:
                print('Enviando maior gasto', indice)
                client.publish('maisGasto/Hidrometros', indice) #é enviado para o servidor central
                time.sleep(1)
            media = mediaNo(tabela)
            client.publish(topicoNo, media) #envia a média desse nó
            print(f"Enviando para Servidor\n")
            time.sleep(10) #colocar um tempo maior
        else:
            print(f"Erro na rede. Mensagens não estão sendo enviadas.") 

def subscribeHidrometros(client: mqtt_client): 
    def on_message(client, userdata, msg):           
        topico = msg.topic  
        print('Recebendo mensagem', msg.topic)  
    client.subscribe('Hidrometros/'+setorNevoa+'/#') 
    client.subscribe('api/'+setorNevoa+'/#') 
    client.on_message = on_message 

def run():
    client = connect_mqtt()
    inicializacao(client) 
    client.loop_start()  
    subscribeHidrometros(client)
    subscribeServer(client)    
    publish(client)

if __name__ == '__main__':
    run()