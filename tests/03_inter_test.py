from os.path import join

import pytest

from models.banks import Inter
from utils import PathConstants


@pytest.fixture
def bank():
    pdf_path = join(PathConstants.TEMP, 'inter_2023-07.pdf')
    csv_file_path = join(
        PathConstants.TEMP, 'Extrato-01-07-2023-a-31-07-2023.csv'
    )
    bank = Inter(pdf_path, csv_file_path)
    return bank


def test_inter_credit_card_bill_reader(bank):
    df = bank.read_credit_card_bill()
    assert not df.empty


def test_inter_extract_reader(bank):
    inter_extract = bank.read_bank_extract()
    print('\n', inter_extract.head())
