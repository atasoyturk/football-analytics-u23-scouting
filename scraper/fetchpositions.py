from scraper.setup import setup_browser
from bs4 import BeautifulSoup
import pandas as pd
import time

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
        time.sleep(5)  # Sayfa tam yüklensin
        soup = BeautifulSoup(driver.page_source, "html.parser")

        # Yeni class'lardan çekiyoruz
        for player_div in soup.find_all("div", class_="content-row__link-fix--first"):
            name_tag = player_div.find("p", class_="player-name")
            position_tag = player_div.find("span", class_="position")

            if name_tag and position_tag:
                player_name = name_tag.text.strip()
                position = position_tag.text.strip()
                data.append({"Player": player_name, "Position": position, "League": league_name})
                
        time.sleep(2)

    driver.quit()

    df = pd.DataFrame(data).drop_duplicates()
    df.to_csv(output_file, index=False, encoding="utf-8-sig")
    print(f"✅ Positions dosyası üretildi: {output_file}")

if __name__ == "__main__":
    fetch_positions()
