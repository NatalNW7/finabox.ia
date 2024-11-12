from pytest import mark

from src.utils import convert_date_format, to_float


@mark.parametrize(
    'input,output',
    [
        ('18 jun 2023', '18/06/2023'),
        ('28 abr 2023', '28/04/2023'),
        ('16 mai 2023', '16/05/2023'),
        ('16 JUN', '16/06/2023'),
        ('02 JUL', '02/07/2023'),
        ('16/02', '16/02/2023'),
        ('05/06', '05/06/2023'),
        ('20/06', '20/06/2023'),
        ('01/07', '01/07/2023'),
    ],
)
def test_convert_date_format(input, output):
    assert convert_date_format(input, year='2023') == output


@mark.parametrize(
    'input,output',
    [
        ('29,64', 29.64),
        ('3.779,94', 3779.94),
        ('9,44', 9.44),
        ('30,00', 30.00),
        ('667,40', 667.40),
        ('123', 123),
    ],
)
def test_to_float(input, output):
    assert to_float(input) == output
