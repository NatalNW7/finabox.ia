from abc import ABC, abstractmethod
from os.path import join

from pandas import DataFrame

from src.utils import PathConstants, Pdf


class CreditCardBillReader(ABC):
    def __init__(self) -> None:
        super().__init__()
        self.pdf = None

    def load_pdf(self, file: str):
        if '.pdf' not in file:
            raise FileExistsError('This file is not a pdf')
        self.pdf = Pdf(join(PathConstants.TEMP, file))

    @abstractmethod
    def read_bill(self) -> DataFrame: ...


class BankExtractReader(ABC):
    def __init__(self) -> None:
        self._extract_df = None

    def load_csv(self, csv_file: str):
        self._extract_df = self._read_csv(join(PathConstants.TEMP, csv_file))

    @abstractmethod
    def read_extract() -> DataFrame: ...

    @abstractmethod
    def _read_csv(self, csv_file: str) -> DataFrame: ...

    def _change_columns(self, columns):
        self._extract_df.columns = columns


class Bank(ABC):
    def __init__(self, pdf_file: str = None, csv_file: str = None) -> None:
        self._pdf_file = pdf_file
        self._csv_file = csv_file
        self._bill_reader: CreditCardBillReader = None
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