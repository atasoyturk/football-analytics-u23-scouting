# scraper/extract.py
from bs4 import BeautifulSoup
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def fetch_html(driver, url, wait_time=10):
    driver.get(url)
    print(f"🌐 Sayfa açıldı: {url}")

    try:
        WebDriverWait(driver, wait_time).until(
            EC.presence_of_element_located((By.TAG_NAME, "table"))
        )
    except Exception as e:
        print(f"⚠️ Sayfa yüklenirken hata oluştu: {e}")

    return driver.page_source


def extract_table(html, table_id='stats_standard'):
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find('table', {'id': table_id})
    if not table:
        raise ValueError(f"{table_id} ID'li tablo bulunamadı.")

    df = pd.read_html(str(table))[0]

    # MultiIndex temizliği
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = ['_'.join(col).strip() for col in df.columns.values]

    # Tekrarlanan başlık satırlarını sil
    player_col = [col for col in df.columns if 'Player' in col or 'player' in col]
    if player_col:
        df = df[df[player_col[0]] != player_col[0].split('_')[-1]]

    return df

def clean_and_fix_columns(df):
    
    unnamed_cols = [col for col in df.columns if 'Unnamed' in str(col)]
    if unnamed_cols:
        df = df.drop(columns=unnamed_cols)
        print(f"✅ Kaldırılan Unnamed kolonlar: {unnamed_cols}")

    # 2. Eğer kolon MultiIndex ise tek seviyeye indir
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = ['_'.join(filter(None, map(str, col))).strip() for col in df.columns.values]

    # 3. Kolon isimlerinde temizleme
    df.columns = [col.strip().lower().replace(' ', '_') for col in df.columns]

    df = df.fillna(0)

    return df
