import tabula
from PyPDF2 import PdfReader
import pandas as pd
import re
import os
from pdf2image import convert_from_path
from pytesseract import pytesseract
import uuid
from abc import ABC, abstractmethod


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

class BillUtils():
    @staticmethod
    def convert_date_format(data_str: str, year: str = None):
        meses = {'JAN': '01', 'FEV':'02', 'MAR':'03', 'ABR':'04', 'MAI':'05', 'JUN':'06', 'JUL':'07', 'AGO':'08', 'SET':'09', 'OUT':'10', 'NOV':'11', 'DEZ':'12'}
        data_str = data_str.upper()
        mes = re.search(r'[A-Za-z]+', data_str)

        if mes:
            mes = mes.group(0)
            data_str = data_str.replace(mes, meses[mes.upper()])
        
        data_str += f" {year}" if year and year not in data_str else ""
        
        return data_str.replace(" ","/")

    @staticmethod
    def to_float(num: str) -> float:
        num = num.replace('.', '').replace(',', '.')
        return float(num)

    @staticmethod
    def generate_uuid(arg) -> str:
        return str(uuid.uuid4())

class BillInterface(ABC):

    def __init__(self, file_path: str) -> None:
        super().__init__()
        self.pdf = Pdf(file_path)

    @abstractmethod
    def read_bill(self) -> pd.DataFrame: ...

class NubankBill(BillInterface):
    def read_bill(self) -> pd.DataFrame:
        header=['DATE', 'Unnamed', 'TRANSACTION', 'PRICE']
        pages = f'4-{self.pdf.total_pages}'
        bill = self.pdf.to_dataframe(pages, header)
        bill.drop(columns=['Unnamed'], inplace=True)
        bill.dropna(axis=0, inplace=True)
        bill['BANK'] = 'Nubank'
        bill['PAYMENT_TYPE'] = 'Credit'

        return bill

class InterBill(BillInterface):
    def read_bill(self):
        text = self.pdf.pages[1].extract_text()
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
                        'DATE': BillUtils.convert_date_format(extracted.group(1).strip()),
                        'TRANSACTION': extracted.group(2).strip(),
                        'PRICE': extracted.group(3).strip().replace('R$ ', ''),
                        'BANK': 'Inter',
                        'PAYMENT_TYPE': 'Credit'
                    })

        return pd.DataFrame(dict_fatura)

class MeliuzBill(BillInterface):
    def read_bill(self):
        pages = f'3-{self.pdf.total_pages}'
        df = self.pdf.to_dataframe(pages=pages)
        df = df[['Unnamed: 0','Unnamed: 1','Unnamed: 2']]
        df = df.rename(columns={'Unnamed: 0': 'DATE', 'Unnamed: 1': 'TRANSACTION', 'Unnamed: 2': 'PRICE'})
        df = df.dropna()
        df = df.reset_index(drop=True)
        df['PRICE'] = df['PRICE'].str.replace('R$ ', '')
        df['BANK'] = 'Meliuz'
        df['PAYMENT_TYPE'] = 'Credit'
        
        return df
    
class PanBill(BillInterface):
    def read_bill(self) -> pd.DataFrame:
        pytesseract.tesseract_cmd = r'/usr/bin/tesseract'  # Substitua pelo caminho correto
        output = os.path.join(BASE, 'output.txt')
        bill = []
        images = convert_from_path(self.pdf.file_path)

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
                            'DATE': BillUtils.convert_date_format(extracted.group(1).strip(), "2023"),
                            'TRANSACTION': extracted.group(2).strip(),
                            'PRICE': re.sub(r'RS|R$|RS |R$ ', '', extracted.group(3).strip()),
                            'BANK': 'Pan',
                            'PAYMENT_TYPE': 'Credit'
                        })

        return pd.DataFrame(bill)

from enum import Enum

class Bank(Enum):
    NUBANK = NubankBill



class BillReader:
    def __init__(self, files: dict[str, str]) -> None:
        self.__files = files
        self.__BANKS = {
            'nubank': NubankBill,
            'inter': InterBill,
            'pan': PanBill,
            'meliuz': MeliuzBill
        }
        self.bills = []

    def bill_reader(self):
        for bank, file in self.__files.items():
            self.bills.append(self.__BANKS[bank.lower()](file).read_bill())

        bill = pd.concat(self.bills, ignore_index=True)
        bill['DATE'] = bill['DATE'].apply(BillUtils.convert_date_format, year='2023')
        bill['PRICE'] = bill['PRICE'].apply(BillUtils.to_float)
        bill['UUID'] = 'UUID'
        bill['UUID'] = bill['UUID'].apply(BillUtils.generate_uuid)

        return bill

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

    # bill = bill_reader(nubank='Nubank_2023-07-23.pdf', inter='inter_2023-07.pdf', meliuz='meliuz-2023-07.pdf', pan='pan_2023-07.pdf') 
    # print(bill)
    
    