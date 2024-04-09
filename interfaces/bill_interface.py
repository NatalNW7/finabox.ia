from abc import ABC, abstractmethod
from models import Pdf
from pandas import DataFrame


class BillInterface(ABC):
    def __init__(self) -> None:
        super().__init__()
        self.pdf = None

    def load_pdf(self, file_path: str):
        if not '.pdf' in file_path:
            raise FileExistsError('This file is not a pdf')
        self.pdf = Pdf(file_path)

    @abstractmethod
    def read_bill(self) -> DataFrame: ...
