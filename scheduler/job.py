# scheduler/job.py
from scraper.setup import setup_browser
from scraper.extract import fetch_html, extract_table, clean_and_fix_columns
from db.save import save_to_sql
from config import LEAGUE_URLS, DB_NAME

def job(league_name):
    """Belirtilen lig için verileri çek ve ortak DB'ye kaydet."""
    try:
        tables = LEAGUE_URLS.get(league_name)
        if not tables:
            raise ValueError(f"❌ {league_name} için config bulunamadı!")

        driver = setup_browser()
        for name, (url, table_id) in tables.items():
            print(f"\n📊 [{league_name}] {name.upper()} tablosu işleniyor...")
            html_content = fetch_html(driver, url)
            df = extract_table(html_content, table_id)
            df = clean_and_fix_columns(df)
            save_to_sql(df, db_name=DB_NAME, table_name=f"{league_name.lower().replace(' ', '_')}_{name}")

        driver.quit()
        print(f"\n✅ {league_name} için tüm tablolar başarıyla güncellendi!")

    except Exception as e:
        print(f"❌ {league_name} job çalışırken hata oluştu: {e}")
