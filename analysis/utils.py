import pandas as pd
import sqlite3
import os 


def clean_column_names(df):
    # Çok seviyeli kolon isimlerini tek seviyeye indirgeme
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = [
            '_'.join(str(x).strip() for x in col if str(x).strip() not in ['', 'Unnamed'])
            for col in df.columns.values
        ]

    # unnamed kolonları temizleme ve boşlukları kaldırma
    new_cols = []
    for col in df.columns:
        col_str = str(col)
        if col_str.lower().startswith('unnamed'):
            new_col = col_str.split('_')[-1].strip()
            new_cols.append(new_col)
        else:
            new_cols.append(col_str.strip())
    df.columns = new_cols

    df.columns = [
        col.lower()
         .replace(' ', '_')
         .replace('/', '_')
         .replace('%', 'pct')
         .replace('__', '_')
         for col in df.columns
    ]
    
    # 'player' kolonu içindeki 'player' stringlerini kaldır
    df = df[df['player'] != 'player']

    # verileri sayısal hale getirme
    non_metric_cols = ["player", "nation", "pos", "squad", "age", "born", "matches"]
    metric_columns = [col for col in df.columns if col not in non_metric_cols]

    for col in metric_columns:
        df[col] = df[col].astype(str).str.replace(r'[,%]', '', regex=True)
        df[col] = pd.to_numeric(df[col], errors='coerce')
        
    
    return df


#0.98'den yuksek korelasyonlu sütunlardan birisni kaldır.
#MASTER TABLE'DA ÇALIŞIR, Sadece 1 kez çalıştırılmalı
def remove_highcorr_columns():
    
    db_path = os.path.abspath("data/data.db")

    try:
        with sqlite3.connect(db_path) as conn:
            print(f"[INFO] Connected to database: {db_path}")
            
            # 1️⃣ Veriyi oku
            df = pd.read_sql("SELECT * FROM master_table", conn)
            
            # 2️⃣ Backup al
            backup_table = "master_table" + "_backup"
            df.to_sql(backup_table, conn, if_exists='replace', index=False)
            print(f"[INFO] Backup created: {backup_table}")
            
            # 3️⃣ Sadece sayısal sütunları al
            num_cols = df.select_dtypes(include='number').columns
            corr_matrix = df[num_cols].corr()
            
            # 4️⃣ Yüksek korelasyonlu sütunları bul ve sil
            to_drop = set()
            for i, col1 in enumerate(num_cols):
                for j, col2 in enumerate(num_cols):
                    if i < j and abs(corr_matrix.loc[col1, col2]) >= 0.98:
                        to_drop.add(col2)
                        print(f"[INFO] Dropping {col2} (highly correlated with {col1}, corr={corr_matrix.loc[col1, col2]:.3f})")
            
            if to_drop:
                df = df.drop(columns=list(to_drop))
                # 5️⃣ Veritabanına geri yaz
                df.to_sql("master_table", conn, if_exists='replace', index=False)
                print(f"[INFO] Dropped {len(to_drop)} columns. Database updated successfully.")
            else:
                print("[INFO] No highly correlated columns to drop.")
                
    except Exception as e:
        print("[ERROR] An error occurred: ", str(e))
        
        
def remove_empty_rows():
   db_path = os.path.abspath("data/data.db")
   

   try:
        with sqlite3.connect(db_path) as conn:
            print(f"[INFO] Connected to database: {db_path}")

            # 1️⃣ Veriyi oku
            df = pd.read_sql("SELECT * FROM master_table", conn)

            # 2️⃣ 'player' sütunu değeri 'Player' olan satırları kaldır
            before_count = len(df)
            df = df[df['player'] != 'Player']
            after_count = len(df)
            removed = before_count - after_count

            if removed != 0 :
                df.to_sql("master_table", conn, if_exists='replace', index=False)
            else:
                print("[INFO] No rows to remove where player='Player'.")

            print(f"[INFO] Removed {removed} rows where player='Player'. Database updated successfully.")

   except Exception as e:
        print("[ERROR] An error occurred:", str(e))            


if __name__ == "__main__":
    #remove_highcorr_columns()
    remove_empty_rows()
    


