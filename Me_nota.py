import cv2
import pytesseract
import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()
MONGO_URL = os.getenv("MONGO_URL")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME")

# Conectar ao MongoDB
client = MongoClient(MONGO_URL)
db = client[MONGO_DB_NAME]
collection = db['identidade']  # Nome da coleção onde os dados serão armazenados

# Função para pré-processar a imagem
def preprocess_image(image_path):
    # Carregar a imagem
    image = cv2.imread(image_path)

    # Converter para escala de cinza
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Aplicar binarização adaptativa
    binary_image = cv2.adaptiveThreshold(gray_image, 255, 
                                         cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                         cv2.THRESH_BINARY, 11, 2)

    # Remover ruído
    denoised_image = cv2.medianBlur(binary_image, 3)

    return denoised_image

# Função para detectar e extrair texto de campos específicos
def extract_fields(image):
    # Usar Tesseract para fazer OCR na imagem
    data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)

    # Inicializar um dicionário para armazenar os campos
    fields = {}

    # Iterar sobre os resultados do OCR
    for i in range(len(data['text'])):
        if int(data['conf'][i]) > 60:  # Filtrar resultados com baixa confiança
            text = data['text'][i]
            x, y, w, h = data['left'][i], data['top'][i], data['width'][i], data['height'][i]

            # Adicione lógica para identificar campos específicos
            if "Nome" in text:
                fields['Nome'] = text
            elif "Data de Nascimento" in text:
                fields['Data de Nascimento'] = text
            elif "Nome da Mãe" in text:
                fields['Nome da Mãe'] = text
            elif "Nome do Pai" in text:
                fields['Nome do Pai'] = text
            elif "Naturalidade" in text:
                fields['Naturalidade'] = text
            # Adicione mais condições conforme necessário

    return fields

# Caminho da imagem do documento
image_path = 'imagem_identidade.jpeg'  

# Pré-processar a imagem
processed_image = preprocess_image(image_path)

# Extrair campos da imagem
extracted_fields = extract_fields(processed_image)

# Exibir os campos extraídos
print("Campos extraídos:")
for key, value in extracted_fields.items():
    print(f"{key}: {value}")

# Inserir os dados extraídos no MongoDB
if extracted_fields:
    collection.insert_one(extracted_fields)
    print("Dados inseridos no MongoDB com sucesso.")
else:
    print("Nenhum dado extraído para inserir no MongoDB.")