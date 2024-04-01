from os.path import join

from pandas import DataFrame
from utils import BillUtils
from re import sub, search
from interfaces import BillInterface

class InterBill(BillInterface):
    def read_bill(self):
        text = self.pdf.pages[1].extract_text()
        dict_fatura = []
        output = join(BASE, "output.txt")

        with open(output, 'w') as file:
            file.write(text)

        with open(output, 'r') as file:
            text = file.readlines()

            for line in text:
                cleaned_line = sub(r'\xa0|\x00', ' ', line.strip())
                extracted = search(r'^(\d{2}\s\w{3}\s\d{4})(.+)(R\$\s\d.\d{1,},\d{2}|R\$\s\d{1,},\d{2})$', cleaned_line)

                if extracted:
                    dict_fatura.append({
                        'DATE': BillUtils.convert_date_format(extracted.group(1).strip()),
                        'TRANSACTION': extracted.group(2).strip(),
                        'PRICE': extracted.group(3).strip().replace('R$ ', ''),
                        'BANK': 'Inter',
                        'PAYMENT_TYPE': 'Credit'
                    })

        return DataFrame(dict_fatura)