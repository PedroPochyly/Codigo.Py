# %%
from sqlalchemy import create_engine, text
import pandas as pd

# %%
# Instalação de bibliotecas (roda só uma vez no ambiente)
# !pip install mysql-connector-python
# !pip install sqlalchemy
# !pip install pymysql

# %%
# Dados da conexão
user = "root"
senha = "1234"
banco_de_dados = "mercado_br"
host = "localhost"
porta = 3306

# Cria conexão com o banco
conexao = create_engine(url=f"mysql+pymysql://{user}:{senha}@{host}:{porta}/{banco_de_dados}")


import os

# Caminho absoluto baseado no diretório do script
base_dir = os.path.dirname(os.path.abspath(__file__))

dados_fechamento = pd.read_csv(os.path.join(base_dir, 'factStocks.csv'))
cadastro_moedas = pd.read_csv(os.path.join(base_dir, 'dimCoin.csv'))
cadastro_empresas = pd.read_csv(os.path.join(base_dir, 'dimcompany.csv'))
descricao_tempo = pd.read_csv(os.path.join(base_dir, 'dimTime.csv'))
dados_cambio = pd.read_csv(os.path.join(base_dir, 'factCoins.csv'))


# %%
# Ajuste nos dados_cambio
dados_cambio = dados_cambio.drop(13300, axis=0)
dados_cambio = dados_cambio.drop(13301, axis=0)

# %%
# INSERÇÃO INTELIGENTE DE cadastro_moedas (sem duplicar chave primária)

with conexao.connect() as conn:
    result = conn.execute(text("SELECT keyCoin FROM cadastro_moedas"))
    chaves_existentes = {row[0] for row in result}

cadastro_moedas_filtrado = cadastro_moedas[~cadastro_moedas['keyCoin'].isin(chaves_existentes)]

if not cadastro_moedas_filtrado.empty:
    cadastro_moedas_filtrado.to_sql('cadastro_moedas', conexao, index=False, if_exists='append')
    print("✅ Moedas novas inseridas com sucesso!")
else:
    print("ℹ️ Nenhuma moeda nova para inserir.")

# %%
# Inserção dos demais dados (sem filtro de duplicidade)
dados_fechamento.to_sql('dados_fechamento', conexao, index=False, if_exists='append')
cadastro_empresas.to_sql('cadastro_empresas', conexao, index=False, if_exists='append')
descricao_tempo.to_sql('descricao_tempo', conexao, index=False, if_exists='append')
dados_cambio.to_sql('dados_cambio', conexao, index=False, if_exists='append')

print("✅ Todos os dados foram inseridos com sucesso!")



