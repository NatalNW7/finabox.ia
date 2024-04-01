from interfaces import BillInterface


class MeliuzBill(BillInterface):
    def read_bill(self):
        pages = f'3-{self.pdf.total_pages}'
        df = self.pdf.to_dataframe(pages=pages)
        df = df[['Unnamed: 0','Unnamed: 1','Unnamed: 2']]
        df = df.rename(columns={'Unnamed: 0': 'DATE', 'Unnamed: 1': 'TRANSACTION', 'Unnamed: 2': 'PRICE'})
        df = df.dropna()
        df = df.reset_index(drop=True)
        df['PRICE'] = df['PRICE'].str.replace('R$ ', '')
        df['BANK'] = 'Meliuz'
        df['PAYMENT_TYPE'] = 'Credit'
        
        return df