from flask import Flask, jsonify
app = Flask(__name__)
'''rotas adm'''



@app.route('/exemplo', methods=['GET'])  #endpoint
def exemplo():
    #primeiro vamos enviar a requisição para o bd via mqtt
    #a gente vai recever a resposta e transformar em json
    #dessa maneira # jsonify(resposta)
    return 'jshfkdsjf'


@app.route('/listar/<int:n>', methods=['GET'])  #lista os n maiores hidômetros <ind:n> = envia os n maiores
def lista(n):
    #primeiro vamos enviar a requisição para o servidor
    #o servidor vai retornar uma lita com os n maiores números
    #n0 servidor, preciso ter uma verificação se possuo essa quantidade
    #a gente vai recever a resposta e transformar em json
    #dessa maneira # jsonify(resposta)
    return 'a lista'


@app.route('/vazamento', methods=['GET'])  #procurar os hidrômetros que possuem vazamento
def lista(n):
    #a ver como será feito
    #a gente vai recever a resposta e transformar em json
    #dessa maneira # jsonify(resposta)
    return 'a lista'


@app.route('/debito/<str:setor>/<str:id>', methods=['GET'])  #verifica se está em debito
def debito(setor, id):
    #no bd
    #primeiro vamos enviar a requisição para o servidor
    #o servidor vai retornar se o hidrômetro está em débito
    #contar por tempo
    #criar uma lista no nó que o nome é 'hidrômetros em débito'
    #trata enviando para o banco de dados
    #a gente vai receber a resposta e transformar em json
    #dessa maneira # jsonify(resposta)
    return 'resposta'


@app.route('/<str:setor>/<str:id>', methods=['GET'])  #selecionar um hidrômetro para visualizar suas informações em tempo real
def list(setor, id):
    #envia requisição para a névoa com base no seu setor
    #bd daquele nó pesquisa o id e retorna a lista
    #pode se inscrever no tópico daquele hidrômetro (testar)
    return jsonify(user)


@app.route('/<int:teto>', methods=['PUT'])  #enviar o teto de gastos para o servidor geral
def teto(teto):
    #envia requisição com o teto de gastos para o servidor geral
    #o servidor geral deve enviar para todos os nós
    return jsonify(user)


@app.route('/<str:setor>/<str:id>', methods=['POST'])  #bloqueia hidrômetro
def bloquear(setor, id):
    #aqui chamamos método já exisente no nó
    #também add à lista de bloqueados: motivação de 'débito'
    return jsonify(user)


'''

                    rotas usuário
                    
                                                          '''


@app.route('historico/<str:setor>/<str:id>',  methods=['GET'])  #visualizar histórico daquele usuário
def histórico(setor, id):
    #envia requisição para o bd do nó deste hidrômetro
    #no bd, ele faz a pesquisa do histórico do hidrômetro
    return jsonify(user)


@app.route('consumo-total/<str:setor>/<str:id>', methods=['GET'])  #visualizar consumo daquele usuário
def consumo(setor, id):
    #envia requisição para o bd do nó deste hidrômetro
    return jsonify(user)


@app.route('consumo-total/<str:setor>/<str:id>', methods=['GET'])  #visualizar históico daquele usuário
def valorConta(setor, id):
    #envia requisição para o bd do nó deste hidrômetro
    return jsonify(user)


@app.route('consumo-total/<str:setor>/<str:id>', methods=['GET'])  #visualizar históico daquele usuário
def pagaConta(setor, id):
    #copia método de desbloqueio aqui
    return jsonify(user)


#como colocar um parâmtros
@app.route('/<str:id>', methods=['GET'])
#eemplo para busca por ID
def list(id):
    for user in db:
        if id == user.id():
            return jsonify(user)


#aqui quando a gente for bloquear um hidrômetro
#@app.route('/bloquear/<str:id>', methods =['POST'])
#vai chamar o método de bloqueio que é mqtt
#tb, precisa add à lista de hidrômetros bloqueado, este com a motivação de 'falta de pagamento'

#inicializando a API
if __name__ == "__main__":
    app.run(host='0.0.0.0')
'''Aqui a gente vai ver como fazer as requisições
import requests
link = https://desenvolvendo-APi.andrezanobrega.repl.co (do exemplo acima)
requisicao = requsts.get(link)
print(requisicao)
print(requisicao.json())'''
