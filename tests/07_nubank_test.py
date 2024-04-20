from models.banks.nubank import NubankBill, NubankExtractReader
import pytest
from utils import PathConstants
from os.path import join


@pytest.fixture
def bank():
    pdf_path = join(PathConstants.TEMP, 'Nubank_2023-07-23.pdf')
    bank = NubankBill()
    bank.load_pdf(pdf_path)
    return bank

@pytest.fixture
def extract():
    csv_file_path = join(PathConstants.TEMP, 'NU_579750386_01JUL2023_31JUL2023.csv')
    extract = NubankExtractReader()
    extract.load_csv(csv_file_path)

    return extract

def test_raise_error_if_file_is_not_pdf(bank):
    with pytest.raises(FileExistsError) as exec_info:
        bank.load_pdf('test.file')

    assert 'This file is not a pdf' in str(exec_info.value)

def test_load_pdf(bank):
    assert bank.pdf != None

def test_read_nubank_bill(bank):
    df = bank.read_bill()
    assert not df.empty

def test_nubank_extract_reader(extract):
    nubank_extract = extract.read_extract()
    print("\n",nubank_extract.head())