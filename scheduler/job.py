from scraper.setup import setup_browser
from scraper.extract import fetch_html, extract_table
from db.save_all_tables import save_to_sql
from config import LEAGUE_URLS, DB_NAME

# its for just saving to db all different league tables (merge will be apllied after)
def job(league_name):
    try:
        tables = LEAGUE_URLS.get(league_name)
        if not tables:
            raise ValueError(f"{league_name} no config!")

        driver = setup_browser()
        for name, (url, table_id) in tables.items():
            print(f"\n📊 [{league_name}] {name.upper()} processed")
            html_content = fetch_html(driver, url)
            df = extract_table(html_content, table_id)
            save_to_sql(df, db_name=DB_NAME, table_name=f"{league_name.lower().replace(' ', '_')}_{name}")

        driver.quit()
        print(f"\n✅ for {league_name}, all tables updated.")

    except Exception as e:
        print(f"❌ {league_name} error: {e}")
