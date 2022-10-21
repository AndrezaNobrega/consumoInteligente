import sqlite3

#criação do banco de dados e cursor para explorar banco

banco = sqlite3.connect('consumo_inteligente.db')
cursor = banco.cursor()


#criação de tabela
cursor.execute("CREATE TABLE hidrometro (id integer, setor integer, bloqueado boolean, motivo varchar, consumo integer)")
cursor.execute("CREATE TABLE historico (id_hidrometro integer, dataHora datatime, vazao integer, statusVazamento integer, setor integer")

#criar hidrometro
def criarHidrometro(id):
    cursor.execute("INSERT INTO hidrometro VALUES (id, "+hidrometro1.getStatus+"'))

#atualizar status para falso onde vazão é maior que a média
cursor.execute("UPDATE hidrometros SET bloqueado = 'False' WHERE vazao < media and ")

cursor.execute("UPDATE hidrometros SET bloqueado = 'True' WHERE vazao > media")


#mostrar na tela
cursor.execute('SELECT * FROM hidrometro')
print(cursor.fetchall())


#bloquear hidrometro

#ativar hidrometro

#buscar média

#adicionar hidrometro

#tornar item do banco um hidrometro




# conn.Execute("INSERT INTO table1(col1 , col2) VALUES(?,?)",val1, val2);