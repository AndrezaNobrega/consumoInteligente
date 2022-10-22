import sqlite3

banco = sqlite3.connect('consumo_inteligente.db')


cursor = banco.cursor()
#cursor.execute("CREATE TABLE hidrometro (id integer, setor integer, bloqueado boolean, motivo varchar, consumo integer)")

cursor.execute("INSERT INTO hidrometro (id, setor, bloqueado, motivo, consumo) VALUES(?,?,?,?,?)",("912", "setor_12",False,"debito","0"))

def criarHidrometro(id,setor):
    #cursor.execute("INSERT INTO hidrometro VALUES (", "+setor")",id,setor)
    cursor.execute("INSERT INTO hidrometro (id, setor, bloqueado, motivo, consumo) VALUES(?,?,?,?,?)",(id, setor,False,"",0))


criarHidrometro(12,"setor2")

cursor.execute('SELECT * FROM hidrometro')
print(cursor.fetchall())