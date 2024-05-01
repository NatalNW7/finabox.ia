import re
import pandas as pd
from utils import PathConstants 
from utils.file import reader  

class Categorize:
    def __init__(self, bill: pd.DataFrame) -> None:
        self.categories = reader(PathConstants.CATEGORIES)
        self.establishments = reader(PathConstants.ESTABLISHMENTS)
        self.__bill = bill

    @property
    def categorized_bill(self):
        self.set_establishments()
        self.set_categories()
        self.clean_bill()

        return self.__bill

    def set_establishments(self, inplace=False):
        dataframes = []
        transactions = self.__bill['TRANSACTION'].apply(self.__clean_transaction)
        transactions = list(transactions.unique().tolist())
        transactions.sort()

        for transaction in transactions:
            transaction = str(transaction).lower().replace('*', r'\*')

            if self.__is_bill_payment(transaction):
                continue

            df = self.__bill[self.__bill['TRANSACTION'].str.contains(transaction, flags=re.IGNORECASE, regex=True)]
            df.insert(0, "ESTABLISHMENT", None)
            has_establishments = False

            for key, values in self.establishments.items():
                if transaction in values:
                    df.loc[:, 'ESTABLISHMENT'] = key
                    dataframes.append(df)
                    has_establishments = True
                    break
                        
            if not has_establishments:
                df.loc[:, 'ESTABLISHMENT'] = 'Sem Estabelecimento'
                dataframes.append(df)


        self.__bill = pd.concat(dataframes, ignore_index=True, sort=True)
        
        return None if inplace else self.__bill

    def set_categories(self, inplace=False) -> pd.DataFrame:
        dataframes = []
        establishments = self.__bill['ESTABLISHMENT']
        establishments = list(establishments.unique().tolist())
        establishments.sort()

        for estabelecimento in establishments:
            for key, values in self.categories.items():
                if estabelecimento in values:
                    df = self.__bill[self.__bill['ESTABLISHMENT'] == estabelecimento]
                    df.insert(0, "CATEGORY", None)
                    df.loc[:, 'CATEGORY'] = key
                    dataframes.append(df)
                    break
        
        self.__bill = pd.concat(dataframes, ignore_index=True, sort=True)

        return None if inplace else self.__bill
    
    def clean_bill(self, inplace=False):
        self.__bill = self.__bill.drop_duplicates(subset=['UUID'])
        self.__bill = self.__bill[~self.__bill['TRANSACTION'].str.contains(r'\+')]
        
        return self.__bill.reset_index(drop=True, inplace=inplace)
    
    def __is_bill_payment(self, transaction):
        payment_checks  = [
            'pagamento efetuado' in transaction,
            'pagto debito automatico' in transaction,
            'pagamento em' in transaction
        ]

        return True in payment_checks

    def __clean_transaction(self, transaction: str):
        regex = r'(parcela\s\d+\sde\s\d+)|(parcela\s\d+\W\d+)|(\-\s\d+\W\d+)'
        transaction = re.sub(regex, '', transaction, flags=re.IGNORECASE).strip()

        return transaction.lower()
