from scraper.setup import setup_browser
from bs4 import BeautifulSoup
import pandas as pd
import time
import os

LEAGUE_LINKS = {
    "Premier League": "https://www.transfermarkt.com/premier-league/startseite/wettbewerb/GB1",
    "La Liga": "https://www.transfermarkt.com/la-liga/startseite/wettbewerb/ES1",
    "Serie A": "https://www.transfermarkt.com/serie-a/startseite/wettbewerb/IT1",
    "Bundesliga": "https://www.transfermarkt.com/bundesliga/startseite/wettbewerb/L1",
    "Ligue 1": "https://www.transfermarkt.com/ligue-1/startseite/wettbewerb/FR1",
}

def fetch_positions(output_file="data/positions.csv"):
    driver = setup_browser()
    data = []
    for league_name, url in LEAGUE_LINKS.items():
        print(f"⚡️ {league_name} oyuncuları çekiliyor...")
        driver.get(url)
        time.sleep(5)

        soup = BeautifulSoup(driver.page_source, "html.parser")

        for p in soup.select("p.player-name"):
            player_name = p.text.strip()
            parent_div = p.find_parent("div", class_="content-row__player-name")
            position_span = parent_div.find("span", class_="position") if parent_div else None
            position = position_span.text.strip() if position_span else None
            data.append({
                "Player": player_name,
                "Position": position
            })

        time.sleep(2)

    driver.quit()

    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    df = pd.DataFrame(data).drop_duplicates()
    df.to_csv(output_file, index=False, encoding="utf-8-sig")
    print(f"✅ Positions dosyası oluşturuldu: {output_file}")

if __name__ == "__main__":
    fetch_positions()
