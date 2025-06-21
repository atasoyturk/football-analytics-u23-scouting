import os
import sqlite3

def save_to_sql(df, db_dir, table_name, league_name):
    """Verilen DataFrame'i belirtilen klasördeki league_name.db dosyasına kaydeder."""
    if not os.path.exists(db_dir):
        os.makedirs(db_dir)

    db_path = os.path.join(db_dir, f"{league_name.replace(' ', '_')}.db")

    conn = sqlite3.connect(db_path)

    # Gereksiz kolon varsa kaldır
    if 'Unnamed: 36_level_0_Matches' in df.columns:
        df.drop(columns=['Unnamed: 36_level_0_Matches'], inplace=True)

    df.to_sql(table_name, conn, if_exists='replace', index=False)
    conn.close()
    print(f"🚀 '{table_name}' tablosu '{db_path}' veritabanına kaydedildi.")
