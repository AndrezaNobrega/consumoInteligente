import sqlite3
import datetime
import json

#CRIAÇÃO DE BANCO E HIDROMETRO ------------------------------------------------------------------------

#criação do banco de dado do setor e criação de tabelas  (MODELO DE NOME DE SETOR: setor1)
def criarBDSetor(nomeSetor):
    try: 
        nomeArquivo = nomeSetor+"_setor.db"  
        banco = sqlite3.connect(nomeArquivo)
        cursor = banco.cursor()

        cursor.execute("CREATE TABLE hidrometros (id integer, setor integer, bloqueado boolean, motivo varchar, pagamento boolean, consumo integer, statusVazamento boolean)")
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

        cursor.execute("INSERT INTO hidrometros (id, setor, bloqueado, motivo, pagamento, consumo, vazamento) VALUES(?,?,?,?,?,?,?)",(id, setor, False, "", True, 0, False))
        cursor.execute('CREATE TABLE {} (dataHora datatime, acao integer, vazao integer)'.format(nome_historico))

        banco.commit()
        banco.close()
    except:
        print("")



#ALTERAÇÃO POR PAGAMENTO ----------------------------------------------------------------

#atualizar pagamento e bloqueio de hidrometro
def bloquearStatusHidrometro_debito(id, setor):
    nomeArquivo = setor+"_setor.db"  
    banco = sqlite3.connect(nomeArquivo)
    cursor = banco.cursor()

    cursor.execute("""UPDATE hidrometros SET bloqueado = True, motivo = 'debito', pagamento = False WHERE id = ?""",(id,))

    banco.commit()
    banco.close()

#atualizar pagamento e bloqueio de hidrometro - pagamento de conta 
def desbloquearStatusHidrometro_debito(id, setor):
    nomeArquivo = setor+"_setor.db"  
    banco = sqlite3.connect(nomeArquivo)
    cursor = banco.cursor()

    cursor.execute("""UPDATE hidrometros SET bloqueado = False, motivo = "", pagamento = True WHERE id = ?""",(id,))

    banco.commit()
    banco.close()

#ALTERAÇÃO POR MÉDIA  -------------------------------------------------------------------

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


#ALTERAÇÃO POR TETO  -------------------------------------------------------------------

#atualizar status para falso onde vazão é maior que digitado por adm
def bloquearStatusHidrometro_Teto(id, setor):
    nomeArquivo = setor+"_setor.db"  
    banco = sqlite3.connect(nomeArquivo)
    cursor = banco.cursor()

    cursor.execute("""UPDATE hidrometros SET bloqueado = True, motivo = 'teto' WHERE id = ?""",(id,))

    banco.commit()
    banco.close()


#MÉTODOS GERAIS -----------------------------------------------------------------------

#salvar consumo total
def salvarConsumoTotal(id,setor,consumo):
    nomeArquivo = setor+"_setor.db"  
    banco = sqlite3.connect(nomeArquivo)
    cursor = banco.cursor()

    cursor.execute("""UPDATE hidrometros SET consumo = ? WHERE id = ? """,(consumo, id,))

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


#criar histórico no banco
def gerarHistorico(id,setor,acao,vazao):
    try:
        nomeArquivo = setor+"_setor.db"  
        banco = sqlite3.connect(nomeArquivo)
        cursor = banco.cursor()

        nome_historico = "historico_"+str(id)+"hidro"
        data_hora = datetime.datetime.now()

        if vazao == 0: 
            cursor.execute("""UPDATE hidrometros SET vazamento = True WHERE id = ?""",(id,))

        else: 
            cursor.execute("""UPDATE hidrometros SET vazamento = False WHERE id = ?""",(id,))
        
        cursor.execute('INSERT INTO {} (dataHora, acao, vazao) VALUES(?,?,?)'.format(nome_historico),(data_hora, acao, vazao))
        
        
        banco.commit()
        banco.close()
    except:
        print("")

#mostrar bd na tela na tela
def mostrarBDTela(setor):
    nomeArquivo = setor+"_setor.db"  
    banco = sqlite3.connect(nomeArquivo)
    cursor = banco.cursor()

    cursor.execute('SELECT * FROM hidrometros')
    print(cursor.fetchall())

    banco.close()


#CONSULTAS -----------------------------------------------------------------------------

#consultar consumo total do hidrometro
def consultarConsumo(id, setor):
    nomeArquivo = setor+"_setor.db"  
    banco = sqlite3.connect(nomeArquivo)
    cursor = banco.cursor()

    cursor.execute("""SELECT consumo FROM hidrometros WHERE id = ?""",(id,))
    
    banco.close()

#exibição do histórico de funcionamento do hidrometro
def exibirHistorico(id, setor):
    nomeArquivo = setor+"_setor.db"  
    banco = sqlite3.connect(nomeArquivo)
    cursor = banco.cursor()

    nome_historico = "historico_"+str(id)+"hidro"

    cursor.execute("""SELECT * FROM {} """.format(nome_historico))    
    banco.close()

#exibir informações de único hidrometro
#def exibirHidrometro_uno(id, setor):

#exibir hidrometros em débito
def consultarStatus_debito(id, setor):
    nomeArquivo = setor+"_setor.db"  
    banco = sqlite3.connect(nomeArquivo)
    cursor = banco.cursor()

    cursor.execute("""SELECT consumo FROM hidrometros WHERE id = ?""",(id,))
    
    banco.close()   

#consultar todos hidrometros em vazamento
def consultarStatus_vazamento(id, setor):
    nomeArquivo = setor+"_setor.db"  
    banco = sqlite3.connect(nomeArquivo)
    cursor = banco.cursor()

    cursor.execute("""SELECT consumo FROM hidrometros WHERE id = ?""",(id,))
    banco.close()







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
