import pandas as pd
import sqlite3

DB_PATH = r"data\data.db"
LEAGUES = ["premier_league", "la_liga", "serie_a", "bundesliga", "ligue_1"]
STAT_TABLE_SUFFIXES = ["shooting", "passing", "passing_types", "gca", "defense", 
    "possession", "playing_time", "miscellaneous", "goalkeeping", "advanced_gk"]

def create_master_table():
    all_leagues_dfs = []
    conn = sqlite3.connect(DB_PATH)
    
    for league in LEAGUES:
        print(f"{league.replace('_', ' ').title()} datas pulling...")
        base_table_name = f"{league}_standard"
        
        try:
            league_df = pd.read_sql(f'SELECT * FROM {base_table_name}', conn)
            print(f"  Base table: {len(league_df)} satır")
            
            for suffix in STAT_TABLE_SUFFIXES:
                table_to_merge_name = f"{league}_{suffix}"
                
                try:
                    df_to_merge = pd.read_sql(f'SELECT * FROM {table_to_merge_name}', conn)
                    print(f"  Merging {suffix}: {len(df_to_merge)} satır", end="")
                    
                    # ÖZEL DURUM: playing_time için aggregate yap
                    if suffix == "playing_time":
                        merge_keys = ["player", "nation", "pos", "age"]  # squad'ı çıkar
                        
                        # Numeric sütunları topla, non-numeric için ilkini al
                        numeric_cols = df_to_merge.select_dtypes(include=['number']).columns.tolist()
                        
                        # Merge key olmayanları topla
                        agg_dict = {}
                        for col in df_to_merge.columns:
                            if col not in merge_keys and col != 'squad' and col not in ['rk', 'born', 'matches']:
                                if col in numeric_cols:
                                    agg_dict[col] = 'sum'  # Sayısal değerleri topla
                        
                        # Squad için son takımı al (veya en fazla oynadığı takım)
                        agg_dict['squad'] = 'last'
                        
                        df_to_merge = df_to_merge.groupby(merge_keys, as_index=False).agg(agg_dict)
                        print(f" -> {len(df_to_merge)} satıra indirildi")
                    else:
                        merge_keys = ["player", "nation", "pos", "squad", "age"]
                        print()
                    
                    # Duplicate kontrol - aynı anahtarlara sahip birden fazla satır varsa ilkini al
                    before_drop = len(df_to_merge)
                    df_to_merge = df_to_merge.drop_duplicates(subset=merge_keys, keep='first')
                    after_drop = len(df_to_merge)
                    
                    if before_drop != after_drop:
                        print(f"    ⚠️  {before_drop - after_drop} duplicate satır kaldırıldı")
                    
                    # Merge et
                    before_merge = len(league_df)
                    league_df = league_df.merge(
                        df_to_merge,
                        on=merge_keys,
                        how="left",
                        suffixes=("", f"_{suffix}")
                    )
                    after_merge = len(league_df)
                    
                    if after_merge != before_merge:
                        print(f"🔴 UYARI: Satır sayısı değişti! {before_merge} -> {after_merge}")
                
                except pd.io.sql.DatabaseError:
                    print(f"UYARI: '{table_to_merge_name}' tablosu bulunamadı. Atlanıyor.")
                    continue
                except Exception as e:
                    print(f"HATA: {str(e)}")
                    continue
            
            league_df['league'] = league.replace('_', ' ').title()
            all_leagues_dfs.append(league_df)
            print(f"  ✓ {league} tamamlandı: {len(league_df)} satır\n")
            
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
    
    # Matches sütunlarını kaldır
    matches_columns = [col for col in master_df.columns if col.startswith('matches')]
    if matches_columns:
        master_df = master_df.drop(columns=matches_columns)
    
    # Gereksiz sütunları kaldır
    basis_names = ['rk', 'born', '90s']
    basis_columns = [col for col in master_df.columns if any(col.startswith(name) and col != name for name in basis_names)]
    if basis_columns:
        master_df = master_df.drop(columns=basis_columns)
    
    #oyuncu ismi 'player' olan satırları kaldır
    master_df = master_df[master_df['player'] != 'Player']

    print(f"\nFinal master table: {master_df.shape}")
    
    # master tablosunu kaydet    
    try:
        with sqlite3.connect(DB_PATH) as conn:
            master_df.to_sql("master_table", conn, if_exists="replace", index=False)
            print(f"Master table created successfully with {len(master_df)} records.")
    
    except Exception as e:
        print(f"Error saving master table: {e}")
    


    
    

    
        

    
            

