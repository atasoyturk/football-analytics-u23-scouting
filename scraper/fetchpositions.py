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

        # Oyuncuları listeleyen tablodaki linkleri bul
        for a in soup.select("a.spielprofil_tooltip"):
            player_name = a.text.strip()
            parent = a.find_parent("tr")  # Satır
            position_td = parent.find_all("td")[4]  # Position genelde 5. kolon
            position = position_td.text.strip() if position_td else None
            data.append({"Player": player_name, "Position": position, "League": league_name})
        time.sleep(2)

    driver.quit()

    df = pd.DataFrame(data).drop_duplicates()
    df.to_csv(output_file, index=False, encoding="utf-8-sig")
    print(f"✅ Positions dosyası üretildi: {output_file}")

if __name__ == "__main__":
    fetch_positions()
