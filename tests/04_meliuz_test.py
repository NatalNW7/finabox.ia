from models.banks import Meliuz
import pytest
from utils import PathConstants
from os.path import join

@pytest.fixture
def bank():
    pdf_path = join(PathConstants.TEMP, 'meliuz-2023-07.pdf')
    bank = Meliuz(pdf_path)
    return bank

def test_meliuz_credit_card_bill_reader(bank):
    df = bank.read_credit_card_bill()
    assert not df.empty