from controllers import Categorize, CreditCardBillReader
import pytest

@pytest.fixture
def categorize():
    pdfs = {
        'nubank': 'Nubank_2023-07-23.pdf',
        'inter': 'inter_2023-07.pdf',
        'pan': 'pan_2023-07.pdf',
        'meliuz': 'meliuz-2023-07.pdf',
    }

    bill_reader = CreditCardBillReader(pdfs)
    categorize = Categorize(bill_reader.bill)

    return categorize

def test_set_establishments(categorize):
    bill_with_establishments = categorize.set_establishments(inplace=False)

    assert check_columns_exists(['ESTABLISHMENT'], bill_with_establishments.columns)

def test_set_categories(categorize):
    categorize.set_establishments()
    bill_with_categories = categorize.set_categories()

    assert check_columns_exists(['CATEGORY'], bill_with_categories.columns)

def test_if_bill_is_categorized(categorize):
    categorized_bill = categorize.categorized_bill

    assert check_columns_exists(['ESTABLISHMENT', 'CATEGORY'], categorized_bill.columns)

def check_columns_exists(columns_to_check, df_columns):
    return set(columns_to_check).issubset(df_columns)