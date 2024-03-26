import tabula
from PyPDF2 import PdfReader
import pandas as pd
import re
import os
from pdf2image import convert_from_path
from pytesseract import pytesseract
import uuid
from abc import abstractmethod

BASE =  os.path.join(os.getcwd(), 'temp')

class Pdf(PdfReader):
    def __init__(self, file_path) -> None:
        super().__init__(file_path)
        self.file_path = file_path
    
    @property
    def total_pages(self) -> int:
        return len(self.pages) 
    
    def to_dataframe(self, pages, header=None) -> pd.DataFrame:
        dfs = tabula.io.read_pdf(self.file_path, pages=pages)

        if len(dfs) > 1:
            output_file = os.path.join(BASE, "output.csv")
            tabula.convert_into(self.file_path, output_file, output_format="csv", pages=pages)
            df = pd.read_csv(output_file, names=header, delimiter=',')

            return df

        return dfs[0]

class BillReader(Pdf):
    def convert_date_format(self, data_str: str, year: str = None):
        meses = {'JAN': '01', 'FEV':'02', 'MAR':'03', 'ABR':'04', 'MAI':'05', 'JUN':'06', 'JUL':'07', 'AGO':'08', 'SET':'09', 'OUT':'10', 'NOV':'11', 'DEZ':'12'}
        data_str = data_str.upper()
        mes = re.search(r'[A-Za-z]+', data_str)

        if mes:
            mes = mes.group(0)
            data_str = data_str.replace(mes, meses[mes.upper()])
        
        data_str += f" {year}" if year and year not in data_str else ""
        
        return data_str.replace(" ","/")

class NubankBill(BillReader):
    def read_bill(self) -> pd.DataFrame:
        header=['DATE', 'Unnamed', 'TRANSACTION', 'PRICE']
        pages = f'4-{self.total_pages}'
        bill = self.to_dataframe(pages, header)
        bill.drop(columns=['Unnamed'], inplace=True)
        bill.dropna(axis=0, inplace=True)
        bill['BANK'] = 'Nubank'
        bill['PAYMENT_TYPE'] = 'Credit'

        return bill

class InterBill(BillReader):
    def read_bill(self):
        text = self.pages[1].extract_text()
        dict_fatura = []
        output = os.path.join(BASE, "output.txt")

        with open(output, 'w') as file:
            file.write(text)

        with open(output, 'r') as file:
            text = file.readlines()

            for line in text:
                cleaned_line = re.sub(r'\xa0|\x00', ' ', line.strip())
                extracted = re.search(r'^(\d{2}\s\w{3}\s\d{4})(.+)(R\$\s\d.\d{1,},\d{2}|R\$\s\d{1,},\d{2})$', cleaned_line)

                if extracted:
                    dict_fatura.append({
                        'DATE': self.convert_date_format(extracted.group(1).strip()),
                        'TRANSACTION': extracted.group(2).strip(),
                        'PRICE': extracted.group(3).strip().replace('R$ ', ''),
                        'BANK': 'Inter',
                        'PAYMENT_TYPE': 'Credit'
                    })

        return pd.DataFrame(dict_fatura)

class MeliuzBill(BillReader):
    def read_bill(self):
        pages = f'3-{self.total_pages}'
        df = self.to_dataframe(pages=pages)
        df = df[['Unnamed: 0','Unnamed: 1','Unnamed: 2']]
        df = df.rename(columns={'Unnamed: 0': 'DATE', 'Unnamed: 1': 'TRANSACTION', 'Unnamed: 2': 'PRICE'})
        df = df.dropna()
        df = df.reset_index(drop=True)
        df['PRICE'] = df['PRICE'].str.replace('R$ ', '')
        df['BANK'] = 'Meliuz'
        df['PAYMENT_TYPE'] = 'Credit'
        
        return df
class PanBill(BillReader):
    def read_bill(self) -> pd.DataFrame:
        pytesseract.tesseract_cmd = r'/usr/bin/tesseract'  # Substitua pelo caminho correto
        output = os.path.join(BASE, 'output.txt')
        bill = []
        images = convert_from_path(self.file_path)

        for i, image in enumerate(images):
            i += 1
            
            if i == 3:
                image_content = pytesseract.image_to_string(image)
                with open(output, 'w') as file:
                    file.write(image_content)

                break
                    
        with open(output, 'r') as file:
            lines = file.readlines()
            for line in lines:
                line = line.strip()
                if line:
                    extracted = re.search(r'^(\d{0,}\/\d{0,})(.+)(RS\d{0,},\d{0,}|RS\s\d{0,},\d{0,}|R\$\d{0,},\d{0,}|R\$\s\d{0,},\d{0,})$', line)

                    if extracted:
                        bill.append({
                            'DATE': self.convert_date_format(extracted.group(1).strip(), "2023"),
                            'TRANSACTION': extracted.group(2).strip(),
                            'PRICE': re.sub(r'RS|R$|RS |R$ ', '', extracted.group(3).strip()),
                            'BANK': 'Pan',
                            'PAYMENT_TYPE': 'Credit'
                        })

        return pd.DataFrame(bill)


    def to_float(self, num: str) -> float:
        num = num.replace('.', '').replace(',', '.')

        return float(num)

    def generate_uuid(self, *args) -> str:
        return str(uuid.uuid4())

def faturas(**files: str):
    BILLS = {
        'NUBANK':...,
        'INTER':...,
        'PAN':...,
        'MELIUZ':...
    }
    
    nubank = read_nubank(pdf_nubank)
    inter = read_inter(pdf_inter)
    meliuz = read_meliuz(pdf_meliuz)
    pan = read_pan(pdf_pan)

    bills = pd.concat([nubank, meliuz, inter, pan], ignore_index=True)
    bills['DATE'] = bills['DATE'].apply(convert_date_format, year='2023')
    bills['PRICE'] = bills['PRICE'].apply(to_float)
    bills['UUID'] = 'UUID'
    bills['UUID'] = bills['UUID'].apply(generate_uuid)

    return bills

if '__main__' == __name__:
    pdf_nubank = 'Nubank_2023-07-23.pdf'
    pdf_inter = 'inter_2023-07.pdf'
    pdf_meliuz = 'meliuz-2023-07.pdf'
    pdf_pan = 'pan_2023-07.pdf'

    nubank = NubankBill(pdf_nubank).read_bill()
    print(nubank)
    inter = InterBill(pdf_inter).read_bill()
    print(inter)
    meliuz = MeliuzBill(pdf_meliuz).read_bill()
    print(meliuz)
    pan = PanBill(pdf_pan).read_bill()
    print(pan)
    # fatura = faturas() 
    # print(fatura[fatura['TRANSACTION'].str.contains('Uber')])
    
    