from pandas import concat
from models import BankInstance

class BankExtractReader:
    def __init__(self, csv_files: dict[str, str]) -> None:
        self.__files = csv_files
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
            bank = BankInstance(bank.upper()).get_instance()
            bank.set_csv(file)
            extract = bank.read_bank_extract()
            self.__extracts.append(extract)
