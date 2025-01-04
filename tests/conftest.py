from os import environ, makedirs
from shutil import rmtree

import pytest

from finabox.banks import BankFactory
from finabox.utils import PathConstants as pc


@pytest.fixture(scope='function')
def bank(request):
    bank_type, pdf_file, csv_file = request.param
    bank_instance = BankFactory(bank_type).get_instance()
    bank_instance.set_pdf(pdf_file)
    bank_instance.set_csv(csv_file)

    return bank_instance


def pytest_sessionfinish(session, exitstatus):
    env = environ.get('ENVIROMENT', 'local')

    if env != 'local':
        rmtree(pc.TEMP)
        makedirs(pc.TEMP)
        print('\nFiles from temp folder was deleted.')
