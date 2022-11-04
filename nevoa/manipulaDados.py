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


def listaVazamento():    
    result = pd.read_excel("dadosGerais.xlsx", index_col=0)  #lê a base de dados    

    print(result)
    pesquisa = 'Situacao == 0'
    filtered_df = result.query(pesquisa)
    print(filtered_df)
    
    vazamento = filtered_df['ID'].tolist() #pega apenas o horário
    print('Usuários com vazamento', vazamento)

    for usuario in vazamento:
        print (usuario)
    print('unsubscribe')


listaVazamento()