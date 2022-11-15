from apiMetodos import *
from flask import Flask, jsonify

app = Flask(__name__)

#enviamos um novo teto de gastos para o servidor
@app.route('/teto/<int:teto>', methods=['PATCH'])  #enviar teto para todos os nós
def teto(teto): 
    retorno = enviaTetoMetodo(teto) #o método retorna se foi enviado com sucesso para o broker
    return jsonify(retorno) #transformando a resposta em JSON

@app.route('/listar/<int:n>', methods=['GET'])  #lista os n maiores hidômetros <ind:n> | envia os n maiores
def lista(n):
    retorno = nHidrometros(n)
    return jsonify(retorno) #transformando a resposta em JSON

@app.route('/vazamento', methods=['GET'])  #procurar os hidrômetros que possuem vazamento
def verifica():
    retorno =  verificaVazamento()
    return jsonify(retorno) #transformando a resposta em JSON

@app.route('/debito/<string:setor>/<string:id>', methods=['GET'])  #verifica se está em debito
def debito(setor, id):
    retorno = verificaDebito(id, setor)
    return jsonify(retorno) #transformando a resposta em JSON

@app.route('/bloqueio/<string:id>', methods=['POST'])  #bloqueia hidrômetro
def bloquear(id):
    user = bloqueiaHidrometro(id)
    return jsonify(user)

#rotas do usuário

@app.route('/historico/<string:setor>/<string:id>',  methods=['GET'])  #visualizar histórico daquele usuário
def histórico(setor, id):
    historico = verificaHistorico(id, setor)
    return jsonify(historico)

@app.route('/consumo-total/<string:setor>/<string:id>', methods=['GET'])  #visualizar consumo daquele usuário
def consumo(setor, id):
    consulta = verificaConsumo(id, setor)
    return jsonify(consulta)
    
@app.route('/valorconta/<string:setor>/<string:id>', methods=['GET'])  #buscar o valor da conta
def valorConta(setor, id):
    consulta = verificaValorConta(id, setor)
    return jsonify(consulta)

@app.route('/pagamento/<string:setor>/<string:id>', methods=['PUT'])  #pagar a conta
def pagaConta(setor, id):
    retornoPagamento = desbloqueiaHidrometro(id, setor)
    return jsonify(retornoPagamento)

#inicializando a API
if __name__ == "__main__":
    app.run(host='172.16.103.6', port=5000)

