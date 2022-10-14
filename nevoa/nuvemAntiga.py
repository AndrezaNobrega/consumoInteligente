from __future__ import print_function
import socket
from time import sleep
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

import _thread

HOST = '127.0.0.1'              # Endereco IP do Servidor
PORT = 5000            # Porta que o Servidor esta

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
print('Aguardando conexões')
def conectado(con, cliente):
    #Script para conexão servidor/nuvem (google sheets)
    creds = None    
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'servidor\client_secret.json', SCOPES) #arquivo usado para fazer a primeira autenticação
            creds = flow.run_local_server(port=0)
        # salvamos para o próximo acesso
        with open('token.json', 'w') as token: #Autenticação p/ acessar a planilha
            token.write(creds.to_json())

    service = build('sheets', 'v4', credentials=creds)
    print ('Conectado por', cliente)
    sheet = service.spreadsheets() #resgata o arquivo      
    while True:        
        dadosHidr = [] #criando lista p os dados dos hidrometros - a lista recebe duas colunas e depois zera novamente
        data = con.recv(1024) #recebendo            
        dado = data.decode() 
        if not data: break
        listrosUtilizados, dataH, vazao, id, vaza, ip, *temp = dado.split(',')    #a variável temp é temp para o demsempacotamento c o split    
        print ('Recebendo dado de cliente com IP:\n', ip)
        print('\nLitros utilizados: ' + listrosUtilizados)
        print('\nHorário/Data: ' + dataH)
        print('\nVazão atual: ' + vazao)
        print('\n ID:' + id)
        print('\n Situção de vazamento (0 para vazamento e 1 para não)'+ vaza)            
        consumo = listrosUtilizados, dataH, vazao, id, vaza, ip
        dadosHidr.append(consumo)               
        #envio para google sheets. Damos sempre um append com uma  linha no final        
        result = sheet.values().append(spreadsheetId='1SDuvwzFTQ4_KIgtYVUgTLKVa2okDRYBc4gXl2Fn8fO0', #id da planilha
                                    range='Página1!A2', 
                                    valueInputOption= 'USER_ENTERED', #tipo de input - Aqui só avisa como será tratado
                                    body= {"values": dadosHidr}).execute()
        
        
        sleep(5)

    print ('Finalizando conexao do cliente', cliente)
    con.close()
    _thread.exit()

tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

orig = (HOST, PORT)

tcp.bind(orig)
tcp.listen(1)

while True: #para aceitar múltiplas conexões, cada hidrometro no servidor é executado como uma thread
    con, cliente = tcp.accept()
    _thread.start_new_thread(conectado, tuple([con, cliente]))    

