from models import BillReader
from utils import PathConstants
from os.path import join


def test_bill_reader():
    pdfs = {
        'nubank': join(PathConstants.TEMP, 'Nubank_2023-07-23.pdf'),
        'inter': join(PathConstants.TEMP, 'inter_2023-07.pdf'),
        'pan': join(PathConstants.TEMP, 'pan_2023-07.pdf'),
        'meliuz': join(PathConstants.TEMP, 'meliuz-2023-07.pdf'),
    }

    bill_reader = BillReader(pdfs)
    assert not bill_reader.bill.empty