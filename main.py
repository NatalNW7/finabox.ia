import pandas as pd
import json
from utils import PathConstants, file
import os


# 'NU_579750386_01JUL2023_31JUL2023.csv'
class ExtractReader:
    def __init__(self, csv_file: str) -> None:
        self.__extract_csv = os.path.join(PathConstants.TEMP, csv_file)
        self.extract_df = self.__read_csv(self.__extract_csv)
    
    def __read_csv(self, extract_csv) -> pd.DataFrame:
        lines = file.reader(extract_csv)
        
        for line in lines:
            if self.__is_header(line):
                break
            lines.remove(line)

        return pd.DataFrame(lines)

    def __is_header(self, text: str):
        headers = [
            'Data,Valor,Identificador,Descrição',
            'Data Lançamento;Histórico;Descrição;Valor;Saldo'
        ]

        return text.strip() in headers

    def __change_columns(self):
        self.extract_df.columns = ['DATE', 'PRICE', 'UUID', 'DESCRIPTION']

    def read_description(self, description) -> dict:
        description = description.strip().split('-')
        return {
            'NAME': description[1].strip(),
            'DESCRIPTION': description[0].strip()
        }

    def parser_dataframe(self):
        extract_lines = []
        extract_json = json.loads(self.extract_df.to_json(orient='records'))

        for data in extract_json:
            line = {
                'PRICE': 0,
                'DATE': '',
                'BANK': 'Nubank',
            }

            if 'Pagamento de fatura' in data['DESCRIPTION']:
                continue

            line['PRICE'] = data['PRICE']
            line['DATE'] = data['DATE']

            line.update(self.read_description(data['DESCRIPTION']))

            extract_lines.append(line)
        
        self.extract_df = pd.DataFrame(extract_lines)

# TODO ler extrato dos outros bancos
