import cv2
import pytesseract

# Função para pré-processar a imagem
def preprocess_image(image_path):
    # Carregar a imagem
    image = cv2.imread(image_path)

    # Converter para escala de cinza
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Aplicar binarização
    _, binary_image = cv2.threshold(gray_image, 150, 255, cv2.THRESH_BINARY)

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

            # Aqui você pode adicionar lógica para identificar campos específicos
            # Por exemplo, se o texto contiver "Nome", você pode armazená-lo
            if "Nome" in text:
                fields['Nome'] = text
            elif "Data de Nascimento" in text:
                fields['Data de Nascimento'] = text
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