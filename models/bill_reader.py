from pandas import DataFrame, concat
from utils import BillUtils
from interfaces import BillInterface
from .banks import (
    InterBill,
    NubankBill,
    MeliuzBill,
    PanBill
)

class BillReader:
    def __init__(self, files: dict[str, str]) -> None:
        self.__files = files
        self.__BANKS: dict[str, BillInterface] = {
            'nubank': NubankBill(),
            'inter': InterBill(),
            'pan': PanBill(),
            'meliuz': MeliuzBill()
        }
        self.__bills = []
        self.bills_reader()

    @property
    def bills(self) -> list[DataFrame]:
        "Return list of each bank bill"
        return self.__bills

    @property
    def bill(self) -> DataFrame:
        "Return bill of all banks in a single dataframe"
        return self.__parsed_bill()

    def bills_reader(self):
        for bank, file in self.__files.items():
            bank_bill = self.__BANKS[bank.lower()]
            bank_bill.load_pdf(file)
            self.__bills.append(bank_bill.read_bill())

    def __concat(self) -> DataFrame:
        return concat(self.__bills, ignore_index=True)

    def __parsed_bill(self):
        bill = self.__concat()
        bill['DATE'] = bill['DATE'].apply(BillUtils.convert_date_format, year='2023')
        bill['PRICE'] = bill['PRICE'].apply(BillUtils.to_float)
        bill['UUID'] = 'UUID'
        bill['UUID'] = bill['UUID'].apply(BillUtils.generate_uuid)

        return bill
    