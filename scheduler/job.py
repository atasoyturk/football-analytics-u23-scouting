# scheduler/job.py
from scraper.setup import setup_browser
from scraper.extract import fetch_html, extract_table
from db.save import save_to_sql
from config import TABLES_INFO, DB_NAME


def job():
    """Bütün tabloları çeker, işler ve SQLite'a kaydeder."""
    try:
        driver = setup_browser()
        for name, (url, table_id) in TABLES_INFO.items():
            print(f"\n📊 {name.upper()} tablosu işleniyor...")
            html_content = fetch_html(driver, url)
            df = extract_table(html_content, table_id)
            save_to_sql(df, db_name=DB_NAME, table_name=f'PL_{name}_data')
        driver.quit()
        print('✅ Tüm tablolar güncellendi!')
    except Exception as e:
        print(f"❌ Job çalışırken bir hata oluştu: {e}")

