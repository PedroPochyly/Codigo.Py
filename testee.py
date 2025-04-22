from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
import re
from datetime import datetime
import yfinance as yf

def calcular_dividendo_anual(df):
    df['Ano'] = df['Pagamento'].dt.year
    ano_atual = datetime.now().year
    anos_validos = [ano_atual - 3, ano_atual - 2, ano_atual - 1]
    df_filtrado = df[df['Ano'].isin(anos_validos)]
    return df_filtrado.groupby('Ano')['Valor'].sum()

# Configurações
dy_esperado = 0.06
Ticker_empresas = ["AURE3", "BBAS3", "CXSE3", "KLBN3", "SAPR3"]

# Inicia o navegador Selenium uma vez
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
wait = WebDriverWait(driver, 20)

for empresa in Ticker_empresas:
    url = f'https://statusinvest.com.br/acoes/{empresa.lower()}'
    driver.get(url)
    driver.maximize_window()

    print(f"\n🔍 Coletando dados para: {empresa}")

    # Espera a tabela de proventos aparecer
    wait.until(EC.presence_of_element_located((By.XPATH, '//div[@class="responsive-table"]/table')))
    time.sleep(2)

    dados = []
    paginas_visitadas = set()

    while True:
        botoes_pagina = driver.find_elements(By.XPATH, '//div[@class="events"]/ul/li/a')
        botoes_numericos = [b for b in botoes_pagina if b.text.strip().isdigit()]
        paginas_visiveis = [b.text.strip() for b in botoes_numericos]

        encontrou_nova = False

        for numero in paginas_visiveis:
            if numero in paginas_visitadas:
                continue

            paginas_visitadas.add(numero)
            print(f"📄 Página {numero}...")

            botao = wait.until(EC.element_to_be_clickable((By.XPATH, f'//div[@class="events"]/ul/li/a[text()="{numero}"]')))
            driver.execute_script("arguments[0].scrollIntoView(true);", botao)
            driver.execute_script("arguments[0].click();", botao)

            # Espera a nova tabela carregar
            wait.until(EC.presence_of_element_located((By.XPATH, '//div[@class="responsive-table"]/table/tbody/tr')))
            time.sleep(1.5)

            # Coleta os dados da tabela
            linhas = driver.find_elements(By.XPATH, '//div[@class="responsive-table"]/table/tbody/tr')
            for linha in linhas:
                colunas = linha.find_elements(By.TAG_NAME, 'td')
                linha_dados = [c.text.strip() for c in colunas]
                if len(linha_dados) == 4:
                    dados.append(linha_dados)

            encontrou_nova = True

        try:
            seta_proxima = driver.find_element(By.XPATH, '//div[@class="events"]/ul/li/a[@aria-label="Próximo"]')
            pai = seta_proxima.find_element(By.XPATH, './..')
            if 'disabled' in pai.get_attribute('class'):
                break
            driver.execute_script("arguments[0].click();", seta_proxima)
            time.sleep(2)
        except:
            break

        if not encontrou_nova:
            break

    # TRATAMENTO REAL DOS DADOS, sem ignorar nada
    df = pd.DataFrame(dados, columns=['Tipo', 'Data Com', 'Pagamento', 'Valor'])
    df = df[['Pagamento', 'Valor']]

    # Conversão de datas
    df['Pagamento'] = pd.to_datetime(df['Pagamento'], format='%d/%m/%Y', errors='coerce')

    # Limpeza da coluna "Valor"
    df['Valor'] = (
        df['Valor']
        .str.replace(r'[^\d,]', '', regex=True)
        .str.replace(',', '.', regex=False)
        .astype(float)
    )

    # Cálculo dos dividendos
    dividendos_anuais = calcular_dividendo_anual(df)
    media_3anos = dividendos_anuais.mean()
    preco_teto = media_3anos / dy_esperado if media_3anos else 0

    # Cotação via Yahoo Finance
    ticker = yf.Ticker(f"{empresa}.SA")
    cotacao_atual = ticker.fast_info["lastPrice"]
    upside = preco_teto / cotacao_atual if cotacao_atual else 0

    # Saída final
    print(f"📊 Média 3 anos: R$ {media_3anos:.2f}")
    print(f"🎯 Preço teto (DY {dy_esperado*100:.0f}%): R$ {preco_teto:.2f}")
    print(f"💸 Cotação atual: R$ {cotacao_atual:.2f}")
    print(f"📈 Upside estimado: {(upside - 1) * 100:.2f}%")

# Encerra o navegador
driver.quit()
