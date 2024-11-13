from pandas import DataFrame, concat

from src.models import BankInstance
from src.utils import convert_date_format, generate_uuid, to_float


class CreditCardBillReader:
    def __init__(
        self,
        pdf_files: dict[str, str],
        default_tesseract_cmd=r'/usr/bin/tesseract',
    ) -> None:
        self.__files = pdf_files
        self.__default_tesseract_cmd = default_tesseract_cmd
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
            bank = BankInstance(bank.upper()).get_instance()
            bank.set_pdf(file)
            bill = bank.read_credit_card_bill()
            self.__bills.append(bill)

    def __parsed_bill(self):
        bill = concat(self.__bills, ignore_index=True)
        bill['DATE'] = bill['DATE'].apply(convert_date_format, year='2023')
        bill['PRICE'] = bill['PRICE'].apply(to_float)
        bill['UUID'] = 'UUID'
        bill['UUID'] = bill['UUID'].apply(generate_uuid)

        return bill
