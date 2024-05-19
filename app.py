from flask import Flask, render_template, request, redirect, url_for
import socket
import threading
import random
import time

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/juego', methods=['POST'])
def juego():
    nombre = request.form['nombre']
    return render_template('juego.html', nombre=nombre)

def recibir_mensajes(client):
    while True:
        try:
            msg = client.recv(1024).decode()
            # Aquí puedes manejar los mensajes recibidos del servidor como desees
            print(msg)
        except:
            client.close()
            break

@app.route('/start_game', methods=['POST'])
def start_game():
    nombre = request.form['nombre']
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('localhost', 5555))
    client.send(nombre.encode())
    threading.Thread(target=recibir_mensajes, args=(client,)).start()
    return redirect(url_for('juego', nombre=nombre))

if __name__ == '__main__':
    app.run(debug=True)
