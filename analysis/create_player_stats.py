import pandas as pd
import sqlite3

DB_PATH = r"data\data.db"
LEAGUES = ["premier_league", "la_liga", "serie_a", "bundesliga", "ligue_1"]
STAT_TABLE_SUFFIXES = ["shooting", "passing", "passing_types", "gca", "defense", 
    "possession", "playing_time", "miscellaneous"]

def create_master_table():
    all_leagues_dfs = []
    conn = sqlite3.connect(DB_PATH)
    
    for league in LEAGUES:
        # replace('_', ' ') ile alt tireleri boşlukla değiştirir. title() ile baş harfleri büyük yapar.
        print(f"{league.replace('_', ' ').title()} datas pulling...")  # premier_league -> Premier League
        base_table_name = f"{league}_standard" # her ligin standard tablolarının isimleri 
        
        try:
            league_df = pd.read_sql(f'SELECT * FROM {base_table_name}', conn)
            
            for suffix in STAT_TABLE_SUFFIXES:
                table_to_merge_name = f"{league}_{suffix}"
                
                try:
                    df_to_merge = pd.read_sql(f'SELECT * FROM {table_to_merge_name}', conn)
                
                    league_df = league_df.merge(
                        df_to_merge,
                        on=["Player", "Nation", "Pos", "Squad", "Age"],  
                        how="left",
                        suffixes=("", f"_{suffix}")
                    )
                
                except pd.io.sql.DatabaseError:
                    print(f"    UYARI: '{table_to_merge_name}' tablosu bulunamadı. Atlanıyor.")
                    continue
            
            league_df['league'] = league.replace('_', ' ').title()
            all_leagues_dfs.append(league_df)
            
        except pd.io.sql.DatabaseError:
            print(f"Table {base_table_name} not found for {league}. Skipping...")
            continue
        
    conn.close()
    
    if not all_leagues_dfs:
        print("No data found for any league.")
        return
    
    print("All leagues are being merged...")
    master_df = pd.concat(all_leagues_dfs, ignore_index=True)
    
    master_df = master_df.fillna(0)
    
    matches_columns = [col for col in master_df.columns if col.startswith('Matches')]
    if matches_columns:
        master_df = master_df.drop(columns=matches_columns)
    else:
        print("No 'Matches' columns found to remove.")
        
    basis_names = ['Rk', 'Born', '90s']
    basis_columns = [col for col in master_df.columns if any(col.startswith(name) and col!=name for name in basis_names)]

    if basis_columns:
        master_df = master_df.drop(columns=basis_columns)

    print("Master table is being created...")
    conn = sqlite3.connect(DB_PATH)
    master_df.to_sql("player_stats", conn, if_exists="replace", index=False)
    conn.close()
    
    print(f"Master table created successfully with {len(master_df)} records.")
    
if __name__ == "__main__":
    create_master_table()
    
        

    
            

