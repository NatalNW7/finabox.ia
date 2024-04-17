from main import ExtractReader
from utils import PathConstants

def test_read_nubank_extract_():
    extract = ExtractReader('NU_579750386_01JUL2023_31JUL2023.csv')

    extract.parser_dataframe()
    print("\n", extract.extract_df.head())
    extract.extract_df.to_csv(PathConstants.OUTPUT_CSV, index=False)

def test_read_inter_extract_():
    extract = ExtractReader('Extrato-01-07-2023-a-31-07-2023.csv')

    extract.parser_dataframe()
    print("\n", extract.extract_df.head())
    extract.extract_df.to_csv(PathConstants.OUTPUT_CSV, index=False)
