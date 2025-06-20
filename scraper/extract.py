# scraper/extract.py
from bs4 import BeautifulSoup
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def fetch_html(driver, url, wait_time=10):
    """URL'yi açıp sayfa kaynağını döndürür."""
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
    """HTML'den belirtilen id'ye sahip tabloyu bulup DataFrame'e çevirir."""
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
