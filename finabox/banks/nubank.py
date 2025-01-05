from json import loads

from pandas import DataFrame, read_csv

from finabox.interfaces import Bank, CreditCardBillReader, StatementReader


class NubankCreditCardBillReader(CreditCardBillReader):
    def read_bill(self):
        header = ['DATE', 'Unnamed', 'DESCRIPTION', 'PRICE']
        pages = f'4-{self.pdf.total_pages}'
        bill = self.pdf.to_dataframe(pages, header)
        bill.drop(columns=['Unnamed'], inplace=True)
        bill.dropna(axis=0, inplace=True)
        bill['BANK'] = 'Nubank'
        bill['PAYMENT_TYPE'] = 'Credit'

        return bill


class NubankStatementReader(StatementReader):
    def _read_csv(self, file_path) -> DataFrame:
        return read_csv(file_path)

    def read_statement(self):
        self._change_columns(['DATE', 'PRICE', 'UUID', 'DESCRIPTION'])
        self.__serialize_dataframe()

        return self._statement_df

    def __read_description(self, description: str) -> dict:
        description = description.strip().split('-')
        return {
            'NAME': description[1].strip(),
            'DESCRIPTION': description[0].strip(),
        }

    def __serialize_dataframe(self):
        statement_lines = []
        statement_json = loads(self._statement_df.to_json(orient='records'))

        for data in statement_json:
            line = {
                'PRICE': 0,
                'DATE': '',
                'BANK': 'Nubank',
            }

            if 'Pagamento de fatura' in data['DESCRIPTION']:
                continue

            line['PRICE'] = data['PRICE']
            line['DATE'] = data['DATE']

            line.update(self.__read_description(data['DESCRIPTION']))

            statement_lines.append(line)

        self._statement_df = DataFrame(statement_lines)


class Nubank(Bank):
    def __init__(self, pdf_file: str = None, csv_file: str = None) -> None:
        super().__init__(pdf_file, csv_file)
        self._bill_reader = NubankCreditCardBillReader()
        self._statement_reader = NubankStatementReader()
