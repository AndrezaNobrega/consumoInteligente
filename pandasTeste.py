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



#recebe como par??metro a matriz do n??
#retornaDataFrame com ??ltima ocorr??ncia de cada ID
def ultimaoOcorrencia(db):
    listaHidrometros = []
    unicaOcorencia = []
    aux = 0
    for hidrometro in db: #para criar uma lista com a ??ltima ocorr??ncia daquele hidr??metro
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
    tabelaDB =  pd.DataFrame(unicaOcorencia, columns= ['Litros Utilizados', 'Hor??rio', 'Vazao atual', 'ID', 'Situacao']) #dataFrame com a ??ltima ocrr??ncia de cada ID    
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

#retorna a m??dia do n??/ utiliza o dataFrame para isso
def mediaNo(tabelaDB):
    media = tabelaDB['Litros Utilizados'].median()
    print('A m??dia de litros utilizados ??: ', media)
    return media

#bloqueia o hidr??metro por m??dia geral do sistema
def bloqueioMediaGeral(tabelaDB, mediaGeral):
    print('bloqueio media geral')    
    bloqueioTabelaMediaGeral = tabelaDB.loc[tabelaDB['Litros Utilizados'] > mediaGeral] #filtramos com a m??dia geral
    # bloqueioTabelaMediaGeral = tabelaDB.loc[tabelaDB['Litros Utilizados'] > mediaGeral, ['ID']] #aqui ir?? retornar o ID
    print(bloqueioTabelaMediaGeral)

#bloqueia hidr??metros por seu teto de gastos
def bloqueioTetoGasto(tabelaDB, tetoGasto):
    print('BLOQUEIO TETO DE GASTOS')
    bloqueioTabelaTestoGasto = tabelaDB.loc[tabelaDB['Litros Utilizados'] > tetoGasto] #filtramos com o teto de gasto #o teto de gasto deve ser verificado ta todo momemento
    print(bloqueioTabelaTestoGasto)
    #depois ?? s?? pegar as id que foram retornadas

#envia para o arquivo
#se j?? existe, ele 
#dataFrame = ultimaoOcorrencia(db)
#dataFrame.to_excel('example.xlsx')
#df_Geral = pd.read_excel('dadosGeraisNo.xlsx', index_col=0,  dtype={'Litros Utilizados': int, 'Hor??rio': datetime, 'Vazao atual': int, 'ID': str, 'Situacao': str})

#para resgatar
# result = pd.read_excel('example.xlsx', index_col=0)  
#print('resultado \n', result)

'''Fun????o atualizaArquivo
dfTemporario: ?? o dataFrame que est?? na sendo utilizado neste ciclo do n??, este ser?? limpo quando as informa????es forem '''
def atualizaArquivo(dfTemporario):
    #le as informa????es ja existentes
    df_Geral = pd.read_excel('historicoGeralNo.xlsx', index_col=0)
    
      

    if df_Geral.empty == False:
        # pega os dois dataframes para concatenar
        #df_Geral = df_Geral = pd.read_excel('dadosGeraisNo.xlsx', index_col=0,  dtype={'Litros Utilizados': float, 'Hor??rio': str, 'Vazao atual': int, 'ID': str, 'Situacao': str, 'Data de pagamento': str})
        df_Geral = df_Geral = pd.read_excel('teste.xlsx', index_col=0) #le o que est?? escrito
        print('dataframe geral******* \n', df_Geral)
        
        dfTemporario = dfTemporario.reset_index(drop = True) #tirando o indice do novo dataframe
        print('data frame novo********** \n', dfTemporario)
        dfNovo = [df_Geral, dfTemporario]
        print(df_Geral, dfTemporario)
        #out_df = pd.concat(dfNovo).reset_index(drop=True)
        out_df = pd.concat(dfNovo).reset_index(drop = True) #cocatena os dois
     
               

        # escreve os DF concatenados para que existam todos
        out_df.to_excel("teste.xlsx", index=False)
        result = pd.read_excel("teste.xlsx", index_col=0)   #le pra visualizar
        print('resultado da concatena????o', result)
    else:
        dfTemporario.to_excel("teste.xlsx", index=False)
        result = pd.read_excel("teste.xlsx", index_col=0)  
        print('resultado', result)



listaTemporaria =[  [150,	'29-09-22 01:40',	'11',	5050,	'1', '29-09-22 01:40'],
                    [160,	'29-09-22 01:40',	'11',	4006,	'1', '29-09-22 01:40'],
                    [176,	'29-09-22 01:40',	'11',	4001,	'1', '29-09-22 01:40'],
                    [165,	'29-09-22 01:39',	'11',	1883,	'1', '29-09-22 01:40'],
                    [11,	'29-09-22 01:39',	'11',	3660,	'1', '29-09-22 01:40'],
                    [176,	'29-09-22 01:40',	'11',	6660,	'1', '29-09-22 01:40'],
                    [176,	'29-09-22 01:40',	'11',	4001,	'1', '29-09-22 01:40'],
                    [150,	'29-09-22 01:40',	'11',	8080,	'1', '29-09-22 01:40'],
                    [160,	'29-09-22 01:40',	'11',	5001,	'1', '29-09-22 01:40'],
                    [176,	'29-09-22 01:40',	'11',	4001,	'1', '29-09-22 01:40'],
                    [165,	'29-09-22 01:39',	'11',	4001,	'1', '29-09-22 01:40'],
                    [11,	'29-09-22 01:39',	'11',	1919,	'1', '29-09-22 01:40'],
                    [176,	'29-09-22 01:40',	'11',	4001,	'1', '29-09-22 01:40'],
                    [176,	'29-09-22 01:40',	'11',	4001,	'1', '29-09-22 01:40'],
                    [150,	'29-09-22 01:40',	'11',	4005,	'1', '29-09-22 01:40'],
                    [160,	'29-09-22 01:40',	'11',	6666,	'1', '29-09-22 01:40'],
                    [222,	'29-09-22 01:40',	'11',	3660,	'1', '29-09-22 01:40']]
 #cria um auxiliar    
dfTemporario = pd.DataFrame(listaTemporaria, columns= ['Litros Utilizados', 'Horario', 'Vazao atual', 'ID', 'Situacao', 'Data de pagamento'])



#m??todo que retorna se o usu??rio est?? em d??bito ou n??o
#id: a id que deseja pesquisa
def verificaDebito(id):
    
    result = pd.read_excel("historicoGeralNo.xlsx", index_col=0)  #l?? a base de dados

    pesquisa = 'ID ==' + str(id)
    filtered_df = result.query(pesquisa) #pega a coluna com aquela id
    horario = filtered_df["Hor??rio"].tolist() #pega apenas o hor??rio

    print(result)
    print(filtered_df)
    print(horario)
    horario = str(horario)

    ano = int(2022)
    mes = int(horario[5:7])   
    dia = int(horario[8:10])    
    hora = int(horario[11:13])   
    minuto = int(horario[14:16])   

    inicio = datetime(year=ano, month=mes, day=dia, hour=hora, minute=minuto, second=0)

    resultado = datetime.now() - inicio
    
    if resultado == timedelta(minutes = 0) or resultado > timedelta(minutes = 0): #programei dois minutos para simula??ao
        print('Este usu??rio est?? em d??bito')
        devendo = str('Em debito')
    else:
        print('Quitado')
        devendo = str('Quitado')



#fazer testes para retornar apenas o valor pedido da lista

for hidro in listaTemporaria:
    print(hidro)
    break
