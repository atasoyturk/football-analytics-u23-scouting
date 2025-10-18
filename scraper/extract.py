from bs4 import BeautifulSoup 

import pandas as pd
from analysis.utils import clean_column_names

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def fetch_html(driver, url, wait_time=10):
    driver.get(url)
    print(f"Website opened: {url}")

    try:
        WebDriverWait(driver, wait_time).until(
            EC.presence_of_element_located((By.TAG_NAME, "table"))
        )
    except Exception as e:
        print(f"Scraping error: {e}")

    return driver.page_source


def extract_table(html, table_id='stats_standard'):
    
    soup = BeautifulSoup(html, 'html.parser') 
    
    table = soup.find('table', {'id': table_id})
    if not table:
        raise ValueError(f"{table_id} could not be found.")

    df = pd.read_html(str(table))[0] 
    df = clean_column_names(df)

    player_col = [col for col in df.columns if 'player' in str(col).lower()]     
    if player_col:
        df = df[df[player_col[0]] != player_col[0].split('_')[-1]]
            
    return df