from importlib import import_module

from core.interfaces import Bank


class BankFactory:
    def __init__(self, bank_name: str) -> None:
        self.__name = bank_name.lower()

    def get_instance(self) -> Bank:
        bank_module = import_module(f'core.banks.{self.__name}')
        bank = getattr(bank_module, self.__name.capitalize())

        return bank()
