BRAVE_PATH = r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"
DB_NAME = r"data\data.db" 

# Lig bazlı TABLES_INFO, dictionary olarak tanımlanır.
LEAGUE_URLS = {
    "Premier League": {
        'standard': ('https://fbref.com/en/comps/9/stats/Premier-League-Stats', 'stats_standard'),
        'shooting': ('https://fbref.com/en/comps/9/shooting/Premier-League-Stats', 'stats_shooting'),
        'passing': ('https://fbref.com/en/comps/9/passing/Premier-League-Stats', 'stats_passing'),
        'passing_types': ('https://fbref.com/en/comps/9/passing_types/Premier-League-Stats', 'stats_passing_types'),
        'gca': ('https://fbref.com/en/comps/9/gca/Premier-League-Stats', 'stats_gca'),
        'defense': ('https://fbref.com/en/comps/9/defense/Premier-League-Stats', 'stats_defense'),
        'possession': ('https://fbref.com/en/comps/9/possession/Premier-League-Stats', 'stats_possession'),
        'playing_time': ('https://fbref.com/en/comps/9/playingtime/Premier-League-Stats', 'stats_playing_time'),
        'miscellaneous': ('https://fbref.com/en/comps/9/misc/Premier-League-Stats', 'stats_misc'),
        'goalkeeping': ('https://fbref.com/en/comps/9/keepersadv/Premier-League-Stats', 'stats_keeper_adv'),
        'advanced_gk' : ('https://fbref.com/en/comps/9/keepers/Premier-League-Stats', 'stats_keeper')
    },
    
    "La Liga": {
        'standard': ('https://fbref.com/en/comps/12/stats/La-Liga-Stats', 'stats_standard'),
        'shooting': ('https://fbref.com/en/comps/12/shooting/La-Liga-Stats', 'stats_shooting'),
        'passing': ('https://fbref.com/en/comps/12/passing/La-Liga-Stats', 'stats_passing'),
        'passing_types': ('https://fbref.com/en/comps/12/passing_types/La-Liga-Stats', 'stats_passing_types'),
        'gca': ('https://fbref.com/en/comps/12/gca/La-Liga-Stats', 'stats_gca'),
        'defense': ('https://fbref.com/en/comps/12/defense/La-Liga-Stats', 'stats_defense'),
        'possession': ('https://fbref.com/en/comps/12/possession/La-Liga-Stats', 'stats_possession'),
        'playing_time': ('https://fbref.com/en/comps/12/playingtime/La-Liga-Stats', 'stats_playing_time'),
        'miscellaneous': ('https://fbref.com/en/comps/12/misc/La-Liga-Stats', 'stats_misc'),
        'goalkeeping': ('https://fbref.com/en/comps/12/keepersadv/La-Liga-Stats', 'stats_keeper_adv'),
        'advanced_gk' : ('https://fbref.com/en/comps/12/keepers/Premier-League-Stats', 'stats_keeper')

    },
    
    "Bundesliga": {
        'standard': ('https://fbref.com/en/comps/20/stats/Bundesliga-Stats', 'stats_standard'),
        'shooting': ('https://fbref.com/en/comps/20/shooting/Bundesliga-Stats', 'stats_shooting'),
        'passing': ('https://fbref.com/en/comps/20/passing/Bundesliga-Stats', 'stats_passing'),
        'passing_types': ('https://fbref.com/en/comps/20/passing_types/Bundesliga-Stats', 'stats_passing_types'),
        'gca': ('https://fbref.com/en/comps/20/gca/Bundesliga-Stats', 'stats_gca'),
        'defense': ('https://fbref.com/en/comps/20/defense/Bundesliga-Stats', 'stats_defense'),
        'possession': ('https://fbref.com/en/comps/20/possession/Bundesliga-Stats', 'stats_possession'),
        'playing_time': ('https://fbref.com/en/comps/20/playingtime/Bundesliga-Stats', 'stats_playing_time'),
        'miscellaneous': ('https://fbref.com/en/comps/20/misc/Bundesliga-Stats', 'stats_misc'),
        'goalkeeping': ('https://fbref.com/en/comps/20/keepersadv/Bundesliga-Stats', 'stats_keeper_adv'),
        'advanced_gk' : ('https://fbref.com/en/comps/20/keepers/Premier-League-Stats', 'stats_keeper')

    },
    
    "Serie A": {
        'standard': ('https://fbref.com/en/comps/11/stats/Serie-A-Stats', 'stats_standard'),
        'shooting': ('https://fbref.com/en/comps/11/shooting/Serie-A-Stats', 'stats_shooting'),
        'passing': ('https://fbref.com/en/comps/11/passing/Serie-A-Stats', 'stats_passing'),
        'passing_types': ('https://fbref.com/en/comps/11/passing_types/Serie-A-Stats', 'stats_passing_types'),
        'gca': ('https://fbref.com/en/comps/11/gca/Serie-A-Stats', 'stats_gca'),
        'defense': ('https://fbref.com/en/comps/11/defense/Serie-A-Stats', 'stats_defense'),
        'possession': ('https://fbref.com/en/comps/11/possession/Serie-A-Stats', 'stats_possession'),
        'playing_time': ('https://fbref.com/en/comps/11/playingtime/Serie-A-Stats', 'stats_playing_time'),
        'miscellaneous': ('https://fbref.com/en/comps/11/misc/Serie-A-Stats', 'stats_misc'),
        'goalkeeping': ('https://fbref.com/en/comps/11/keepersadv/Serie-A-Stats', 'stats_keeper_adv'),
        'advanced_gk' : ('https://fbref.com/en/comps/11/keepers/Premier-League-Stats', 'stats_keeper')
        
    },
    
    "Ligue 1": {
        'standard': ('https://fbref.com/en/comps/13/stats/Ligue-1-Stats', 'stats_standard'),
        'shooting': ('https://fbref.com/en/comps/13/shooting/Ligue-1-Stats', 'stats_shooting'),
        'passing': ('https://fbref.com/en/comps/13/passing/Ligue-1-Stats', 'stats_passing'),
        'passing_types': ('https://fbref.com/en/comps/13/passing_types/Ligue-1-Stats', 'stats_passing_types'),
        'gca': ('https://fbref.com/en/comps/13/gca/Ligue-1-Stats', 'stats_gca'),
        'defense': ('https://fbref.com/en/comps/13/defense/Ligue-1-Stats', 'stats_defense'),
        'possession': ('https://fbref.com/en/comps/13/possession/Ligue-1-Stats', 'stats_possession'),
        'playing_time': ('https://fbref.com/en/comps/13/playingtime/Ligue-1-Stats', 'stats_playing_time'),
        'miscellaneous': ('https://fbref.com/en/comps/13/misc/Ligue-1-Stats', 'stats_misc'),
        'goalkeeping': ('https://fbref.com/en/comps/13/keepersadv/Ligue-1-Stats', 'stats_keeper_adv'),
        'advanced_gk' : ('https://fbref.com/en/comps/13/keepers/Premier-League-Stats', 'stats_keeper')
   
    }

}
