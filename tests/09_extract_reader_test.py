from src.services import BankExtractReader


def test_read_nubank_extract():
    csvs = {
        'nubank': 'NU_579750386_01JUL2023_31JUL2023.csv',
        # 'inter': 'Extrato-01-07-2023-a-31-07-2023.csv',
    }

    extract_reader = BankExtractReader(csvs)
    print('\n', extract_reader.extract)
    assert not extract_reader.extract.empty
