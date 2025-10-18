from scheduler.job import job
from analysis.master_table import create_master_table
from analysis.player_finding import find_players
from scraper.setup import setup_browser
from config import LEAGUE_URLS

def main():
    driver = None
    try:
        print("Scraping & Saving League Tables ")
        driver = setup_browser()  
        
        for league_name in LEAGUE_URLS.keys():
            job(league_name, driver)  

        print("\nCreating Master Table")
        create_master_table()
        
        print("\nFinding and Profiling Players")
        find_players()

        print("\n-Pipeline completed-")

    except Exception as e:
        print(f"\n Pipeline error: {e}")
    
    finally:
        if driver:
            driver.quit()  


if __name__ == "__main__":
    main()
