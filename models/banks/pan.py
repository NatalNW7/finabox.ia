from pytesseract import pytesseract
from pdf2image import convert_from_path
from os.path import join
from interfaces import BillInterface
from re import search, sub
from utils import BillUtils
from pandas import DataFrame
from utils import temp_path

class PanBill(BillInterface):
    def _extract_text(self) -> list[str]:
        pytesseract.tesseract_cmd = r'/usr/bin/tesseract'
        output = join(temp_path(), 'output.txt')
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
        
        return lines

    def read_bill(self):
        dict_fatura = []
        text = self._extract_text()

        for line in text:
            line = line.strip()
            if line:
                extracted = search(r'^(\d{0,}\/\d{0,})(.+)(RS\d{0,},\d{0,}|RS\s\d{0,},\d{0,}|R\$\d{0,},\d{0,}|R\$\s\d{0,},\d{0,})$', line)
                if extracted:
                    dict_fatura.append({
                        'DATE': BillUtils.convert_date_format(extracted.group(1).strip(), "2023"),
                        'TRANSACTION': extracted.group(2).strip(),
                        'PRICE': sub(r'RS|R$|RS |R$ ', '', extracted.group(3).strip()),
                        'BANK': 'Pan',
                        'PAYMENT_TYPE': 'Credit'
                    })

        return DataFrame(dict_fatura)
