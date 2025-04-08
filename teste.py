import pandas as pd
import numpy as np


dados_dy = pd.read_excel('Mundo20-dy_yield_empresas_26set.xlsx').dropna()


dados_dy = dados_dy[['TICKER', 'DY_12M']].sort_values(by='DY_12M', ascending=False)


quartis = [0, 5, 10, 25, 50, 75, 100, 150, 200]
dados_dy['quartis'] = pd.cut(dados_dy['DY_12M'], quartis)

print(dados_dy)

empresa_escolhida = input('Digite o nome da empresa: ')


if empresa_escolhida in dados_dy['TICKER'].values:
    quartil_empresa = dados_dy.loc[dados_dy['TICKER'] == empresa_escolhida, 'quartis'].values[0]
    print(f'Empresa encontrada! Ela está no seguinte quartil: {quartil_empresa}')
else:
    print('Empresa não encontrada.')
