from scheduler.job import job
from analysis.master_table import create_master_table
from analysis.player_finding import find_players
from config import LEAGUE_URLS

def main():
    
    try:
        print("STEP 1: Scraping & Saving League Tables ")
        for league_name in LEAGUE_URLS.keys():
            job(league_name)

        print("\n STEP 2: Creating Master Table")
        create_master_table()
        
        print("\nFinding and Profiling Players")
        find_players()

        print("\n-Pipeline completed-")

    except Exception as e:
        print(f"\n Pipeline terminated due to error: {e}")


if __name__ == "__main__":
    main()
