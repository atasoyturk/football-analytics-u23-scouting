import sqlite3

def save_to_sql(df, db_name, table_name):
    conn = sqlite3.connect(db_name)

    # Eğer gereksiz bir kolon varsa sil
    if 'Unnamed: 36_level_0_Matches' in df.columns:
        df.drop(columns=['Unnamed: 36_level_0_Matches'], inplace=True)

    df.to_sql(table_name, conn, if_exists='replace', index=False)
    conn.close()
    print(f"🚀 '{table_name}' tablosu '{db_name}' veritabanına kaydedildi.")
