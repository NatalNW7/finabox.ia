import tabula
import PyPDF2
import pandas as pd
import re
import json


def get_total_pages(pdf: str) -> int:
    total_pages = 0
    with open(pdf, 'rb') as file:
        pdfReader = PyPDF2.PdfReader(file) 
        total_pages = len(pdfReader.pages)

    return total_pages 

def read_pdf(pdf, pages, header=None) -> pd.DataFrame:
    csv_output = "output.csv"
    
    tabula.convert_into(pdf, csv_output, output_format="csv", pages=pages)
    fatura = pd.read_csv(csv_output, names=header, delimiter=',')

    return fatura

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
    with open('output.txt', 'w') as fatura_txt:
        fatura_txt.write(text)

    with open('output.txt', 'r') as fatura_txt:
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

if '__main__' == __name__:
    pdf_nubank = 'Nubank_2023-07-23.pdf'
    pdf_inter = 'inter_2023-07.pdf'
    pdf_meliuz = 'meliuz-2023-07.pdf'
    pdf_pan = 'pan_2023-07.pdf'

    fatura_nubank = read_nubank(pdf_nubank)
    print(fatura_nubank)
    fatura_inter = read_inter(pdf_inter)
    print(fatura_inter)

    # TODO fazer leitura de pdf pan

            
    
    