
BRAVE_PATH = r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"
CHROME_DRIVER_PATH = r"C:\drivers\chromedriver-win64\chromedriver-win64\chromedriver.exe"

DB_NAME = r"data/PL_data.db"

TABLES_INFO = {
    'standard': ('https://fbref.com/en/comps/9/stats/Premier-League-Stats', 'stats_standard'),
    'shooting': ('https://fbref.com/en/comps/9/shooting/Premier-League-Stats', 'stats_shooting'),
    'passing': ('https://fbref.com/en/comps/9/passing/Premier-League-Stats', 'stats_passing'),
    'passing_types': ('https://fbref.com/en/comps/9/passing_types/Premier-League-Stats', 'stats_passing_types'),
    'goal&shot_creating_actions': ('https://fbref.com/en/comps/9/gca/Premier-League-Stats', 'stats_gca'),
    'defense': ('https://fbref.com/en/comps/9/defense/Premier-League-Stats', 'stats_defense'),
    'possession': ('https://fbref.com/en/comps/9/possession/Premier-League-Stats', 'stats_possession'),
    'playing_time': ('https://fbref.com/en/comps/9/playingtime/Premier-League-Stats', 'stats_playing_time'),
    'miscellaneous': ('https://fbref.com/en/comps/9/misc/Premier-League-Stats', 'stats_misc'),
    'goalkeeping': ('https://fbref.com/en/comps/9/keepersadv/Premier-League-Stats', 'stats_keeper_adv')
}
