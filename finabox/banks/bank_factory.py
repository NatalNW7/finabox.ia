from importlib import import_module

from finabox.interfaces import Bank


class BankFactory:
    def __init__(self, bank_name: str) -> None:
        self.__name = bank_name.lower()

    def get_instance(self) -> Bank:
        bank_module = import_module(f'finabox.banks.{self.__name}')
        bank = getattr(bank_module, self.__name.capitalize())

        return bank()
