from pandas import concat

from finabox.banks import BankFactory


class StatementReader:
    def __init__(self, csv_files: dict[str, str]) -> None:
        self.__files = csv_files
        self.__statements = []
        self.__statement_reader()

    @property
    def statement(self):
        "Return statement of all banks in a single dataframe"
        return concat(self.__statements, ignore_index=True)

    @property
    def statements(self):
        "Return list of each bank statement"
        return self.__statements

    def __statement_reader(self):
        for bank, file in self.__files.items():
            bank = BankFactory(bank).get_instance()
            bank.set_csv(file)
            statement = bank.read_bank_statement()
            self.__statements.append(statement)
