from pandas import DataFrame, read_csv

from finabox.interfaces import Bank, CreditCardBillReader, StatementReader


class NubankCreditCardBillReader(CreditCardBillReader):
    def read_bill(self):
        header = ['date', 'Unnamed', 'description', 'price']
        pages = f'4-{self.pdf.total_pages}'
        bill = self.pdf.to_dataframe(pages, header)
        bill.drop(columns=['Unnamed'], inplace=True)
        bill.dropna(axis=0, inplace=True)
        bill['bank'] = 'Nubank'
        bill['payment_type'] = 'Credit'

        return bill


class NubankStatementReader(StatementReader):
    def _read_csv(self, file_path) -> DataFrame:
        return read_csv(file_path)

    def read_statement(self):
        self._change_columns(['date', 'price', 'uuid', 'description'])
        self.__serialize_dataframe()

        return self._statement_df

    def __read_description(self, description: str) -> dict:
        description = description.strip().split('-')
        return {
            'name': description[1].strip(),
            'description': description[0].strip(),
        }

    def __serialize_dataframe(self):
        statement_lines = []
        statement_json = self._statement_df.to_dict(orient='records')

        for data in statement_json:
            line = {
                'price': 0,
                'date': '',
                'bank': 'Nubank',
            }

            if 'Pagamento de fatura' in data['description']:
                continue

            line['price'] = data['price']
            line['date'] = data['date']

            line.update(self.__read_description(data['description']))

            statement_lines.append(line)

        self._statement_df = DataFrame(statement_lines)


class Nubank(Bank):
    def __init__(self, pdf_file: str = None, csv_file: str = None) -> None:
        super().__init__(pdf_file, csv_file)
        self._bill_reader = NubankCreditCardBillReader()
        self._statement_reader = NubankStatementReader()
