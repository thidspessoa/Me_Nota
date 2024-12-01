from flask import Flask, redirect, render_template, request, jsonify, send_from_directory, url_for
from pymongo import MongoClient
import os
from dotenv import load_dotenv
import jwt
import datetime
import subprocess  # Para chamar o script extrai.py

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

app = Flask(__name__)

# Conexão com o MongoDB
client = MongoClient(os.getenv("MONGO_URL"))
db = client[os.getenv("MONGO_DB_NAME")]
collection = db[os.getenv("MONGO_DB_CLUSTER")]

@app.route('/')
def home():
    return send_from_directory(os.path.join(os.pardir, 'front'), 'Telas','login.html') 

@app.route('/Telas/<path:filename>')
def serve_tela(filename):
    return send_from_directory(os.path.join(os.pardir, 'front', 'Telas'), filename)

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory(os.path.join(os.pardir, 'front', 'static'), filename)

# Pasta para salvar os arquivos enviados
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/validarNota', methods=['GET', 'POST'])
def validar_nota():
    if request.method == 'POST':
        # Verifica se o arquivo foi enviado
        if 'file' not in request.files:
            return 'Nenhum arquivo enviado', 400
        file = request.files['file']
        if file.filename == '':
            return 'Nenhum arquivo selecionado', 400

        # Salva o arquivo
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)

        # Chama o extrai.py com o caminho do arquivo e captura o retorno
        result = subprocess.run(['python', 'extrai.py', file_path], capture_output=True, text=True)

        # Verifica se o processamento foi bem-sucedido
        if result.returncode == 0:
            return redirect(url_for('pontuacao'))  # Redireciona para pontuacao.html
        else:
            return 'Erro ao processar o arquivo: ' + result.stderr, 500

    return render_template('validarNota.html')  # Renderiza a página de validação

@app.route('/pontuacao')
def pontuacao():
    return render_template('pontuacao.html')  # Renderiza a página de pontuação


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)