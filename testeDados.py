import sqlite3
import datetime

vazao = 0
id = 25

nomeArquivo = "1_setor.db"  
banco = sqlite3.connect(nomeArquivo)
cursor = banco.cursor()

nome_historico = "historico_"+str(id)+"hidro"
data_hora = datetime.datetime.now()

if vazao == 0: status_vazamento = True
else: status_vazamento = False

#cursor.execute("CREATE TABLE hidrometros (id integer, setor integer, bloqueado boolean, motivo varchar, pagamento boolean, consumo integer)")
"""cursor.execute("INSERT INTO hidrometros (id, setor, bloqueado, motivo, pagamento, consumo) VALUES(?,?,?,?,?,?)",(id, 1, True, "", True, 0))

cursor.execute('CREATE TABLE {} (dataHora datatime, acao integer, vazao integer, statusVazamento boolean)'.format(nome_historico))
cursor.execute('INSERT INTO {} (dataHora, acao, vazao , statusVazamento) VALUES(?,?,?,?)'.format(nome_historico),(data_hora, "hidrometro criado", vazao, status_vazamento))
"""

#cursor.execute("""UPDATE hidrometros SET consumo = ? WHERE id = ?""",(45,id,))
#cursor.execute("""SELECT consumo FROM hidrometros WHERE id = ?""",(id,))
cursor.execute("""SELECT * FROM {} """.format(nome_historico))
print(cursor.fetchall())

"""cursor.execute('INSERT INTO {} (dataHora, acao, vazao , statusVazamento) VALUES(?,?,?,?)'.format(nome_historico),(data_hora, "funcionamento normal", 10, status_vazamento))
cursor.execute('INSERT INTO {} (dataHora, acao, vazao , statusVazamento) VALUES(?,?,?,?)'.format(nome_historico),(data_hora, "bloqueado", 44, status_vazamento))
"""


banco.commit()
banco.close()