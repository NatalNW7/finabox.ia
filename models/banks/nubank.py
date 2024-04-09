from interfaces import BillInterface


class NubankBill(BillInterface):
    def read_bill(self):
        header=['DATE', 'Unnamed', 'TRANSACTION', 'PRICE']
        pages = f'4-{self.pdf.total_pages}'
        bill = self.pdf.to_dataframe(pages, header)
        bill.drop(columns=['Unnamed'], inplace=True)
        bill.dropna(axis=0, inplace=True)
        bill['BANK'] = 'Nubank'
        bill['PAYMENT_TYPE'] = 'Credit'

        return bill