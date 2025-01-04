from re import search, sub

from pandas import DataFrame, read_csv

from finabox.interfaces import Bank, CreditCardBillReader, StatementReader
from finabox.utils import PathConstants, file


class InterCreditCardBillReader(CreditCardBillReader):
    def _extract_text(self) -> list[str]:
        text = self.pdf.pages[1].extract_text()

        file.writer(text, PathConstants.OUTPUT_TXT)
        lines = file.reader(PathConstants.OUTPUT_TXT)

        return lines

    def read_bill(self, **kwargs):
        dict_fatura = []
        text = self._extract_text()

        for line in text:
            cleaned_line = sub(r'\xa0|\x00', ' ', line.strip())
            statemented = search(
                r'^(\d{2}\s\w{3}\s\d{4})(.+)(R\$\s\d.\d{1,},\d{2}|R\$\s\d{1,},\d{2})$',
                cleaned_line,
            )
            if statemented:
                dict_fatura.append({
                    'DATE': statemented.group(1).strip(),
                    'TRANSACTION': statemented.group(2).strip(),
                    'PRICE': statemented.group(3).strip(),
                    'BANK': 'Inter',
                    'PAYMENT_TYPE': 'Credit',
                })

        return DataFrame(dict_fatura)


class InterStatementReader(StatementReader):
    def _read_csv(self, csv_file: str) -> DataFrame:
        lines = file.reader(csv_file, delete_after_read=False)

        for line in lines:
            if self.__is_header(line):
                header_index = lines.index(line)
                break

        statement_lines = lines[header_index:]
        file.writer(statement_lines, csv_file)
        return read_csv(csv_file, sep=';')

    def __is_header(self, line: str):
        return (
            line.strip() == 'Data Lançamento;Histórico;Descrição;Valor;Saldo'
        )

    def read_statement(self) -> DataFrame:
        self._change_columns(['DATE', 'DESCRIPTION', 'NAME', 'PRICE', 'SALDO'])
        self._statement_df.drop(columns=['SALDO'], inplace=True)
        self._statement_df['BANK'] = 'Inter'

        return self._statement_df


class Inter(Bank):
    def __init__(self, pdf_file: str = None, csv_file: str = None) -> None:
        super().__init__(pdf_file, csv_file)
        self._bill_reader = InterCreditCardBillReader()
        self._statement_reader = InterStatementReader()
