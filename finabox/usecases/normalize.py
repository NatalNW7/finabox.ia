from json import load
from os.path import join

from pandas import DataFrame, concat

from finabox.banks import BankFactory
from finabox.classifier import Classifier
from finabox.interfaces import Bank
from finabox.schemas import BankInfo, FileType


class Normalize:
    def __init__(self, info: BankInfo):
        self.bank_info = info
        self.classifier = Classifier()

    def normalized(self):
        bank = BankFactory(self.bank_info.name).get_instance()

        data = []
        for file in self.bank_info.files:
            if file.type == FileType.PDF:
                data.append(
                    self.normalize_credit_card_bill(bank, file.name, file.year)
                )

        data = concat(data)
        self.set_estabilishment(data)

    def normalize_statement(self, bank: Bank, file: str):
        bank.set_csv(file)
        return bank.read_bank_statement()

    def normalize_credit_card_bill(
        self, bank: Bank, file: str, year: str = None
    ):
        bank.set_pdf(file)
        return bank.read_credit_card_bill(year)

    def set_estabilishment(self, data: DataFrame):
        with open(
            join('resources', 'estabilishments-mapping.json'), 'r'
        ) as file:
            estabilishments_mapping: dict = load(file)

        self.classifier.setup_resource(estabilishments_mapping)
        estabilishments = self.classifier.classify(
            data['description'].tolist()
        )
        estabilishments = [
            estabilishment[0] if estabilishment else ''
            for estabilishment in estabilishments
        ]
        data['estabilishment'] = estabilishments
        print(data.head(50))
