from apiMetodos import *
from flask import Flask, jsonify
from flask import Flask, render_template, request
from flask_socketio import SocketIO
from random import random
from threading import Lock
import random
from paho.mqtt import client as mqtt_client
#broker = 'broker.emqx.io'
broker = 'localhost'  
port = 1883

client_id =str(random.randint(0, 1000))
username = 'emqx'
password = 'public'
app = Flask(__name__)


thread = None
thread_lock = Lock()
app.config['SECRET_KEY'] = 'donsky!'
socketio = SocketIO(app, cors_allowed_origins='*')

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client
client = connect_mqtt() 

"""
Aqui é onde captamos o valor via mqtt e enviamos diretamente parao o script JS para ser exibido na tela
"""
def background_thread():
    def subscribe(client: mqtt_client):
        
        def on_message(client, userdata, msg):
            mensagem = msg.payload.decode() 
            listrosUtilizados, dataH, vazao, id, vaza, *temp = mensagem.split(',')    #a variável temp é aux para o demsempacotamento c o split
            print('horário', dataH)
            print('Consumo', listrosUtilizados) 
            print('vazao', vazao)
            print('id', id)
            socketio.emit('updateHidrometro', {'value': listrosUtilizados, "date": dataH+' \nvazao:'+vazao})
            socketio.sleep(1)         
        client.on_message = on_message
    subscribe(client)
    client.loop_forever()  

"""
setor e id como parametros
"""
@app.route('/hidrometro/<string:setor>/<string:id>')
def index(setor, id):   
    client.subscribe('Hidrometros/'+ setor + '/'+ id)
    return render_template('index.html', setor = setor, id = id)

"""
Ele chama a thread que se inscreve no tópico do hidrômetro
"""
@socketio.on('connect')
def connect():
    global thread
    print('Client connected')

    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(background_thread)

"""
Quando disconectamos
"""
@socketio.on('disconnect')
def disconnect():
    print('Client disconnected',  request.sid)

"""
Envia tento o servidor central que envia para os nós
"""
@app.route('/teto/<int:teto>', methods=['PATCH']) 
def teto(teto): 
    retorno = enviaTetoMetodo(teto) #o método retorna se foi enviado com sucesso para o broker
    return jsonify(retorno) #transformando a resposta em JSON



if __name__ == "__main__":    
    socketio.run(app)

