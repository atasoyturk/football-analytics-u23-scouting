import pandas as pd
import numpy as np
import sqlite3

def get_player_data(db_path):
    conn = None
    try: 
        conn = sqlite3.connect(db_path)
        df = pd.read_sql_query("SELECT * FROM def_metrics", conn)
        print(f"Data loaded from {db_path}")
        return df
    except sqlite3.error as e:
        print(f"SQLite error: {e}")
        return pd.DataFrame() #hata olursa bos dataframe dondur
    finally:
        if conn:
            conn.close()
            print("Database connection closed.")
            

def handle_NULL_values(df):
    if df.empty:
        print("DataFrame is empty. No NULL values to handle.")
        return df
    
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    
    league_prefixes = ['bundesliga_', 'premier_league_', 'la_liga_', 'serie_a_', 'ligue_1_']
    for col in numeric_cols:
        if any(col.startswith(prefix) for prefix in league_prefixes):
            if df[col].isnull().any():
                df[col] = df[col].fillna(0)

    print("NULL values that start with league prefixes have been handled.")
    return df
    
    
if __name__ == "__main__":

    DB_PATH = "data/data.db"
    player_df = get_player_data(DB_PATH)
        
    if not player_df.empty:
        
        
        '''print("Column names and types:")
        print(player_df.info())'''
       
        processed_df = handle_NULL_values(player_df.copy())
        print("Processed DataFrame few rows:")
        print(processed_df.head()) 
        
        print("NULL columns:")
        print(processed_df.isnull().sum()[processed_df.isnull().sum() > 0]) # sıfır çıkması lazım 
        
    else:
        print("No data to process.")