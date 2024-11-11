from json import loads

from pandas import DataFrame, read_csv

from interfaces import Bank, BankExtractReader, CreditCardBillReader


class NubankCreditCardBillReader(CreditCardBillReader):
    def read_bill(self):
        header = ['DATE', 'Unnamed', 'TRANSACTION', 'PRICE']
        pages = f'4-{self.pdf.total_pages}'
        bill = self.pdf.to_dataframe(pages, header)
        bill.drop(columns=['Unnamed'], inplace=True)
        bill.dropna(axis=0, inplace=True)
        bill['BANK'] = 'Nubank'
        bill['PAYMENT_TYPE'] = 'Credit'

        return bill


class NubankExtractReader(BankExtractReader):
    def _read_csv(self, file_path) -> DataFrame:
        return read_csv(file_path)

    def read_extract(self):
        self._change_columns(['DATE', 'PRICE', 'UUID', 'DESCRIPTION'])
        self.__serialize_dataframe()

        return self._extract_df

    def __read_description(self, description: str) -> dict:
        description = description.strip().split('-')
        return {
            'NAME': description[1].strip(),
            'DESCRIPTION': description[0].strip(),
        }

    def __serialize_dataframe(self):
        extract_lines = []
        extract_json = loads(self._extract_df.to_json(orient='records'))

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

            line.update(self.__read_description(data['DESCRIPTION']))

            extract_lines.append(line)

        self._extract_df = DataFrame(extract_lines)


class Nubank(Bank):
    def __init__(self, pdf_file: str = None, csv_file: str = None) -> None:
        super().__init__(pdf_file, csv_file)
        self._bill_reader = NubankCreditCardBillReader()
        self._extract_reader = NubankExtractReader()
