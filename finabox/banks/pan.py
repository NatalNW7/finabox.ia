from re import search, sub

from pandas import DataFrame
from pdf2image import convert_from_path
from pytesseract import pytesseract

from finabox.interfaces import Bank, CreditCardBillReader
from finabox.utils import (
    PathConstants,
    find_tesseract_path,
)
from finabox.utils.file import reader, writer


class PanCreditCardBillReader(CreditCardBillReader):
    def __init__(self, default_tesseract_cmd=find_tesseract_path()) -> None:
        super().__init__()
        self.__default_tesseract_cmd = default_tesseract_cmd

    def _statement_text(self) -> list[str]:
        pytesseract.tesseract_cmd = self.__default_tesseract_cmd
        images = convert_from_path(self.pdf.file_path)

        for i, image in enumerate(images):
            i += 1
            if i == 3:
                image_content = pytesseract.image_to_string(image)
                writer(image_content, PathConstants.OUTPUT_TXT)
                break

        return reader(PathConstants.OUTPUT_TXT)

    def read_bill(self):
        dict_fatura = []
        text = self._statement_text()

        for line in text:
            line = line.strip()
            if line:
                statemented = search(
                    r'^(\d{0,}\/\d{0,})(.+)(RS\d{0,},\d{0,}|RS\s\d{0,},\d{0,}|R\$\d{0,},\d{0,}|R\$\s\d{0,},\d{0,})$',
                    line,
                )
                if statemented:
                    dict_fatura.append({
                        'DATE': statemented.group(1).strip(),
                        'DESCRIPTION': statemented.group(2).strip(),
                        'PRICE': sub(
                            r'RS|R$|RS |R$ ', '', statemented.group(3).strip()
                        ),
                        'BANK': 'Pan',
                        'PAYMENT_TYPE': 'Credit',
                    })

        return DataFrame(dict_fatura)


class Pan(Bank):
    def __init__(self, pdf_file: str = None, csv_file: str = None) -> None:
        super().__init__(pdf_file, csv_file)
        self._bill_reader = PanCreditCardBillReader()
