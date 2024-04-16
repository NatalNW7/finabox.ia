from models.banks import NubankBill
import pytest
from utils import PathConstants
from os.path import join

@pytest.fixture
def bank():
    pdf_path = join(PathConstants.TEMP, 'Nubank_2023-07-23.pdf')
    bank = NubankBill()
    bank.load_pdf(pdf_path)
    return bank

def test_raise_error_if_file_is_not_pdf(bank):
    with pytest.raises(FileExistsError) as exec_info:
        bank.load_pdf('test.file')

    assert 'This file is not a pdf' in str(exec_info.value)

def test_load_pdf(bank):
    assert bank.pdf != None

def test_read_nubank_bill(bank):
    df = bank.read_bill()
    assert not df.empty