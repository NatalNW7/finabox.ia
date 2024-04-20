from models.banks.inter import InterBill, InterExtractReader
import pytest
from utils import PathConstants
from os.path import join

@pytest.fixture
def bank():
    pdf_path = join(PathConstants.TEMP, 'inter_2023-07.pdf')
    bank = InterBill()
    bank.load_pdf(pdf_path)
    return bank

@pytest.fixture
def extract():
    csv_file_path = join(PathConstants.TEMP, 'Extrato-01-07-2023-a-31-07-2023.csv')
    extract = InterExtractReader()
    extract.load_csv(csv_file_path)

    return extract

def test_extract_text_from_pdf(bank):
    text = bank._extract_text()

    assert len(text) != 0

def test_read_inter_bill(bank):
    df = bank.read_bill()
    assert not df.empty

def test_inter_extract_reader(extract):
    inter_extract = extract.read_extract()
    print("\n",inter_extract.head())