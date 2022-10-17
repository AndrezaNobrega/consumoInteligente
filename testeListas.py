lista = []
lista.append('15')
for i in range(5):
    add = str(i)
    lista.append(add)
    i = int(i)
lista.append(';')
lista.append('25')
for i in range(5):
    add = str(i)
    lista.append(add)
    i = int(i)
lista.append(';')
lista.append('25')
for i in range(5):
    add = str(i)
    lista.append(add)
    i = int(i)
lista.append(';')

print(lista)
hidroNovo = '7'
encontrado = '0'
for no in lista:
    for hidro in no:
        if hidro == hidroNovo:            
            encontrado = '1'
            break
if encontrado == '1':
    print('encontrado')
else:
    print('não foi encontrado')

