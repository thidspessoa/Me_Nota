from flask import Flask, redirect, render_template, request, send_from_directory, url_for
from pymongo import MongoClient
import os
from dotenv import load_dotenv
import subprocess

load_dotenv()

template_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), '../front/templates')
static_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), '../front/static')

app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)

# Definindo a pasta para salvar os arquivos enviados
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Conexão com o MongoDB
client = MongoClient(os.getenv("MONGO_URL"))
db = client[os.getenv("MONGO_DB_NAME")]  
collection = db[os.getenv("MONGO_DB_COLLECTION2")] 

@app.route('/')
def home():
    return render_template('telaCarregamento.html')

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form.get('nome')
        cpf = request.form.get('cpf')
        email = request.form.get('email')
        senha = request.form.get('senha')
        tipo = request.form.get('tipo')

        if not nome or not cpf or not email or not senha or not tipo:
            return render_template('cadastro.html', message='Todos os campos são obrigatórios.')

        # Verifica se o CPF já está cadastrado
        if collection.find_one({'cpf': cpf}):
            return render_template('cadastro.html', message='Este CPF já está registrado.')

        # Verifica se o e-mail já está cadastrado
        if collection.find_one({'email': email}):
            return render_template('cadastro.html', message='Este e-mail já está registrado.')

        # Insere o novo usuário no banco de dados
        user = {
            "nome": nome,
            "cpf": cpf,
            "email": email,
            "senha": senha,  # Não é recomendado armazenar senhas sem hash, considere usar hashing
            "tipo": tipo
        }
        collection.insert_one(user)

        # Redireciona para o login após o cadastro
        return redirect(url_for('login'))

    return render_template('cadastro.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('senha')

        if not email or not senha:
            return render_template('login.html', message='Por favor, preencha todos os campos.')

        # Busca o usuário no MongoDB
        user = collection.find_one({'email': email})

        if not user:
            return render_template('login.html', message='Usuário não encontrado.')

        # Verifica se a senha está correta (comparação direta)
        if user['senha'] != senha:
            return render_template('login.html', message='Senha incorreta.')

        # Redireciona para o menu após autenticação bem-sucedida
        return redirect(url_for('telaPrincipal.html'))
    
    return render_template('login.html')

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
    return send_from_directory(static_dir, filename)

if __name__ == '__main__':
    app.run(debug=True)