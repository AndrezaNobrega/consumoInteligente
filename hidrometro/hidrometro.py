class Hidrometro: #construtor
    def __init__(self, id, setor):
        self.id = id
        self.bloqueado = False      
        self.setor = setor
        self.motivoBloqueio = ""
        self.consumoTotal = 0
        self.pagamento = True
        self.vazamento = False

    def getId(self): #retorna ID
        id = str(self.id)
        return id

    def getStatus(self):
        return self.bloqueado
    
    def getSetor(self):
        return self.setor
    
    def getMotivoBloqueio(self):
        return self.motivoBloqueio
    
    def getConsumoTotal(self):
        return self.consumoTotal
    
    def getPagamento(self):
        return self.pagamento

    def getVazamento(self):
        return self.vazamento