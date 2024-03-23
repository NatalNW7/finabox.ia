import tabula
import PyPDF2
import pandas as pd
import re
import os
from pdf2image import convert_from_path
import pytesseract
from datetime import datetime
import uuid


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
    fatura['Cartao'] = 'Nubank'
    fatura['Tipo de Compra'] = 'Credito'

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
                    'Data': converter_formato_data(extracted.group(1).strip()),
                    'Movimentacao': extracted.group(2).strip(),
                    'Valor': extracted.group(3).strip().replace('R$ ', ''),
                    'Cartao': 'Inter',
                    'Tipo de Compra': 'Credito'
                })

    return pd.DataFrame(dict_fatura)

def read_meliuz(pdf):
    pages = f'3-{get_total_pages(pdf)}'
    df = read_pdf(pdf, pages=pages)
    df = df[['Unnamed: 0','Unnamed: 1','Unnamed: 2']]
    df = df.rename(columns={'Unnamed: 0': 'Data', 'Unnamed: 1': 'Movimentacao', 'Unnamed: 2': 'Valor'})
    df = df.dropna()
    df = df.reset_index(drop=True)
    df['Valor'] = df['Valor'].str.replace('R$ ', '')
    df['Cartao'] = 'Meliuz'
    df['Tipo de Compra'] = 'Credito'
    
    return df

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
                        'Data': converter_formato_data(extracted.group(1).strip(), "2023"),
                        'Movimentacao': extracted.group(2).strip(),
                        'Valor': re.sub(r'RS|R$|RS |R$ ', '', extracted.group(3).strip()),
                        'Cartao': 'Pan',
                        'Tipo de Compra': 'Credito'
                    })

    return pd.DataFrame(fatura)

def converter_formato_data(data_str: str, year: str = None):
    meses = {'JAN': '01', 'FEV':'02', 'MAR':'03', 'ABR':'04', 'MAI':'05', 'JUN':'06', 'JUL':'07', 'AGO':'08', 'SET':'09', 'OUT':'10', 'NOV':'11', 'DEZ':'12'}
    data_str = data_str.upper()
    mes = re.search(r'[A-Za-z]+', data_str)

    if mes:
        mes = mes.group(0)
        data_str = data_str.replace(mes, meses[mes.upper()])
    
    data_str += f" {year}" if year and year not in data_str else ""
    
    return data_str.replace(" ","/")

def to_float(num: str) -> float:
    num = num.replace('.', '').replace(',', '.')

    return float(num)

def generate_uuid(*agr) -> str:
    return str(uuid.uuid4())

def faturas():
    pdf_nubank = 'Nubank_2023-07-23.pdf'
    pdf_inter = 'inter_2023-07.pdf'
    pdf_meliuz = 'meliuz-2023-07.pdf'
    pdf_pan = 'pan_2023-07.pdf'

    fatura_nubank = read_nubank(pdf_nubank)
    fatura_inter = read_inter(pdf_inter)
    fatura_meliuz = read_meliuz(pdf_meliuz)
    fatura_pan = read_pan(pdf_pan)

    faturas = pd.concat([fatura_nubank, fatura_meliuz, fatura_inter, fatura_pan], ignore_index=True)
    faturas['Data'] = faturas['Data'].apply(converter_formato_data, year='2023')
    faturas['Valor'] = faturas['Valor'].apply(to_float)
    faturas['unique_id'] = 'unique_id'
    faturas['unique_id'] = faturas['unique_id'].apply(generate_uuid)

    return faturas

if '__main__' == __name__:
    fatura = faturas() 
    print(fatura[fatura['Movimentacao'].str.contains('Uber')])
    
    