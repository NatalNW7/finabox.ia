from models.banks import PanBill
import pytest
from utils import PathConstants
from os.path import join

@pytest.fixture
def bank():
    pdf_path = join(PathConstants.TEMP, 'pan_2023-07.pdf')
    bank = PanBill()
    bank.load_pdf(pdf_path)
    return bank

def test_extract_text_from_pdf(bank):
    text = bank._extract_text()

    assert len(text) != 0

def test_read_pan_bill(bank):
    df = bank.read_bill()
    assert not df.empty