import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import json

url = "https://www.fundamentus.com.br/buscaavancada.php"
top100acao = {}

rankings = {
    'P/L': {'field': 'P/L'}, # Quantidade de click => 1x
    'P/VP': {'field': 'P/VP'}, # Quantidade de click => 1x
    'P/EBIT': {'field': 'P/EBIT'}, # Quantidade de click => 1x
    'Div.Yield': {'field': 'Div.Yield'}, # Quantidade de click => 2x
    'Patrim. Liq': {'field': 'Patrim. Líq'}, # Quantidade de click => 2x
    'Mrg Ebit': {'field': 'Mrg Ebit'}, # Quantidade de click => 2x
    'Cresc. Rec.5a': {'field': 'Cresc. Rec.5a'} # Quantidade de click => 2x
}

def filtro():
    driver.find_element(By.TAG_NAME, 'tbody').find_element(By.NAME, 'pl_min').send_keys('1')

    driver.find_element(By.TAG_NAME, 'tbody').find_element(By.NAME, 'pvp_min').send_keys('0')

    driver.find_element(By.TAG_NAME, 'tbody').find_element(By.NAME, 'divy_min').send_keys('0')

    driver.find_element(By.TAG_NAME, 'tbody').find_element(By.NAME, 'pebit_min').send_keys('0')

    driver.find_element(By.TAG_NAME, 'tbody').find_element(By.NAME, 'firma_ebit_min').send_keys('0')

    driver.find_element(By.TAG_NAME, 'tbody').find_element(By.NAME, 'firma_ebitda_min').send_keys('0')

    driver.find_element(By.TAG_NAME, 'tbody').find_element(By.NAME, 'margemliq_min').send_keys('0')

    driver.find_element(By.TAG_NAME, 'tbody').find_element(By.NAME, 'roe_min').send_keys('0')
    
    driver.find_element(By.TAG_NAME, 'tbody').find_element(By.NAME, 'divbruta_min').send_keys('0')
    
    driver.find_element(By.TAG_NAME, 'tbody').find_element(By.NAME, 'tx_cresc_rec_min').send_keys('0')
    
    driver.find_element(By.CLASS_NAME, 'buscar').click()

def rankacao(type):
    field = rankings[type]['field']

    if field == 'Div.Yield' or field == 'Patrim. Líq' or field == 'Mrg Ebit' or field == 'Cresc. Rec.5a':
        driver.find_element(By.ID,"resultado").find_element(By.LINK_TEXT, f'{field}').click()
        driver.find_element(By.ID,"resultado").find_element(By.LINK_TEXT, f'{field}').click()
    else : 
        driver.find_element(By.ID,"resultado").find_element(By.LINK_TEXT, f'{field}').click()
    
    element = driver.find_element(By.ID,"resultado")
    html_content = element.get_attribute('outerHTML')

    soup = BeautifulSoup(html_content, 'html.parser')
    table = soup.find(name='table')

    df_full = pd.read_html(str(table))[0].head(100)
    df = df_full[['Papel', 'Cotação', 'P/L', 'P/VP', 'Div.Yield', 'Patrim. Líq', 'Mrg Ebit', 'P/EBIT', 'Cresc. Rec.5a']]
    df.columns = ['Papel', 'Cotacao', 'P/L', 'P/VP', 'Div.Yield', 'Patrim. Liq', 'Mrg Ebit', 'P/EBIT', 'Cresc. Rec.5a']

    return df.to_dict('records')

option = Options()
option.headless = True
driver = webdriver.Chrome()
# options=option

driver.get(url)
driver.implicitly_wait(10)

filtro()

for k in rankings:
    top100acao[k] = rankacao(k)

driver.quit()

with open('ranking.json', 'w', encoding='utf-8') as jp:
    js = json.dumps(top100acao, indent=4)
    jp.write(js)