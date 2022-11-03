from datetime import *
from msilib.schema import tables
import time
from unittest import result
import pandas as pd
#pip install o openpyxl
from openpyxl import load_workbook

db = [[154,	'29-09-22 01:39',	'11',	4001,	'1'],
[176,	'29-09-22 01:40',	'11',	4001,	'1'],
[165,	'29-09-22 01:39',	'11',	4001,	'1'],
[11,	'29-09-22 01:39',	'11',	3660,	'1'],
[176,	'29-09-22 01:40',	'11',	4001,	'1'],
[176,	'29-09-22 01:40',	'11',	4001,	'1'],
[150,	'29-09-22 01:40',	'11',	4005,	'1'],
[160,	'29-09-22 01:40',	'11',	4006,	'1'],
[176,	'29-09-22 01:40',	'11',	4001,	'1'],
[165,	'29-09-22 01:39',	'11',	4001,	'1'],
[11,	'29-09-22 01:39',	'11',	3660,	'1'],
[176,	'29-09-22 01:40',	'11',	4001,	'1'],
[176,	'29-09-22 01:40',	'11',	4001,	'1'],
[150,	'29-09-22 01:40',	'11',	4005,	'1'],
[160,	'29-09-22 01:40',	'11',	4006,	'1'],
[176,	'29-09-22 01:40',	'11',	4001,	'1'],
[165,	'29-09-22 01:39',	'11',	4001,	'1'],
[11,	'29-09-22 01:39',	'11',	3660,	'1'],
[176,	'29-09-22 01:40',	'11',	4001,	'1'],
[176,	'29-09-22 01:40',	'11',	4001,	'1'],
[150,	'29-09-22 01:40',	'11',	4005,	'1'],
[160,	'29-09-22 01:40',	'11',	4006,	'1'],
[176,	'29-09-22 01:40',	'11',	4001,	'1'],
[165,	'29-09-22 01:39',	'11',	4001,	'1'],
[11,	'29-09-22 01:39',	'11',	3660,	'1'],
[176,	'29-09-22 01:40',	'11',	4001,	'1'],
[176,	'29-09-22 01:40',	'11',	4001,	'1'],
[150,	'29-09-22 01:40',	'11',	4005,	'1'],
[160,	'29-09-22 01:40',	'11',	4006,	'1'],
[176,	'29-09-22 01:40',	'11',	4001,	'1'],
[165,	'29-09-22 01:39',	'11',	4001,	'1'],
[11,	'29-09-22 01:39',	'11',	3660,	'1'],
[176,	'29-09-22 01:40',	'11',	4001,	'1'],
[176,	'29-09-22 01:40',	'11',	4001,	'1'],
[150,	'29-09-22 01:40',	'11',	4005,	'1'],
[160,	'29-09-22 01:40',	'11',	4006,	'1'],
[176,	'29-09-22 01:40',	'11',	4001,	'1'],
[165,	'29-09-22 01:39',	'11',	4001,	'1'],
[11,	'29-09-22 01:39',	'11',	3660,	'1'],
[176,	'29-09-22 01:40',	'11',	4001,	'1'],
[176,	'29-09-22 01:40',	'11',	4001,	'1'],
[150,	'29-09-22 01:40',	'11',	4005,	'1'],
[160,	'29-09-22 01:40',	'11',	4006,	'1'],
[176,	'29-09-22 01:40',	'11',	4001,	'1'],
[165,	'29-09-22 01:39',	'11',	4001,	'1'],
[11,	'29-09-22 01:39',	'11',	3660,	'1'],
[176,	'29-09-22 01:40',	'11',	4001,	'1'],
[176,	'29-09-22 01:40',	'11',	4001,	'1'],
[150,	'29-09-22 01:40',	'11',	4005,	'1'],
[160,	'29-09-22 01:40',	'11',	4006,	'1'],
[176,	'29-09-22 01:40',	'11',	4001,	'1'],
[165,	'29-09-22 01:39',	'11',	4001,	'1'],
[11,	'29-09-22 01:39',	'11',	3660,	'1'],
[176,	'29-09-22 01:40',	'11',	4001,	'1'],
[176,	'29-09-22 01:40',	'11',	4001,	'1'],
[150,	'29-09-22 01:40',	'11',	4005,	'1'],
[160,	'29-09-22 01:40',	'11',	4006,	'1'],
[176,	'29-09-22 01:40',	'11',	4001,	'1'],
[165,	'29-09-22 01:39',	'11',	4001,	'1'],
[11,	'29-09-22 01:39',	'11',	3660,	'1'],
[176,	'29-09-22 01:40',	'11',	4001,	'1'],
[176,	'29-09-22 01:40',	'11',	4001,	'1'],
[150,	'29-09-22 01:40',	'11',	4005,	'1'],
[160,	'29-09-22 01:40',	'11',	4006,	'1'],
[22,	'29-09-22 01:40',	'11',	3660,	'1']]



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
        else:
            aux = listaHidrometros.index(id)
            unicaOcorencia.pop(aux)
            unicaOcorencia.append(hidrometro) 
            listaHidrometros.pop(aux)
            listaHidrometros.append(id)        
    tabelaDB =  pd.DataFrame(unicaOcorencia, columns= ['Litros Utilizados', 'Horário', 'Vazao atual', 'ID', 'Situacao']) #dataFrame com a última ocrrência de cada ID    
    return tabelaDB

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
    
    
    #agora enviamos para o servidor central

