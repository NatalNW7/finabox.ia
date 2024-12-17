from os.path import join

import pytest

from core.utils import PathConstants as pc


@pytest.mark.parametrize(
    'bank',
    [
        (
            'inter',
            join(pc.TEMP, 'inter_2023-07.pdf'),
            join(pc.TEMP, 'Extrato-01-07-2023-a-31-07-2023.csv'),
        ),
        (
            'nubank',
            join(pc.TEMP, 'Nubank_2023-07-23.pdf'),
            join(pc.TEMP, 'NU_579750386_01JUL2023_31JUL2023.csv'),
        ),
    ],
    ids=lambda param: param[0],
    indirect=True,
)
def test_read_statement(bank):
    df = bank.read_bank_statement()

    assert df.empty == False


@pytest.mark.parametrize(
    'bank',
    [
        (
            'inter',
            join(pc.TEMP, 'inter_2023-07.pdf'),
            join(pc.TEMP, 'Extrato-01-07-2023-a-31-07-2023.csv'),
        ),
        (
            'nubank',
            join(pc.TEMP, 'Nubank_2023-07-23.pdf'),
            join(pc.TEMP, 'NU_579750386_01JUL2023_31JUL2023.csv'),
        ),
        (
            'pan',
            join(pc.TEMP, 'pan_2023-07.pdf'),
            '',
        ),
        (
            'meliuz',
            join(pc.TEMP, 'meliuz-2023-07.pdf'),
            '',
        ),
    ],
    ids=lambda param: param[0],
    indirect=True,
)
def test_read_credit_card_bill(bank):
    df = bank.read_credit_card_bill()

    assert df.empty == False
