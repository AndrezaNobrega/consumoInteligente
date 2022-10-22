import sqlite3
cursor = sqlite3.Cursor()

#criação do banco de dado do setor e criação de tabelas 
def criarSetor(nomeSetor):
    nomeArquivo = nomeSetor+"_setor.db"  
    banco = sqlite3.connect(nomeArquivo)
    cursor = banco.cursor()

    cursor.execute("CREATE TABLE hidrometro (id integer, setor integer, bloqueado boolean, motivo varchar, consumo integer)")
    cursor.execute("CREATE TABLE historico (id_hidrometro integer, dataHora datatime, vazao integer, statusVazamento integer, setor integer")

#criar hidrometro no banco
def criarHidrometro(id,setor):
    cursor.execute("INSERT INTO hidrometro (id, setor, bloqueado, motivo, consumo) VALUES(?,?,?,?,?)",(id, setor, False, "", 0))

#atualizar status para falso  ou true onde vazão é maior que digitado por adm ou por débito em aberto, colocar variável referente ao motivo do bloqueio 
def atualizarStatusHidrometro(id, idAcao):
    cursor.execute("UPDATE hidrometros SET bloqueado = True WHERE id_hidrometro == id")

    #dependendo do id da ação causa um bloqueio por motivo diferente
    if idAcao == 1:             #bloqueio por media
        cursor.execute("UPDATE hidrometros SET motivo = 'media' WHERE id_hidrometro == id")
    elif idAcao == 2:           #bloqueio por débito
        cursor.execute("UPDATE hidrometros SET motivo = 'débito' WHERE id_hidrometro == id")


#mostrar bd na tela na tela
def mostrarBDTela():
    cursor.execute('SELECT * FROM hidrometro')
    print(cursor.fetchall())

#tornar item do banco um hidrometro - pegar linha do sql e transformar em obj




# conn.Execute("INSERT INTO table1(col1 , col2) VALUES(?,?)",val1, val2);