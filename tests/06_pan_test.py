from models.banks import PanBill
import pytest

@pytest.fixture
def bank():
    bank = PanBill()
    bank.load_pdf('pan_2023-07.pdf')
    return bank

def test_extract_text_from_pdf(bank):
    text = bank._extract_text()

    assert len(text) != 0

def test_read_pan_bill(bank):
    df = bank.read_bill()
    assert not df.empty