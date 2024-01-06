import pandas as pd
import json


def read_descricao(descricao: str) -> dict:
    descricao = descricao.strip().split('-')
    return {
        'Nome': descricao[1].strip(),
        'Categoria': descricao[0].strip()
    }
 
def json_dumps(json_dict: dict) -> str:
    return json.dumps(json_dict, indent=4, ensure_ascii=False).encode('utf8').decode()

extrato_csv = 'NU_579750386_01JUL2023_31JUL2023.csv'
df = pd.read_csv(extrato_csv, delimiter=',')
df = df[['Data', 'Valor', 'Descrição']]
json_arr = []

print(df.head())

datas = json.loads(df.to_json(orient='records'))

for data in datas:
    json_obj = {
        'Valor': 0,
        'Data': '',
        'Banco': 'Nubank',
    }

    if 'Pagamento de fatura' in data['Descrição']:
        continue
    json_obj['Valor'] = data['Valor']
    json_obj['Data'] = data['Data']

    read_descricao(data['Descrição'])
    json_obj.update(read_descricao(data['Descrição']))

    print(json_obj)
    json_arr.append(json_obj)


print(json_dumps(json_arr))

# TODO resolver problema  Transfer\u00eancia para Transferência 
# TODO ler extrato dos outros bancos