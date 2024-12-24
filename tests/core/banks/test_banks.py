from os.path import join

import pytest

from core.utils import PathConstants as pc


@pytest.mark.parametrize(
    'bank',
    [
        (
            'inter',
            join(pc.TEMP, 'cartao-inter.pdf'),
            join(pc.TEMP, 'extrato-inter.csv'),
        ),
        (
            'nubank',
            join(pc.TEMP, 'cartao-nubank.pdf'),
            join(pc.TEMP, 'extrato-nubank.csv'),
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
            join(pc.TEMP, 'cartao-inter.pdf'),
            '',
        ),
        (
            'nubank',
            join(pc.TEMP, 'cartao-nubank.pdf'),
            '',
        ),
        (
            'pan',
            join(pc.TEMP, 'cartao-pan.pdf'),
            '',
        ),
        (
            'meliuz',
            join(pc.TEMP, 'cartao-meliuz.pdf'),
            '',
        ),
    ],
    ids=lambda param: param[0],
    indirect=True,
)
def test_read_credit_card_bill(bank):
    df = bank.read_credit_card_bill()

    assert df.empty == False
