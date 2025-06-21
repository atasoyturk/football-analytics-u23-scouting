import sqlite3
import pandas as pd
import os
from db.save import save_to_sql

# PL_data.db yolu
PL_DB_PATH = os.path.join("old_data", "PL_data.db")  # PL_data.db'nin yolu
DATA_DIR = "data"

# PL_data.db'deki tablolarla yeni şema adı eşleşmeleri
TABLE_MAPPING = {
    "PL_standard_data": "stats_standard",
    "PL_shooting_data": "stats_shooting",
    "PL_passing_data": "stats_passing",
    "PL_passing_types_data": "stats_passing_types",
    "PL_goal&shot_creating_actions_data": "stats_gca",
    "PL_defense_data": "stats_defense",
    "PL_possession_data": "stats_possession",
    "PL_playing_time_data": "stats_playing_time",
    "PL_miscellaneous_data": "stats_misc",
    "PL_goalkeeping_data": "stats_keeper_adv"
}

def migrate():
    """PL_data.db'den data/data.db'ye tüm verileri migrate eder."""
    conn = sqlite3.connect(PL_DB_PATH)

    for old_table, new_table in TABLE_MAPPING.items():
        # Veriyi oku
        df = pd.read_sql(f"SELECT * FROM {old_table}", conn)

        # Yeni şema adıyla kaydet
        save_to_sql(df, db_dir=DATA_DIR, table_name=new_table, league_name="Premier League")
    conn.close()

    print("\n✅ PL_data.db'den data/data.db'ye tüm veriler başarıyla migrate edildi!")

