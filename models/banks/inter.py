

from pandas import DataFrame
from utils import BillUtils
from re import sub, search
from interfaces import BillInterface
from utils.file import writer, reader

class InterBill(BillInterface):
    def _extract_text(self) -> list[str]:
        text = self.pdf.pages[1].extract_text()

        if writer(text):
            lines = reader()
        else:
            raise Exception("Error to write content")
       
        return lines
 
    def read_bill(self):
        dict_fatura = []
        text = self._extract_text()
        
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