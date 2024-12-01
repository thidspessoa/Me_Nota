from flask import Flask, redirect, render_template, request, send_from_directory, url_for
from pymongo import MongoClient
import os
from dotenv import load_dotenv
import subprocess

load_dotenv()

app = Flask(__name__, template_folder='template/Telas')  # Definindo a pasta de templates

# Definindo a pasta para salvar os arquivos enviados
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Conexão com o MongoDB
client = MongoClient(os.getenv("MONGO_URL"))
db = client[os.getenv("MONGO_DB_NAME")]  
collection = db[os.getenv("MONGO_DB_CLUSTER")] 

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Aqui você pode implementar a lógica de autenticação
        return redirect(url_for('menu'))  # Redireciona para o menu após login
    return render_template('login.html')  # Renderiza a página de login

@app.route('/menu')
def menu():
    return render_template('menu.html')  # Renderiza o menu principal

@app.route('/validarNota', methods=['GET', 'POST'])
def validar_nota():
    if request.method == 'POST':
        if 'file' not in request.files:
            return 'Nenhum arquivo enviado', 400
        file = request.files['file']
        if file.filename == '':
            return 'Nenhum arquivo selecionado', 400

        # Salva o arquivo
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)

        # Chama o extrai.py com o caminho do arquivo
        result = subprocess.run(['python', 'back/extrai.py', file_path], capture_output=True, text=True)

        # Verifica se o processamento foi bem-sucedido
        if result.returncode == 0:
            return redirect(url_for('pontuacao'))  # Redireciona para pontuacao.html
        else:
            return 'Erro ao processar o arquivo: ' + result.stderr, 500

    return render_template('validarNota.html')  # Renderiza a página de validação

@app.route('/emitir', methods=['GET', 'POST'])
def emitir():
    if request.method == 'POST':
        # Aqui você pode implementar a lógica para emitir uma nota
        return redirect(url_for('menu'))  # Redireciona para o menu após emitir
    return render_template('emitir.html')  # Renderiza a página de emissão

@app.route('/consultar')
def consultar():
    return render_template('consultar.html')  # Renderiza a página de consulta

@app.route('/lerNota', methods=['GET', 'POST'])
def ler_nota():
    if request.method == 'POST':
        # Aqui você pode implementar a lógica para ler uma nota
        return redirect(url_for('menu'))  # Redireciona para o menu após ler
    return render_template('lerNota.html')  # Renderiza a página para ler nota

@app.route('/pontuacao')
def pontuacao():
        return render_template('pontuacao.html')  # Renderiza a página de pontuação

# Rota para servir arquivos estáticos
@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('front/static', filename)

if __name__ == '__main__':
    app.run(debug=True)