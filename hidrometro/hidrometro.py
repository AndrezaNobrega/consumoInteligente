
class Hidrometro: #construtor
    def __init__(self, id):
        self.id = id
        self.bloqueado = False      

    def getId(self): #retorna ID
        id = str(self.id)
        return id

    def getStatus(self):
        return self.bloqueado