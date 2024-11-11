from abc import ABC, abstractmethod
from os.path import join

from pandas import DataFrame

from models import Pdf
from utils import PathConstants


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
