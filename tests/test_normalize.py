from os.path import join

from finabox.schemas import BankInfo, FileInfo, FileType
from finabox.usecases.normalize import Normalize
from finabox.utils import PathConstants as pc


def test_normalzie():
    file_info = FileInfo(
        name=join(pc.TEMP, 'cartao-nubank.pdf'), type=FileType.PDF, year='2023'
    )

    bank_info = BankInfo(name='Nubank', files=[file_info])

    normalize = Normalize(bank_info)
    normalize.normalized()
    # TODO: aqui eu estava colocando a categorização de estabelicimentos, seria bom eu dar um revisada
