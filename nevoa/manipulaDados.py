from datetime import datetime, timedelta

import time
import pandas as pd







def verificaDebito(id, client):    
    result = pd.read_excel("dadosGerais.xlsx", index_col=0)  #lê a base de dados
    

    pesquisa = 'ID ==' + str(id)

    filtered_df = result.query(pesquisa)
    print(filtered_df)
    
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
    
    if resultado == timedelta(minutes = 0) or resultado > timedelta(minutes = 0): #programei dois minutos para simulaçao
        print('O usuário', id, 'está em débito')  

    else:
        print(id, ' está quitado')


def listaVazamento(client):    
    vazamento = pd.read_excel("vazamento.xlsx", index_col=0)  #lê a base de dados   
    for usuario in vazamento:
        print (usuario)
    print('unsubscribe')


def retornaHistorico(id, client):    
    result = pd.read_excel("historicoGeralNo.xlsx", index_col=0)  #lê a base de dados   

    pesquisa = 'ID ==' + str(id)
    filtered_df = result.query(pesquisa)
    print(filtered_df)    
    historico = filtered_df.values.tolist() #transforma o histórico em lista
    if len(historico) == 0:
        print('Não existe hidrômetro matriculado com este ID')
    else:
        for coluna in historico:
            linhaHistorico = str(coluna[0]) + ';'+ str(coluna[1]) + ';'+  str(coluna[4])
            print(linhaHistorico)
    print('unsubscribe')

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
        client.publish('consumo/', 'Não existe hidrômetro matriculado com este ID' + ';'+ id + ';'+ 'x' + ';')
    else:
        resultado = indice.values.tolist()    
        resultado = resultado[1] #pega o valor específico
        resultado = str(resultado)
        print('Valor total do gasto', resultado)
        #client.publish('consumo/', resultado)
            
    client.publish('consumo/', 'unsubscribe') #quando acaba de enviar o conteúdo, envia uma mensagem para cancelar a inscrição


#busca o valor da conta de hidrômetro específico 
def retornaValorConta(id):    
    result = pd.read_excel("historicoGeralNo.xlsx", index_col=0)  #lê a base de dados  
    print(result) 

    pesquisa = 'ID ==' + str(id)
    filtered_df = result.query(pesquisa)
    ordenado = filtered_df.sort_values('Litros Utilizados', ascending=False) #ordena para pegar o valor mais recente
    indice = ordenado.iloc[1]
    resultado = indice.values.tolist()
    totalLitros = resultado[1] #pega o valor específico
    resultado = str(resultado)
    if len(resultado) == 0:
        print('Não existe hidrômetro matriculado com este ID')
        #client.publish('valorConta/', 'Não existe hidrômetro matriculado com este ID' + ';'+ id + ';'+ 'x' + ';')
    else:
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
        print('Valor total do gasto', resultado)
        #client.publish('valorConta/', resultado)
            
    #client.publish('valorConta/', 'unsubscribe') #quando acaba de enviar o conteúdo, envia uma mensagem para cancelar a inscrição

retornaValorConta('4357')





