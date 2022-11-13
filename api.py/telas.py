

def menu():
    import requests
    print('_______________________________________________________')
    print('####################### M E N U #######################')
    print('_______________________________________________________')
    print('1) Cliente')
    print('2) Admin')
    resposta = input('Digite a opção: ')
    if resposta == '1':
        print('_______________________________________________________')
        print('####################### M E N U #######################')
        print('_____________________U S U Á R I O_____________________')
        print('')
        id = input('Digite sua matrícula: ')
        setor = input('Digite aqui o seu setor:')
        print('Bem vindo',  resposta)   
        print('1) Consumo total') 
        print('2) histórico')
        print('3) Valor')
        print('4) Pagar')
        print('5) Retornar para o menu')
        opcao = input('Digite a opção que deseja escolher: \n')  
        if opcao == '1':
            print('LITROS ACUMULADOS')        
            import requests
            url = "http://127.0.0.1:5000/consumo-total/"+ setor + '/' + id
            payload = ""
            response = requests.request("GET", url, data=payload)
            
            print(response.text)
            menu()
        elif opcao == '2':
            print('HISTÓRICO DE CONSUMO:')           
            import requests
            url = "http://127.0.0.1:5000/historico/"+ setor + '/' + id
            payload = ""
            response = requests.request("GET", url, data=payload) 
            print(' Horário| Vazão | Litros utilizados')
            print(response.text)
            menu()
        elif opcao == '3':
            print('Valor da sua conta:')            
            import requests
            url = "http://127.0.0.1:5000/valorconta/"+ setor + '/' + id
            payload = ""
            response = requests.request("GET", url, data=payload) 
            print(response.text)
            menu()
        elif opcao == '4':
            print('Realizando o pagamento:')            
            import requests
            url = "http://127.0.0.1:5000/pagamento/"+ setor + '/' + id
            payload = ""
            response = requests.request("GET", url, data=payload) 
            print(response.text)
            print('O pagamento foi realizado com sucesso')
            menu()        
        elif opcao == '5':
            menu()
    else:
        print('Menu aministrador')
        senha = input('Digite aqui a senha: ')
        if senha == '1234':
            print('_______________________________________________________')
            print('####################### M E N U #######################')
            print('________________A D M I N S T R A D O R________________')
            print('')
            print('Bem vindo, Admin!')
            print('Digite a opção: \n')
            print('1) Envie um novo teto de gastos')
            print('2) Visualização dos N maiores hidrômetros')
            print('3) Visualização dos hidrômetros com possível vazamento')
            print('4) Digite aqui para verificar se determinado hidrômetro está em débito')
            print('5) Bloquear hidrômetro')
            print('6) Visualiza hidrômetro em tempo real')
            opcao = input('Digite aqui a opção que deseja acessar: \n')
            if opcao == '1':
                import requests
                teto = str(input('Digite aqui o teto de gastos que deseja inserir:'))
                url = "http://127.0.0.11:5000/teto/" + teto
                payload = " "
                headers = {"Content-Type": "application/json"}
                response = requests.request("PATCH", url, data=payload, headers=headers)
                print(response.text)
                menu()
            elif opcao == '2':   
                print('Visualização dos N maiores hidrômetros') 
                n = str(input('Digite o número de hidrômetros que deseja visualizar:'))
                url = "http://127.0.0.1:5000/listar/" + n
                payload = ""
                response = requests.request("GET", url, data=payload)
                print(response.text)
                menu()
            elif opcao == '3':
                print('Visualizando IDs de hidrômetros com possível vazamento')
                url = "http://127.0.0.1:5000/vazamento"
                payload = ""
                response = requests.request("GET", url, data=payload)
                print(response.text)
                menu()
            elif opcao == '4':
                print('Verificar se determinado hidrômetro está em débito')
                id = str(input('Digite aqui o id do hidrômetro que deseja pesquisar:'))
                setor = str(input('Digite aqui o setor do hidrômetro que deseja pesquisar:'))
                url = "http://127.0.0.1:5000/debito/"+ setor + '/' + id
                headers = {"Content-Type": "application/json"}
                response = requests.request("GET", url, headers=headers)
                print(response.text)
            elif opcao == '5':
                print('Bloquear hidrômetro que está em débito')
                import requests
                id = str(input('Digite aqui o id do hidrômetro que será bloqueado'))
                url = "http://127.0.0.1:5000/bloqueio/" + id
                payload = ""
                response = requests.request("POST", url, data=payload)
                print('Status:')                
                print(response.text)
            elif opcao == '6':
                print('Visualizar hidrômetro em tempo real')
                id = str(input('Digite aqui o id do hidrômetro que deseja pesquisar:'))
                setor = str(input('Digite aqui o setor do hidrômetro que deseja pesquisar:'))
                url = "http://127.0.0.1:5000/hidrometro/"+ setor + '/' + id
                print('Abra o navegador em ip+:5000/hidrometro/')
                payload = ""
                response = requests.request("GET", url, data=payload)
                print(response.text)
            else:
                menu()  
        else:
            print('Senha errada!')
            menu()
menu()







