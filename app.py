from flask import Flask, render_template, request, redirect, jsonify
from tinydb import TinyDB, Query
from datetime import datetime
from dobot import TheRobot

robot = TheRobot()

app = Flask(__name__)
db = TinyDB('dados/db.json')

@app.route('/')
def main():
    return render_template('index.html')

@app.route('/logs', methods=['GET'])
def get_logs():
    logs = db.table('logs').all()
    return render_template('logs.html', logs=logs)

@app.route('/move', methods=['POST'])
def move():
    dados = request.form
    x = dados.get("x")
    y = dados.get("y")
    z = dados.get("z")
    r = dados.get("r")

    if None in (x, y, z, r):
        # Registra um comando de erro se qualquer coordenada estiver ausente
        registrar_comando("Movimento - Não foi possível movimentar o robô", x=x, y=y, z=z, r=r)
        # Redireciona para a página inicial se os dados de movimentação estiverem incompletos
        return jsonify ({"error": "Dados de movimentação incompletos"}), 400
    else:
        x, y, z, r = float(x), float(y), float(z), float(r)
        registrar_comando("Movimento - Movimento realizado com sucesso", x=x, y=y, z=z, r=r)
        robot.mover(x, y, z, 0)
    return render_template('index.html')

@app.route('/home', methods=['POST'])
def home():
    try:
        # Supondo que a função para mover o robô para a posição inicial seja home()
        robot.home()
        return jsonify({"success": "Robô movido para a posição inicial com sucesso!"}), 200
    except Exception as e:
        # Em caso de erro, retorna uma mensagem indicativa
        return jsonify({"error": str(e)}), 500
	
def registrar_comando(descricao, **kwargs):
     now = datetime.now()
     date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
     comando = {'descricao': descricao, 'date_time': date_time, 'updates': kwargs}
     db.table('logs').insert(comando)

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=8000)