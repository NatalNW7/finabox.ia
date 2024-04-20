from abc import ABC, abstractmethod
from os.path import join
from utils import PathConstants
from pandas import DataFrame

class ExtractReaderinterface(ABC):
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