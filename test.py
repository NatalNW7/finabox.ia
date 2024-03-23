import pandas as pd

# Criar um DataFrame de exemplo
data1 = pd.read_csv('Controle Financeiro - Cartao.csv')
dados2 = pd.read_csv('controle-financeiro-teste.csv')

# print(data1)
# print(dados2)

deferenca = pd.concat([data1,dados2])

print(deferenca.sort_values(by=['Valor']).drop_duplicates())