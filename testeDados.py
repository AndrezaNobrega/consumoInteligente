

from nevoa.manipularBanco import *








"""import pandas as pd

estados = ['Acre',
           'Amapá',
           'Amazonas',
           'Pará',
           'Rondônia',
           'Roraima',
           'Tocantins']

df = pd.DataFrame(estados, columns=['estados'])

print(df)"""
"""import sqlite3

banco = sqlite3.connect("setor.db")
cursor = banco.cursor()
id = 50
#cursor.execute("CREATE TABLE hidrometro (id integer, setor integer, bloqueado boolean, motivo varchar, consumo integer)")
#cursor.execute("INSERT INTO hidrometro (id, setor, bloqueado, motivo, consumo) VALUES(?,?,?,?,?)",(id, "1", True, "media", 0))
banco.commit()

cursor.execute('SELECT * FROM hidrometro')
print(cursor.fetchall())

"""
"""banco = sqlite3.connect("2_setor.db")
cursor = banco.cursor()

cursor.execute('SELECT * FROM hidrometro')
print(cursor.fetchall())"""


nomeArquivo = "_setor.db"  
banco = sqlite3.connect(nomeArquivo)
cursor = banco.cursor()

id_nome = str(500)
nome_historicoBanco = id_nome + "_hidro_historico"

#cursor.execute("CREATE TABLE hidrometros (id integer, setor integer, bloqueado boolean, motivo varchar, consumo integer)")
#cursor.execute("INSERT INTO hidrometros (id, setor, bloqueado, motivo, consumo) VALUES(?,?,?,?,?)",(500, 2, False, "", 0))
#banco.commit()
cursor.execute('SELECT * FROM hidrometros')
print(cursor.fetchall())

cursor.execute("""UPDATE hidrometros SET bloqueado = False, motivo = '' WHERE id = ?""",(500,))
banco.commit()


"""cursor.execute("CREATE TABLE {} (id_hidrometro integer, dataHora datatime, vazao integer, statusVazamento boolean, setor integer".format(nome_historicoBanco))
banco.commit()"""
banco.close()