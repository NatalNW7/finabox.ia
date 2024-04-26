from interfaces import Bank
from models.banks import (
    Nubank,
    Inter,
    Pan,
    Meliuz
)

class BankInstance:
    def __init__(self, bank_name: str) -> None:
        self.__name = bank_name
        self.__BANKS = {
            'NUBANK': Nubank(),
            'INTER': Inter(),
            'PAN': Pan(),
            'MELIUZ': Meliuz(),
        }

    def get_instance(self) -> Bank:
        return self.__BANKS[self.__name]