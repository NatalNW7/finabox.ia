from os.path import join

import pytest

from src.models.banks import Meliuz
from src.utils import PathConstants


@pytest.fixture
def bank():
    pdf_path = join(PathConstants.TEMP, 'meliuz-2023-07.pdf')
    bank = Meliuz(pdf_path)
    return bank


def test_meliuz_credit_card_bill_reader(bank):
    df = bank.read_credit_card_bill()
    assert not df.empty
