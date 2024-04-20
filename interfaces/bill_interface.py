from abc import ABC, abstractmethod
from models import Pdf
from pandas import DataFrame
from os.path import join
from utils import PathConstants


class BillInterface(ABC):
    def __init__(self) -> None:
        super().__init__()
        self.pdf = None

    def load_pdf(self, file: str):
        if not '.pdf' in file:
            raise FileExistsError('This file is not a pdf')
        self.pdf = Pdf(join(PathConstants.TEMP, file))

    @abstractmethod
    def read_bill(self) -> DataFrame: ...
