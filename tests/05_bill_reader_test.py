from src.services import CreditCardBillReader


def test_bill_reader():
    pdfs = {
        'nubank': 'Nubank_2023-07-23.pdf',
        'inter': 'inter_2023-07.pdf',
        'pan': 'pan_2023-07.pdf',
        'meliuz': 'meliuz-2023-07.pdf',
    }

    bill_reader = CreditCardBillReader(pdfs)
    assert not bill_reader.bill.empty
