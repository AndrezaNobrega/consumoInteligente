lista = []




teste = ('11111: 3')
idL, nL = teste.split(':')
if len(lista) != 0:
    indice = 0
    for no in lista:        
        id, numeroHidros = no.split(':')
        if id == idL: #se já existe na lista 
            print('antes do pop', lista)
            print(indice)           
            lista.pop(indice) #apagamos o anterior 
            print('depois do pop', lista) 
        indice =+ 1 #para pegar o indice que deve ser deletado    
    teste = (idL+ ':'+ nL) 
    lista.append(teste) #atualizamos o valor
    print(lista)
else:
    teste = (idL+ ':'+ nL) 
    lista.append(teste) #atualizamos o valor
    print(lista)
    