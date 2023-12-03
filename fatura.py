import tabula
import PyPDF2
import pandas as pd


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
    header=['Data', 'Unnamed', 'Movimentação', 'Valor']
    pages = f'4-{get_total_pages(pdf)}'
    fatura = read_pdf(pdf, pages, header)
    fatura.drop(columns=['Unnamed'], inplace=True)
    fatura.dropna(axis=0, inplace=True)

    return fatura

def read_inter(pdf): #-> pd.DataFrame:
    # fatura = tabula.read_pdf(pdf, pages=2, lattice=True)
    fatura = PyPDF2.PdfReader(pdf)

    return fatura

if '__main__' == __name__:
    pdf_nubank = 'Nubank_2023-07-23.pdf'
    pdf_inter = 'inter_2023-07.pdf'
    pdf_meliuz = 'meliuz-2023-07.pdf'
    pdf_pan = 'pan_2023-07.pdf'

    # fatura_nubank = read_nubank(pdf_nubank)
    fatura_inter = read_inter(pdf_inter)

    text = fatura_inter.pages[1].extract_text()
    # print(fatura_inter.pages[1].extract_text())
    print(text)
    with open('teste.txt', 'w') as fatura:
        fatura.write(text)

    import re

    with open('teste.txt', 'r') as fatura:
        text = fatura.readlines()
        print(text)
        for line in text:
            cleaned_line = re.sub(r'\xa0|\x00', ' ', line.strip())
            extracted = re.search(r'^(\d{2}\s\w{3}\s\d{4})(.+)(R\$\s\d.\d{1,},\d{2}|R\$\s\d{1,},\d{2})$', cleaned_line)
            if extracted:
                print(extracted.groups())
                print('data =', extracted.group(1))
                print('movimentação =', extracted.group(2))
                print('valor =', extracted.group(3))

    # TODO terminar funcão de leitura do pdf inter

            
    
    