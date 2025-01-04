from os.path import join
from re import fullmatch

import pytest

from finabox.interfaces import Bank
from finabox.utils import PathConstants as pc


def expected_date_format(date: str):
    match_str = r'\d{2,2}\/\d{2,2}\/\d{4,4}'
    return fullmatch(match_str, date)


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
def test_read_statement(bank: Bank):
    df = bank.read_bank_statement()
    # df.to_csv(f'{bank.__class__.__name__}-extrato.csv', index=False)
    assert df.empty == False
    assert expected_date_format(df['DATE'].loc[0])


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
def test_read_credit_card_bill(bank: Bank):
    df = bank.read_credit_card_bill(year='2023')
    # df.to_csv(f'{bank.__class__.__name__}-cartao.csv', index=False)
    assert df.empty == False
    assert expected_date_format(df['DATE'].loc[0])
