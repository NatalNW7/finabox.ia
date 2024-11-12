from os.path import join

import pytest
from pandas import DataFrame

from src.utils import PathConstants, Pdf
from src.utils.file import reader


@pytest.fixture
def pdf():
    pdf_path = join(PathConstants.TEMP, 'Nubank_2023-07-23.pdf')
    pdf = Pdf(pdf_path)
    return pdf


@pytest.fixture
def pages(pdf):
    return f'4-{pdf.total_pages}'


def test_convert_pdf_to_dataframe(pdf, pages):
    df = pdf.to_dataframe(pages)

    assert isinstance(df, DataFrame)


def test_check_if_csv_content_was_deleted_after_convert_pdf_to_dataframe(
    pdf, pages
):
    df = pdf.to_dataframe(pages)

    assert reader(PathConstants.OUTPUT_CSV) == ['content was deleted']
