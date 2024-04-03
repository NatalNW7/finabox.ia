from models.banks import MeliuzBill
import pytest

@pytest.fixture
def bank():
    bank = MeliuzBill()
    bank.load_pdf('meliuz-2023-07.pdf')
    return bank

def test_read_meliuz_bill(bank):
    df = bank.read_bill()
    assert not df.empty