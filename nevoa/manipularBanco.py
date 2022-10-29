import sqlite3
import datetime

#criação do banco de dado do setor e criação de tabelas  (MODELO DE NOME DE SETOR: setor1)
def criarBDSetor(nomeSetor):
    try: 
        nomeArquivo = nomeSetor+"_setor.db"  
        banco = sqlite3.connect(nomeArquivo)
        cursor = banco.cursor()

        cursor.execute("CREATE TABLE hidrometros (id integer, setor integer, bloqueado boolean, motivo varchar, pagamento boolean, consumo integer)")
        banco.commit()
        banco.close()
        print("Setor criado! Conexão com sucesso!")
    except:
        print("Conexão com sucesso!")

    

#criar hidrometro no banco
def criarHidrometro(id,setor):
    try:
        nomeArquivo = setor+"_setor.db"  
        banco = sqlite3.connect(nomeArquivo)
        cursor = banco.cursor()

        nome_historico = "historico_"+str(id)+"hidro"

        cursor.execute("INSERT INTO hidrometros (id, setor, bloqueado, motivo, pagamento, consumo) VALUES(?,?,?,?,?,?)",(id, setor, False, "", True, 0))
        cursor.execute('CREATE TABLE {} (dataHora datatime, acao integer, vazao integer, statusVazamento boolean)'.format(nome_historico))

        banco.commit()
        banco.close()
    except:
        print("")


#criar histórico no banco
def gerarHistorico(id,setor,acao,vazao):
    try:
        nomeArquivo = setor+"_setor.db"  
        banco = sqlite3.connect(nomeArquivo)
        cursor = banco.cursor()

        nome_historico = "historico_"+str(id)+"hidro"
        data_hora = datetime.datetime.now()

        if vazao == 0: status_vazamento = True
        else: status_vazamento = False
        
        cursor.execute('INSERT INTO {} (dataHora, acao, vazao , statusVazamento) VALUES(?,?,?,?)'.format(nome_historico),(data_hora, "Funcionamento normal", vazao, status_vazamento))

        banco.commit()
        banco.close()
    except:
        print("")
"""#atualizar status para falso onde vazão é maior que digitado por adm ou por débito em aberto, colocar variável referente ao motivo do bloqueio 
def bloquearStatusHidrometro(id, idAcao, setor):
    nomeArquivo = setor+"_setor.db"  
    banco = sqlite3.connect(nomeArquivo)
    cursor = banco.cursor()

    cursor.execute("UPDATE hidrometros SET bloqueado = True WHERE id_hidrometro == %i",id)

    #dependendo do id da ação causa um bloqueio por motivo diferente
    if idAcao == 1:             #bloqueio por media
        cursor.execute("UPDATE hidrometros SET motivo = 'media' WHERE id_hidrometro == %i",id)
    elif idAcao == 2:           #bloqueio por débito
        cursor.execute("UPDATE hidrometros SET motivo = 'débito' WHERE id_hidrometro == %i",id)

    banco.commit()
    banco.close()"""


"""#atualizar status para true onde desbloqueia o hidrometro por adm ou por débito em aberto
def desbloquearStatusHidrometro(id, idAcao, setor):
    
    nomeArquivo = setor+"_setor.db"  
    banco = sqlite3.connect(nomeArquivo)
    cursor = banco.cursor()

    cursor.execute("UPDATE hidrometros SET bloqueado = False WHERE id_hidrometro == %i",id)

    #dependendo do id da ação causa um bloqueio por motivo diferente
    if idAcao == 1:             #bloqueio por media
        cursor.execute("UPDATE hidrometros SET motivo = '' WHERE id_hidrometro == %i",id)
    elif idAcao == 2:           #bloqueio por débito
        cursor.execute("UPDATE hidrometros SET motivo = '' WHERE id_hidrometro == %i",id)

    banco.close()"""

#atualizar status para falso onde vazão é maior que digitado por adm ou por débito em aberto, colocar variável referente ao motivo do bloqueio 
def bloquearStatusHidrometro_Media(id, setor):
    nomeArquivo = setor+"_setor.db"  
    banco = sqlite3.connect(nomeArquivo)
    cursor = banco.cursor()

    cursor.execute("""UPDATE hidrometros SET bloqueado = True, motivo = 'media' WHERE id = ?""",(id,))

    banco.commit()
    banco.close()

#atualizar status para true onde desbloqueia o hidrometro por adm ou por débito em aberto
def desbloquearStatusHidrometro_Media(id, setor):
    
    nomeArquivo = setor+"_setor.db"  
    banco = sqlite3.connect(nomeArquivo)
    cursor = banco.cursor()

    cursor.execute("""UPDATE hidrometros SET bloqueado = False, motivo = "" WHERE id = ? and motivo = 'media' """,(id,))
    
    banco.commit()
    banco.close()



#atualizar status para falso onde vazão é maior que digitado por adm
def bloquearStatusHidrometro_Teto(id, setor):
    nomeArquivo = setor+"_setor.db"  
    banco = sqlite3.connect(nomeArquivo)
    cursor = banco.cursor()

    cursor.execute("""UPDATE hidrometros SET bloqueado = True, motivo = 'teto' WHERE id = ?""",(id,))

    banco.commit()
    banco.close()


#atualizar status para falso por todos os motivos
def desbloquearStatusHidrometro_motivosGerais(id, setor):
    nomeArquivo = setor+"_setor.db"  
    banco = sqlite3.connect(nomeArquivo)
    cursor = banco.cursor()

    cursor.execute("""UPDATE hidrometros SET bloqueado = False WHERE id = ?""",(id,))

    banco.commit()
    banco.close()


#mostrar bd na tela na tela
def mostrarBDTela(setor):
    nomeArquivo = setor+"_setor.db"  
    banco = sqlite3.connect(nomeArquivo)
    cursor = banco.cursor()

    cursor.execute('SELECT * FROM hidrometros')
    print(cursor.fetchall())

    banco.close()


