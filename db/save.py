import sqlite3
import os

def save_to_sql(df, db_dir, table_name, league_name):
    """Verilen DF'i data/data.db içine kaydeder. League adı otomatik eklenir."""
    # Eğer gereksiz bir kolon varsa sil
    if 'Unnamed: 36_level_0_Matches' in df.columns:
        df.drop(columns=['Unnamed: 36_level_0_Matches'], inplace=True)

    # League adı ekle
    df["league"] = league_name

    # Veritabanı yolu
    db_name = os.path.join(db_dir, "data.db")
    conn = sqlite3.connect(db_name)

    # Veriyi tabloya ekle
    df.to_sql(table_name, conn, if_exists='append', index=False)

    conn.close()
    print(f"🚀 '{table_name}' tablosuna '{league_name}' ligi eklendi ({db_name}).")
