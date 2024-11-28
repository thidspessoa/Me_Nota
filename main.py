import pytesseract
import cv2
import re

# Função para limpar e formatar o texto
def clean_text(text):
    text = re.sub(r'[<>«»]', '', text)  # Remove símbolos indesejados
    text = re.sub(r'\s+', ' ', text)  # Remove espaços extras
    return text.strip()

# Função para exibir o texto bruto extraído
def display_raw_text(data):
    print("Texto bruto extraído pela OCR:")
    for i in range(len(data['text'])):
        print(f"Texto: {data['text'][i]}, Confiança: {data['conf'][i]}")

# Função para extrair campos específicos
def extract_fields(data):
    fields = {'NOME': None, 'FILIAÇÃO': None, 'NATURALIDADE': None, 'DATA DE NASCIMENTO': None}
    filiation = []

    # Variáveis para armazenar os valores encontrados
    nome_found = False
    filiacao_found = False

    # Percorre todo o texto extraído
    for i in range(len(data['text'])):
        text = clean_text(data['text'][i])
        confidence = int(data['conf'][i])

        if confidence > 60:  # Confiança mínima
            # Detecta e captura o nome, se encontrado entre << >>
            if not nome_found:
                if text.upper() == "NOME" and i + 1 < len(data['text']):
                    next_text = clean_text(data['text'][i + 1])
                    match = re.search(r'<<([^\>]+)>>|<<\+([^\>]+)>', next_text)  # Procura por << >> ou <<+>
                    if match:
                        fields['NOME'] = ' '.join(filter(None, match.groups())).strip()  # Junta as palavras capturadas
                        nome_found = True  # Marca que o nome foi encontrado

            # Detecta e captura a filiação, se encontrada entre << >>
            if not filiacao_found and text.upper() == "FILIAÇÃO":
                # Procura pelas próximas palavras entre << >> ou <<+>
                for j in range(i + 1, len(data['text'])):
                    next_text = clean_text(data['text'][j])
                    match = re.search(r'<<([^\>]+)>>|<<\+([^\>]+)>', next_text)
                    if match:
                        filiation.append(' '.join(filter(None, match.groups())).strip())  # Adiciona a filiação encontrada
                    # Verifica se o próximo texto é outro marcador de fim de filiação
                    if filiation and len(filiation) > 1:
                        break

                if filiation:
                    fields['FILIAÇÃO'] = " e ".join(filiation)  # Junta os valores encontrados como uma string
                    filiacao_found = True  # Marca que a filiação foi encontrada

            # Detecta a naturalidade
            if text.upper() == "NATURALIDADE" and i + 1 < len(data['text']):
                fields['NATURALIDADE'] = clean_text(data['text'][i + 1])

            # Detecta a data de nascimento
            if "NASC" in text.upper():  # Considera variações como "NASCMBDO"
                for j in range(1, 3):  # Procura data nas próximas linhas
                    if i + j < len(data['text']) and re.match(r'\d{2}/\d{2}/\d{4}', data['text'][i + j]):
                        fields['DATA DE NASCIMENTO'] = data['text'][i + j]
                        break

    return fields

# Função principal
def main(image_path):
    # Carrega a imagem
    image = cv2.imread(image_path)

    # Pré-processamento da imagem
    processed_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # Converte para escala de cinza
    processed_image = cv2.threshold(processed_image, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]  # Binariza a imagem

    # Realiza OCR na imagem
    custom_config = r'--oem 3 --psm 6'
    data = pytesseract.image_to_data(processed_image, lang='por', config=custom_config, output_type=pytesseract.Output.DICT)

    # Exibe o texto bruto extraído
    display_raw_text(data)

    # Extrai os campos relevantes
    extracted_fields = extract_fields(data)

    # Exibe os campos extraídos
    print("\nCampos extraídos:")
    for key, value in extracted_fields.items():
        print(f"{key}: {value}")

    # Condição para inserir no MongoDB
    if all(extracted_fields.values()):
        print("Dados prontos para inserção no MongoDB:")
        print(extracted_fields)
    else:
        print("Nenhum dado relevante extraído para inserir no MongoDB.")

# Executa o programa
if __name__ == "__main__":
    image_path = "gray_image.jpg"
    main(image_path)






