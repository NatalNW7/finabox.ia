import tabula
import PyPDF2
import pandas as pd
import re
import os
from pdf2image import convert_from_path
import pytesseract

BASE =  os.path.join(os.getcwd(), 'temp')

def get_total_pages(pdf: str) -> int:
    total_pages = 0
    with open(pdf, 'rb') as file:
        pdfReader = PyPDF2.PdfReader(file) 
        total_pages = len(pdfReader.pages)

    return total_pages 

def read_pdf(pdf, pages, header=None) -> pd.DataFrame:
    dfs = tabula.io.read_pdf(pdf,pages=pages)

    if len(dfs) > 1:
        csv_output = os.path.join(BASE, "output.csv")
        tabula.convert_into(pdf, csv_output, output_format="csv", pages=pages)
        fatura = pd.read_csv(csv_output, names=header, delimiter=',')

        return fatura

    return dfs[0]

def read_nubank(pdf) -> pd.DataFrame:
    header=['Data', 'Unnamed', 'Movimentacao', 'Valor']
    pages = f'4-{get_total_pages(pdf)}'
    fatura = read_pdf(pdf, pages, header)
    fatura.drop(columns=['Unnamed'], inplace=True)
    fatura.dropna(axis=0, inplace=True)

    return fatura

def read_inter(pdf):
    fatura = PyPDF2.PdfReader(pdf)
    text = fatura.pages[1].extract_text()
    dict_fatura = []
    output = os.path.join(BASE, "output.txt")

    with open(output, 'w') as fatura_txt:
        fatura_txt.write(text)

    with open(output, 'r') as fatura_txt:
        text = fatura_txt.readlines()

        for line in text:
            cleaned_line = re.sub(r'\xa0|\x00', ' ', line.strip())
            extracted = re.search(r'^(\d{2}\s\w{3}\s\d{4})(.+)(R\$\s\d.\d{1,},\d{2}|R\$\s\d{1,},\d{2})$', cleaned_line)

            if extracted:
                dict_fatura.append({
                    'Data': extracted.group(1).strip(),
                    'Movimentacao': extracted.group(2).strip(),
                    'Valor': extracted.group(3).strip()
                })

    fatura = pd.DataFrame(dict_fatura)

    return fatura

def read_meliuz(pdf):
    pages = f'3-{get_total_pages(pdf)}'
    df = read_pdf(pdf, pages=pages)
    df = df[['Unnamed: 0','Unnamed: 1','Unnamed: 2']]
    df = df.rename(columns={'Unnamed: 0': 'Data', 'Unnamed: 1': 'Movimentacao', 'Unnamed: 2': 'Valor'})
    df = df.dropna()
    
    return df.reset_index(drop=True)

def read_pan(pdf) -> pd.DataFrame:
    pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'  # Substitua pelo caminho correto
    output = 'output.txt'
    fatura = []
    imagens = convert_from_path(pdf)

    for i, imagem in enumerate(imagens):
        i += 1
        
        if i == 3:
            texto = pytesseract.image_to_string(imagem)
            with open(os.path.join(BASE, output), 'w') as fatura_txt:
                fatura_txt.write(texto)
                
    with open(os.path.join(BASE, output), 'r') as fatura_txt:
        lines = fatura_txt.readlines()
        for line in lines:
            line = line.strip()
            if line:
                extracted = re.search(r'^(\d{0,}\/\d{0,})(.+)(RS\d{0,},\d{0,}|RS\s\d{0,},\d{0,}|R\$\d{0,},\d{0,}|R\$\s\d{0,},\d{0,})$', line)

                if extracted:
                    fatura.append({
                        'Data': extracted.group(1).strip(),
                        'Movimentacao': extracted.group(2).strip(),
                        'Valor': extracted.group(3).strip()
                    })

    return pd.DataFrame(fatura)

if '__main__' == __name__:
    pdf_nubank = 'Nubank_2023-07-23.pdf'
    pdf_inter = 'inter_2023-07.pdf'
    pdf_meliuz = 'meliuz-2023-07.pdf'
    pdf_pan = 'pan_2023-07.pdf'

    fatura_nubank = read_nubank(pdf_nubank)
    print("Nubank", fatura_nubank)
    fatura_inter = read_inter(pdf_inter)
    print("Inter",fatura_inter)

    fatura_meliuz = read_meliuz(pdf_meliuz)
    print("Meliuz",fatura_meliuz)

    fatura_pan = read_pan(pdf_pan)
    print("Pan",fatura_pan)

    # TODO fazer leitura de pdf pan

            
    
    