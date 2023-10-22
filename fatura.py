import tabula
import logging
import PyPDF2
import pandas as pd


def get_total_pages(pdf: str) -> int:
    total_pages = 0
    with open(pdf, 'rb') as file:
        pdfReader = PyPDF2.PdfReader(file) 
        total_pages = len(pdfReader.pages)

    return total_pages 

def read_pdf(pdf: str) -> pd.DataFrame:
    csv_output = "output.csv"
    header=['Data', 'Unnamed', 'Nome', 'Valor']
    total_pages = get_total_pages(pdf)
    pages = f'4-{total_pages}'

    tabula.convert_into(pdf, csv_output, output_format="csv", pages=pages)
    fatura = pd.read_csv(csv_output, names=header, delimiter=',')
    fatura.drop(columns=['Unnamed'], inplace=True)
    fatura.dropna(axis=0, inplace=True)

    return fatura


pdf = 'Nubank_2023-07-23.pdf'

fatura = read_pdf(pdf)

print(fatura)
