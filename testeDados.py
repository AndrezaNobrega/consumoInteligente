import sqlite3
import datetime

nomeArquivo = "teste"+"_setor.db"  
banco = sqlite3.connect(nomeArquivo)
cursor = banco.cursor()

nome_historico = "historico_"+str(300)+"hidro"
data_hora = datetime.datetime.now()

vazao = str(5)

if vazao == 0: status_vazamento = True
else: status_vazamento = False
        
#cursor.execute('CREATE TABLE {} (dataHora datatime, acao integer, vazao integer, statusVazamento boolean)'.format(nome_historico))
cursor.execute('INSERT INTO {} (dataHora, acao, vazao , statusVazamento) VALUES(?,?,?,?)'.format(nome_historico),(data_hora, "Funcionamento normal", vazao, status_vazamento))

banco.commit()
banco.close()