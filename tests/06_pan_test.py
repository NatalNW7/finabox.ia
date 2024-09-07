from models.banks import Pan
import pytest

@pytest.fixture
def bank():
    pdf_path = 'pan_2023-07.pdf'
    bank = Pan(pdf_path)
    return bank

def test_pan_credit_card_bill_reader(bank):
    df = bank.read_credit_card_bill()
    assert not df.empty