from pandas import DataFrame, concat
from utils import BillUtils
from interfaces import BillInterface
from models.banks import (
    nubank,
    inter,
    meliuz,
    pan
)

class BillReader:
    def __init__(self, pdf_files: dict[str, str], default_tesseract_cmd=r'/usr/bin/tesseract') -> None:
        self.__files = pdf_files
        self.__default_tesseract_cmd = default_tesseract_cmd
        self.__BANKS: dict[str, BillInterface] = {
            'nubank': nubank.NubankBill(),
            'inter': inter.InterBill(),
            'pan': pan.PanBill(default_tesseract_cmd=self.__default_tesseract_cmd),
            'meliuz': meliuz.MeliuzBill()
        }
        self.__bills = []
        self.__bills_reader()

    @property
    def bills(self) -> list[DataFrame]:
        "Return list of each bank bill"
        return self.__bills

    @property
    def bill(self) -> DataFrame:
        "Return bill of all banks in a single dataframe"
        return self.__parsed_bill()

    def __bills_reader(self):
        for bank, file in self.__files.items():
            bank_bill = self.__BANKS[bank.lower()]
            bank_bill.load_pdf(file)
            self.__bills.append(bank_bill.read_bill())

    def __parsed_bill(self):
        bill = concat(self.__bills, ignore_index=True)
        bill['DATE'] = bill['DATE'].apply(BillUtils.convert_date_format, year='2023')
        bill['PRICE'] = bill['PRICE'].apply(BillUtils.to_float)
        bill['UUID'] = 'UUID'
        bill['UUID'] = bill['UUID'].apply(BillUtils.generate_uuid)

        return bill
    