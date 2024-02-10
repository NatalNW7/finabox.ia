from pdf2image import convert_from_path
import pytesseract

# Caminho para o arquivo PDF
caminho_pdf = 'meliuz-2023-07.pdf'

# Convertendo o PDF para uma lista de imagens
imagens = convert_from_path(caminho_pdf)

# Inicializando o Pytesseract
pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'  # Substitua pelo caminho correto

# Processando cada imagem
for i, imagem in enumerate(imagens):
    # Convertendo a imagem para texto usando Pytesseract
    texto = pytesseract.image_to_string(imagem)  # 'por' para português
    
    # Fazendo algo com o texto (por exemplo, imprimir)
    print(f"Texto na página {i + 1}:\n{texto}\n{'='*50}")
