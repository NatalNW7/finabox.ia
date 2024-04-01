import json
import os
import re

from models.bill_reader import bill_reader
import pandas as pd


RESOURCES = os.path.join(os.getcwd(), 'resources') 

def read_json(file_path) -> dict:
    with open(file_path) as file:
        content = json.loads(file.read())
    
    return content

def carrega_categorias():
    categorias = sort_dict(read_json(os.path.join(RESOURCES, 'categorias.json')))
    return categorias

def carrega_estabelecimentos():
    estabelecimentos = sort_dict(read_json(os.path.join(RESOURCES, 'estabelecimentos.json')))
    return estabelecimentos

def set_estabelecimento(fatura: pd.DataFrame) -> pd.DataFrame:
    estabelecimentos=carrega_estabelecimentos()
    dataframes = []
    movimentacoes = fatura['TRANSACTION'].apply(clean_movimentacao)
    movimentacoes = list(movimentacoes.unique().tolist())
    movimentacoes.sort()

    for movimentacao in movimentacoes:
        movimentacao = str(movimentacao).lower()
        has_estabelecimento = False
        is_pagamento_boleto = 'pagamento efetuado' in movimentacao or 'pagto debito automatico' in movimentacao or 'pagamento em' in movimentacao

        if is_pagamento_boleto:
            continue

        for key, values in estabelecimentos.items():
            if movimentacao in values:
                df = fatura[fatura['TRANSACTION'].str.contains(movimentacao.replace('*', '\*'), flags=re.IGNORECASE, regex=True)]
                df['ESTABLISHMENT'] = key
                dataframes.append(df)
                has_estabelecimento = True
                break
                    
        if not has_estabelecimento:
            df = fatura[fatura['TRANSACTION'].str.contains(movimentacao.replace('*', '\*'), flags=re.IGNORECASE, regex=True)]
            df['ESTABLISHMENT'] = 'Sem Estabelecimento'
            dataframes.append(df)
    
    return pd.concat(dataframes, ignore_index=True, sort=True)

def set_categoria(fatura: pd.DataFrame) -> pd.DataFrame:
    categorias=carrega_categorias()
    dataframes = []
    estabelecimentos = fatura['ESTABLISHMENT']
    estabelecimentos = list(estabelecimentos.unique().tolist())
    estabelecimentos.sort()

    for estabelecimento in estabelecimentos:
        for key, values in categorias.items():
            if estabelecimento in values:
                df = fatura[fatura['ESTABLISHMENT'] == estabelecimento]
                df['CATEGORY'] = key
                dataframes.append(df)
                break
    
    return pd.concat(dataframes, ignore_index=True, sort=True)

def sort_dict(obj: dict) -> dict:
    return {key: obj[key] for key in sorted(obj)}

def clean_movimentacao(movimentacao: str):
    regex = r'(parcela\s\d+\sde\s\d+)|(parcela\s\d+\W\d+)|(\-\s\d+\W\d+)'
    movimentacao = re.sub(regex, '', movimentacao, flags=re.IGNORECASE).strip()

    return movimentacao.lower()

def clean_fatura(fatura: pd.DataFrame) -> pd.DataFrame:
    fatura = fatura.drop_duplicates(subset=['UUID'])
    fatura = fatura[~fatura['TRANSACTION'].str.contains('\+')]

    return fatura.reset_index(drop=True, inplace=False)

def categorize_fatura() -> pd.DataFrame:
    files = {
        'nubank': 'Nubank_2023-07-23.pdf',
        'inter': 'inter_2023-07.pdf',
        'meliuz': 'meliuz-2023-07.pdf',
        'pan': 'pan_2023-07.pdf'
    }

    fatura = bill_reader(files)
    fatura_com_estabelecimento = set_estabelecimento(fatura)
    fatura_categorizada = set_categoria(fatura_com_estabelecimento)
    cleaned_fatura = clean_fatura(fatura_categorizada)

    return cleaned_fatura

if '__main__' == __name__:
    fatura = categorize_fatura()
    print(fatura)
    print(fatura['PRICE'].sum())

    # fatura.to_csv('controle-fianceiro-teste.csv', index=False)
