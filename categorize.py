import json
import os
import re

from fatura import faturas


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

def set_estabelecimento():
    pass

def sort_dict(obj: dict) -> dict:
    return {key: obj[key] for key in sorted(obj)}

def clean_movimentacao(movimentacao: str):
    regex = r'(parcela\s\d+\sde\s\d+)|(parcela\s\d+\W\d+)|(\-\s\d+\W\d+)'
    movimentacao = re.sub(regex, '', movimentacao, flags=re.IGNORECASE).strip()

    return movimentacao.lower()

categorias=carrega_categorias()
estabelecimentos=carrega_estabelecimentos()
categorias=carrega_categorias()

fatura = faturas()
movimentacoes = fatura['Movimentacao'].apply(clean_movimentacao)
movimentacoes = list(movimentacoes.unique().tolist())
movimentacoes.sort()
sem_estabelecimento = []

for movimentacao in movimentacoes:
    movimentacao = str(movimentacao).lower()
    has_estabelecimento = False
    is_pagamento_boleto = 'pagamento efetuado' in movimentacao or 'pagto debito automatico' in movimentacao or 'pagamento em' in movimentacao

    if is_pagamento_boleto:
        continue

    for key, values in estabelecimentos.items():
        if movimentacao in values:
            print('movimentacao = ', movimentacao, '\n', 'key = ', key)
            has_estabelecimento = True
            break
                
    if not has_estabelecimento:
        sem_estabelecimento.append(movimentacao)

print('\nSEM ESTABELECIMENTO')
for sm in sem_estabelecimento:
    print(sm)        
