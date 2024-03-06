import json
import os

from fatura import faturas


RESOURCES = os.path.join(os.getcwd(), 'resources') 

def read_json(file_path) -> dict:
    with open(file_path) as file:
        content = json.loads(file.read())
    
    return content

def carrega_categorias():
    return read_json(os.path.join(RESOURCES, 'categorias.json'))

def carrega_estabelecimentos():
    return read_json(os.path.join(RESOURCES, 'estabelecimentos.json'))

def set_estabelecimento():
    pass

categorias=carrega_categorias()
estabelecimentos=carrega_estabelecimentos()
fatura = faturas()
movimentacoes = list(fatura['Movimentacao'].unique().tolist())
movimentacoes.sort()
sem_estabelecimento = []

for movimentacao in movimentacoes:
    is_pagamento_boleto = 'Pagamento Efetuado' in movimentacao or 'Pagto Debito Automatico' in movimentacao or 'Pagamento em' in movimentacao
    has_estabelecimento = False
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
