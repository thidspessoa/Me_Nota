import pytesseract
import cv2
import re
from pymongo import MongoClient
from dotenv import load_dotenv
import os
import sys

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Função para limpar e formatar o texto
def clean_text(text):
    text = re.sub(r'[<>«»]', '', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

# Função para exibir o texto bruto extraído
def display_raw_text(data):
    print("Texto bruto extraído pela OCR:")
    for i in range(len(data['text'])):
        print(f"Texto: {data['text'][i]}, Confiança: {data['conf'][i]}")

# Função para extrair campos específicos
def extract_fields(data):
    fields = {'RG': None, 'NOME': None, 'FILIAÇÃO 1': None, 'FILIAÇÃO 2': None, 'DATA DE EXPEDIÇÃO': None, 'DATA DE NASCIMENTO': None}
    current_field = 'NOME'  # Inicia preenchendo o campo 'NOME'
    field_order = ['NOME', 'FILIAÇÃO 1', 'FILIAÇÃO 2', 'DATA DE EXPEDIÇÃO', 'DATA DE NASCIMENTO']
    current_index = 0  # Índice do campo atual
    parts = []  # Armazena as partes entre delimitadores
    rg_found = False  # Controle para RG
    data_expedicao_found = False  # Controle para data de expedição
    data_nascimento_found = False  # Controle para data de nascimento

    for i in range(len(data['text'])):
        text = data['text'][i]
        confidence = int(data['conf'][i])

        # Ignorar textos com baixa confiança ou vazios, exceto para a naturalidade
        if confidence <= 60 and not text.strip():
            continue

        # Procurar o número do RG (primeira sequência de números com pontos)
        if not rg_found and re.match(r'\d{1,3}\.\d{3}\.\d{3}', text):
            fields['RG'] = text
            rg_found = True
            continue

        # Procurar datas no formato dd/mm/aaaa
        if not data_expedicao_found and re.match(r'\d{2}/\d{2}/\d{4}', text):
            fields['DATA DE EXPEDIÇÃO'] = text
            data_expedicao_found = True
            continue
        if not data_nascimento_found and re.match(r'\d{2}/\d{2}/\d{4}', text):
            fields['DATA DE NASCIMENTO'] = text
            data_nascimento_found = True
            continue

        # Detectar início de um bloco
        if text in ["<<", "<<+","<"]:
            parts = []  # Reinicia as partes para o novo bloco
            continue

        # Detectar fim de um bloco
        if text in [">>", "+>"]:
            if parts:  # Verifica se há algo válido no bloco
                joined_text = " ".join(parts).strip()  # Junta as partes
                fields[field_order[current_index]] = joined_text  # Salva no campo atual
                current_index += 1  # Avança para o próximo campo
                if current_index >= len(field_order):  # Limita os campos
                    break
            parts = []  # Reseta as partes
            continue
        # Adicionar texto válido ao bloco
        parts.append(text)
    return fields

# Função para inserir dados no MongoDB
def insert_into_mongo(data):
    try:
        # Conectar ao MongoDB Atlas
        client = MongoClient(os.getenv("MONGO_URL"))
        db = client[os.getenv("MONGO_DB_NAME")]
        collection = db[os.getenv("MONGO_DB_CLUSTER")]

        # Inserir os dados extraídos
        collection.insert_one(data)
        print("Dados inseridos com sucesso no MongoDB.")
    except Exception as e:
        print(f"Erro ao inserir no MongoDB: {e}")

def main(image_path):
    image = cv2.imread(image_path)

    # Ajustar contraste e brilho
    alpha = 2.0 # Contraste
    beta = 25  # Brilho
    adjusted_image = cv2.convertScaleAbs(image, alpha=alpha, beta=beta)

    # Converter para escala de cinza
    gray_image = cv2.cvtColor(adjusted_image, cv2.COLOR_BGR2GRAY)

    # Aplicar remoção de ruído
    denoised_image = cv2.fastNlMeansDenoising(gray_image, None, 30, 7, 21)

    # Aplicar binarização adaptativa para melhorar o contraste local
    binary_image = cv2.adaptiveThreshold(
        denoised_image, 
        255, 
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
        cv2.THRESH_BINARY, 
        11, 
        2
    )

    # Salvar e exibir a imagem processada
    processed_image_path = "processed_image_for_ocr.jpg"
    cv2.imwrite("processed_image_for_ocr.jpg", binary_image)

    # Realizar OCR na imagem processada
    custom_config = r'--oem 3 --psm 6'
    data = pytesseract.image_to_data(binary_image, lang='por', config=custom_config, output_type=pytesseract.Output.DICT)

    # Exibir texto bruto extraído
    display_raw_text(data)

    # Extrair campos relevantes
    extracted_fields = extract_fields(data)

    # Exibir campos extraídos
    print("\nCampos extraídos:")
    for key, value in extracted_fields.items():
        print(f"{key}: {value}")

    # Condição para inserir no MongoDB
    if all(extracted_fields.values()):
        print("Dados prontos para inserção no MongoDB:")
        print(extracted_fields)
        insert_into_mongo(extracted_fields)
    else:
        print("Nenhum dado relevante extraído para inserir no MongoDB.")

    # Excluir a imagem processada
    if os.path.exists(processed_image_path):
         os.remove(processed_image_path)
         print(f"A imagem processada '{processed_image_path}' foi excluída.")
    else:
         print(f"A imagem processada '{processed_image_path}' não foi encontrada para exclusão.")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Uso: python extrai.py <caminho_da_imagem>")
        sys.exit(1)
    image_path = sys.argv[1]
    success = main(image_path)
    if success:
        print("Processamento concluído com sucesso.")
    else:
        print("Falha no processamento.")
