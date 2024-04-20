from models.banks.meliuz import MeliuzBill
import pytest
from utils import PathConstants
from os.path import join

@pytest.fixture
def bank():
    pdf_path = join(PathConstants.TEMP, 'meliuz-2023-07.pdf')
    bank = MeliuzBill()
    bank.load_pdf(pdf_path)
    return bank

def test_read_meliuz_bill(bank):
    df = bank.read_bill()
    assert not df.empty