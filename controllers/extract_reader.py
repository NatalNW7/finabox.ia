from utils import PathConstants, file
from os.path import join
from pandas import concat
from interfaces import ExtractReaderinterface
from models.banks import (
    nubank,
    inter,
    meliuz,
    pan
)

class ExtractReader:
    def __init__(self, csv_files: dict[str, str]) -> None:
        self.__files = csv_files
        self.__BANKS: dict[str, ExtractReaderinterface] = {
            'nubank': nubank.NubankExtractReader(),
            'inter': inter.InterExtractReader(),
            'pan': pan.PanExtractReader(),
            'meliuz': meliuz.MeliuzExtractReader()
        }

        self.__extracts = []
        self.__extract_reader()

    @property
    def extract(self):
        "Return extract of all banks in a single dataframe"
        return concat(self.__extracts, ignore_index=True)
    
    @property
    def extracts(self):
        "Return list of each bank extract"
        return self.__extracts

    def __extract_reader(self):
        for bank, file in self.__files.items():
            bank_extract = self.__BANKS[bank.lower()]
            bank_extract.load_csv(file)
            self.__extracts.append(bank_extract.read_extract())
