from os.path import join

import pytest

from src.models.banks.nubank import Nubank
from src.utils import PathConstants


@pytest.fixture
def bank():
    pdf_path = join(PathConstants.TEMP, 'Nubank_2023-07-23.pdf')
    csv_file_path = join(
        PathConstants.TEMP, 'NU_579750386_01JUL2023_31JUL2023.csv'
    )
    bank = Nubank(pdf_path, csv_file_path)
    return bank


def test_nubank_credit_card_bill_reader(bank):
    df = bank.read_credit_card_bill()
    assert not df.empty


def test_nubank_extract_reader(bank):
    nubank_extract = bank.read_bank_extract()
    print('\n', nubank_extract.head())
