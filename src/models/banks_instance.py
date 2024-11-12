from importlib import import_module

from src.interfaces import Bank


class BankInstance:
    def __init__(self, bank_name: str) -> None:
        self.__name = bank_name.lower()

    def get_instance(self) -> Bank:
        bank_module = import_module(f'src.models.banks.{self.__name}')
        bank = getattr(bank_module, self.__name.capitalize())

        return bank()