#retorna a média do nó/ utiliza o dataFrame para isso
def mediaNo(tabelaDB):
    media = tabelaDB['Litros Utilizados'].median()
    print('A média de litros utilizados é: ', media)
    return media

#bloqueia o hidrômetro por média geral do sistema
def bloqueioMediaGeral(tabelaDB, mediaGeral):
    print('bloqueio media geral')    
    bloqueioTabelaMediaGeral = tabelaDB.loc[tabelaDB['Litros Utilizados'] > mediaGeral] #filtramos com a média geral
    # bloqueioTabelaMediaGeral = tabelaDB.loc[tabelaDB['Litros Utilizados'] > mediaGeral, ['ID']] #aqui irá retornar o ID
    print(bloqueioTabelaMediaGeral)

#bloqueia hidrômetros por seu teto de gastos
def bloqueioTetoGasto(tabelaDB, tetoGasto):
    print('BLOQUEIO TETO DE GASTOS')
    bloqueioTabelaTestoGasto = tabelaDB.loc[tabelaDB['Litros Utilizados'] > tetoGasto] #filtramos com o teto de gasto #o teto de gasto deve ser verificado ta todo momemento
    print(bloqueioTabelaTestoGasto)
    #depois é só pegar as id que foram retornadas

#envia para o arquivo
#se já existe, ele 
#dataFrame = ultimaoOcorrencia(db)
#dataFrame.to_excel('example.xlsx')
#df_Geral = pd.read_excel('dadosGeraisNo.xlsx', index_col=0,  dtype={'Litros Utilizados': int, 'Horário': datetime, 'Vazao atual': int, 'ID': str, 'Situacao': str})

#para resgatar
# result = pd.read_excel('example.xlsx', index_col=0)  
#print('resultado \n', result)

'''Função atualizaArquivo
dfTemporario: é o dataFrame que está na sendo utilizado neste ciclo do nó, este será limpo quando as informações forem '''
def atualizaArquivo(dfTemporario):
    #le as informações ja existentes
    df_Geral = pd.read_excel('historicoGeralNo.xlsx', index_col=0)
    print(df_Geral)

    

    # pega os dois dataframes para concatenar
    dfNovo = [df_Geral, dfTemporario]
    print(df_Geral, dfTemporario)
    out_df = pd.concat(dfNovo).reset_index(drop=True)

    # escreve os DF concatenados para que existam todos
    out_df.to_excel("historicoGeralNo.xlsx", index=False)
    result = pd.read_excel("historicoGeralNo.xlsx", index_col=0)  
    print('resultado', result)


listaTemporaria =[  [150,	'29-09-22 01:40',	'11',	5050,	'1'],
                    [160,	'29-09-22 01:40',	'11',	4006,	'1'],
                    [176,	'29-09-22 01:40',	'11',	4001,	'1'],
                    [165,	'29-09-22 01:39',	'11',	1883,	'1'],
                    [11,	'29-09-22 01:39',	'11',	3660,	'1'],
                    [176,	'29-09-22 01:40',	'11',	6660,	'1'],
                    [176,	'29-09-22 01:40',	'11',	4001,	'1'],
                    [150,	'29-09-22 01:40',	'11',	8080,	'1'],
                    [160,	'29-09-22 01:40',	'11',	5001,	'1'],
                    [176,	'29-09-22 01:40',	'11',	4001,	'1'],
                    [165,	'29-09-22 01:39',	'11',	4001,	'1'],
                    [11,	'29-09-22 01:39',	'11',	1919,	'1'],
                    [176,	'29-09-22 01:40',	'11',	4001,	'1'],
                    [176,	'29-09-22 01:40',	'11',	4001,	'1'],
                    [150,	'29-09-22 01:40',	'11',	4005,	'1'],
                    [160,	'29-09-22 01:40',	'11',	4006,	'1'],
                    [222,	'29-09-22 01:40',	'11',	3660,	'1']]
 #cria um auxiliar    
dfTemporario = pd.DataFrame(listaTemporaria, columns= ['Litros Utilizados', 'Horário', 'Vazao atual', 'ID', 'Situacao'])



#método que retorna se o usuário está em débito ou não
#id: a id que deseja pesquisa

def verificaDebito(id):
    
    result = pd.read_excel("historicoGeralNo.xlsx", index_col=0)  #lê a base de dados

    pesquisa = 'ID ==' + id
    filtered_df = dfTemporario.query(pesquisa) #pega a coluna com aquela id
    horario = filtered_df["Horário"].tolist() #pega apenas o horário
    horario = str(horario)

    ano = int(2022)
    mes = int(horario[5:7])   
    dia = int(horario[8:10])    
    hora = int(horario[11:13])   
    minuto = int(horario[14:16])   

    inicio = datetime(year=ano, month=mes, day=dia, hour=hora, minute=minuto, second=0)

    resultado = datetime.now() - inicio
    
    if resultado == timedelta(minutes = 0) or resultado > timedelta(minutes = 0): #programei dois minutos para simulaçao
        print('Este usuário está em débito')
        devendo = str('Em debito')
    else:
        print('Quitado')
        devendo = str('Quitado')

verificaDebito('1919', dfTemporario)