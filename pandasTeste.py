import pandas as pd

db = [[154,	'29-09-22 01:39',	'11',	4001,	'1'],
[165,	'29-09-22 01:39',	'11',	4001,	'1'],
[11,	'29-09-22 01:39',	'11',	3660,	'1'],
[176,	'29-09-22 01:40',	'11',	4001,	'1'],
[22,	'29-09-22 01:40',	'11',	3660,	'1']]

tabelaDB =  pd.DataFrame(db, columns= ['Litros Utilizados', 'Horário', 'Vazao atual', 'ID', 'Situacao']) #criando DataFrame do bd
tabelaDB.plot()

print(tabelaDB)

#recebe como parâmetro a matriz do nó
#retorna média
def mediaNo(db):
    listaHidrometros = []
    unicaOcorencia = []
    aux = 0
    for hidrometro in db: #para criar uma lista com a última ocorrência daquele hidrômetro
        id = hidrometro[3]        
        if id not in listaHidrometros: 
            listaHidrometros.append(id)
            unicaOcorencia.append(hidrometro)                             
        else:
            unicaOcorencia.pop(aux)
            unicaOcorencia.append(hidrometro) 
    aux +=1 
    print(aux)                  
    tabelaDB =  pd.DataFrame(unicaOcorencia, columns= ['Litros Utilizados', 'Horário', 'Vazao atual', 'ID', 'Situacao']) #criando DataFrame do bd    
    media = tabelaDB['Litros Utilizados'].median()
    print('A média de litros utilizados é: ', media)
    return int(media)
media = mediaNo(db)
print(media)