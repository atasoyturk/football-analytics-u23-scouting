# save.py

import sqlite3


def save_to_sql(df, db_name, table_name):
    """
    Temizlenmiş DataFrame'i SQLite veritabanına yazar.
    
    Args:
        df (pd.DataFrame): Kaydedilecek veri
        db_name (str): Veritabanı dosya adı
        table_name (str): Tablo adı
    """
    try:
        with sqlite3.connect(db_name) as conn:
            # 1. Unnamed kolonları otomatik temizle
            unnamed_cols = [col for col in df.columns if "unnamed" in str(col).lower()]
            if unnamed_cols:
                df.drop(columns=unnamed_cols, inplace=True)
                print(f"🗑️ Kaldırılan Unnamed kolonlar: {unnamed_cols}")

            # 2. DataFrame’i SQLite’a yaz
            df.to_sql(table_name, conn, if_exists='replace', index=False)

        print(f"✅ '{table_name}' tablosu '{db_name}' veritabanına başarıyla kaydedildi.")

    except Exception as e:
        print(f"❌ '{table_name}' tablosu kaydedilirken hata oluştu: {e}")