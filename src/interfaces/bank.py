from pandas import DataFrame
from abc import ABC
from interfaces import CreditCardBillReader, BankExtractReader

class Bank(ABC):
    def __init__(self, pdf_file: str = None, csv_file: str = None) -> None:
        self._pdf_file = pdf_file
        self._csv_file = csv_file
        self._bill_reader: CreditCardBillReader =  None
        self._extract_reader: BankExtractReader = None

    def set_pdf(self, pdf_file: str):
        self._pdf_file = pdf_file

    def set_csv(self, csv_file: str):
        self._csv_file = csv_file

    def read_credit_card_bill(self) -> DataFrame:
        self._bill_reader.load_pdf(self._pdf_file)
        bill = self._bill_reader.read_bill()

        return bill

    def read_bank_extract(self) -> DataFrame:
        self._extract_reader.load_csv(self._csv_file)
        extract = self._extract_reader.read_extract()

        return extract