from re import search
from shutil import which
from uuid import uuid4


def convert_date_format(data_str: str, year: str = None) -> str:
    meses = {
        'JAN': '01',
        'FEV': '02',
        'MAR': '03',
        'ABR': '04',
        'MAI': '05',
        'JUN': '06',
        'JUL': '07',
        'AGO': '08',
        'SET': '09',
        'OUT': '10',
        'NOV': '11',
        'DEZ': '12',
    }
    data_str = data_str.upper()
    mes = search(r'[A-Za-z]+', data_str)

    if mes:
        mes = mes.group(0)
        data_str = data_str.replace(mes, meses[mes.upper()])

    data_str += f' {year}' if year and (year not in data_str) else ''

    return data_str.strip().replace(' ', '/')


def to_float(num: str) -> float:
    if isinstance(num, float):
        return num

    num = num.replace('.', '').replace(',', '.').replace('R$', '').strip()
    return float(num)


def generate_uuid(arg) -> str:
    return str(uuid4())


def find_tesseract_path() -> str:
    return which('tesseract')
