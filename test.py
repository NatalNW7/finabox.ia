from pdf2image import convert_from_path
import pytesseract
import os
import re
import json


BASE =  os.path.join(os.getcwd(), 'temp')

# Caminho para o arquivo PDF
caminho_pdf = 'meliuz-2023-07.pdf'
output = 'output.txt'

imagens = convert_from_path(caminho_pdf)

pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'  # Substitua pelo caminho correto

fatura = []

for i, imagem in enumerate(imagens):
    i += 1
    
    if i == 3:
        texto = pytesseract.image_to_string(imagem)
        with open(os.path.join(BASE, output), 'w') as fatura_txt:
            fatura_txt.write(texto)
        # if re.search(r'Natanael\W+\D+\d+', texto):
        #     print("DEBUG", texto)
            
with open(os.path.join(BASE, output), 'r') as fatura_txt:
    lines = fatura_txt.readlines()
    for line in lines:
        if line.strip():
            print(line)
            extracted = re.search(r'^(\d{0,}\/\d{0,})(.+)(RS\d{0,},\d{0,}|RS\s\d{0,},\d{0,}|R\$\d{0,},\d{0,}|R\$\s\d{0,},\d{0,})$', line.strip())
            print(extracted)
            if extracted:
                fatura.append({
                    'Data': extracted.group(1).strip(),
                    'Movimentacao': extracted.group(2).strip(),
                    'Valor': extracted.group(3).strip()
                })


print(len(fatura))
print(json.dumps(fatura, indent=4))
