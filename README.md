# 🌟 **Me Nota - Gerenciamento de Notas Fiscais Simplificado** 🌟

## 📋 **Descrição**
O **Me Nota** é um sistema intuitivo e responsivo que facilita o gerenciamento de notas fiscais para pequenas empresas e autônomos. A plataforma permite **emissão, consulta, leitura e validação de notas fiscais**, garantindo uma experiência simples e eficiente, com design minimalista e funcional.

## 🛠️ **Funcionalidades**
- **Login Seguro**: Autenticação para proteger o acesso ao sistema.
- **Emissão de Notas**: Cadastro de notas fiscais com preenchimento prático.
- **Consulta de Notas**: Visualização de registros emitidos de forma organizada.
- **Leitura de Notas**: Busca por notas fiscais a partir de um código exclusivo.
- **Validação de Notas**: Upload e validação de arquivos de notas fiscais (PDF, JPEG, PNG).
- **Design Responsivo**: Interface adaptável para desktops e dispositivos móveis.

## 📦 **Importações Necessárias**
Para rodar o aplicativo, você precisará das seguintes bibliotecas e tecnologias:

### Backend
- **Flask**: Para o servidor web.
- **pymongo**: Para interação com o MongoDB.
- **python-dotenv**: Para gerenciar variáveis de ambiente.
- **opencv-python**: Para processamento de imagens (se necessário).
- **pytesseract**: Para reconhecimento óptico de caracteres (OCR).

### Frontend
- **HTML**: Para a estrutura do sistema.
- **CSS**: Para estilização personalizada e responsiva.
- **JavaScript**: Para funcionalidades dinâmicas.

### Instalação das Dependências
Crie um arquivo `requirements.txt` com as seguintes dependências:
- Flask pymongo python-dotenv opencv-python pytesseract

### 1. **Clone o Repositório**
Clone o repositório do projeto para sua máquina local:
```bash
git clone https://github.com/Airassilva/Me_Nota.git

### 2. **Instale as Dependências**
Navegue até o diretório do projeto e instale as dependências:
- pip install -r requirements.txt
Certifique-se de que você tem o Python e o pip instalados.

### 3. **Configuração do Banco de Dados**
Certifique-se de que você tem um banco de dados MongoDB configurado. Crie um arquivo .env na raiz do projeto com as seguintes variáveis:

MONGO_URL=mongodb://<username>:<password>@<host>:<port>/<database>
MONGO_DB_NAME=nome_do_banco
MONGO_DB_COLLECTION=nome_da_colecao_documentos
MONGO_DB_COLLECTION2=nome_da_colecao_usuarios

