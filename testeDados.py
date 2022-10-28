import sqlite3

nomeArquivo = "teste"+"_setor.db"  
banco = sqlite3.connect(nomeArquivo)
cursor = banco.cursor()

nome_historico = str(200)+"_hidroHistorico"

"""            """
cursor.execute("""CREATE TABLE {} (id_hidrometro integer, dataHora datatime, vazao integer, statusVazamento boolean, setor integer)""".format(nome_historico))

banco.commit()
banco.close()