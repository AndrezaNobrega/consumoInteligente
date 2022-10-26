

from banco_dados.manipularBanco import *








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

cursor.execute("""UPDATE hidrometro SET bloqueado = False, motivo = "" WHERE id = ? and motivo = 'media' """,(id,))
banco.commit()

cursor.execute('SELECT * FROM hidrometro')
print(cursor.fetchall())

banco.close()"""
