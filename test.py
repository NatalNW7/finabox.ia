import pandas as pd

# Criar um DataFrame de exemplo
dados = {'Nomes': ['Alice', 'Bob', 'Charlie', 'David']}
df = pd.DataFrame(dados)

# Função para converter nomes para maiúsculas
def converter_para_maiusculas(nome):
    return nome.upper()

# Aplicar a função à coluna 'Nomes' usando apply
df['Nomes'] = df['Nomes'].apply(converter_para_maiusculas)

# Imprimir o DataFrame resultante
print(df)
