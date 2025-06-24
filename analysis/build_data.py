import pandas as pd
import sqlite3

DB_NAME = "data/data.db"

def load_all_tables(db_name):
    conn = sqlite3.connect(db_name)
    tables = [name for name in pd.read_sql("SELECT name FROM sqlite_master WHERE type='table'", conn)['name']]
    data = {}
    for name in tables:
        df = pd.read_sql(f'SELECT * FROM "{name}"', conn)
        print(f"Tablo: {name} - İlk 5 satır (player, nation, pos, squad):")
        # Eğer bu kolonlar yoksa hata vermesin diye try-except kullanalım
        try:
            print(df[['Player', 'Nation', 'Pos', 'Squad']].head())
        except KeyError:
            print(f"Tablo {name} içinde Player, Nation, Pos veya Squad kolonu yok.")
        data[name] = df
    conn.close()
    return data


def clean_column_names(df):
    # Çok katmanlı kolon isimleri için düzleştirme ve küçük harfe çevirme
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = ['_'.join(map(str, col)).strip() for col in df.columns.values]
    df.columns = df.columns.str.replace(' ', '_').str.replace('%', 'pct').str.lower()
    return df

def convert_columns_to_numeric(df, exclude_cols=None):
    if exclude_cols is None:
        exclude_cols = []
    for col in df.columns:
        if col not in exclude_cols:
            # Zorla numeric yap, olmazsa NaN bırak
            df[col] = pd.to_numeric(df[col], errors='coerce')
    return df

def enhanced_positions(df):
    # Burada ileri seviye filtre, feature engineering veya temizleme yapabilirsin
    df = clean_column_names(df)

    categorical_cols = ['player', 'nation', 'pos', 'squad']
    numeric_cols = df.columns.difference(categorical_cols)

    df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors='coerce')
    
    return df

def build_master(data):
    master_frames = []
    for name, df in data.items():
        df = clean_column_names(df)
        df['source_table'] = name
        master_frames.append(df)

    master = pd.concat(master_frames, ignore_index=True)

    # Defense tablosunu otomatik bul ve işlem yap
    defense_tables = {name: df for name, df in data.items() if name.endswith('_defense')}
    if defense_tables:
        enhanced_frames = []
        for name, defense_df in defense_tables.items():
            enhanced_df = enhanced_positions(defense_df)
            enhanced_df["source_table"] = name
            enhanced_frames.append(enhanced_df)
        enhanced_positions_master = pd.concat(enhanced_frames, ignore_index=True)
        return master, enhanced_positions_master
    else:
        return master, None

if __name__ == "__main__":
    data = load_all_tables(DB_NAME)
    master, enhanced_positions_master = build_master(data)

    conn = sqlite3.connect(DB_NAME)
    master.to_sql('master', conn, if_exists='replace', index=False)
    print(f"✅ master tablosu '{DB_NAME}' içine kaydedildi.")

    if enhanced_positions_master is not None:
        enhanced_positions_master.to_sql('enhanced_positions', conn, if_exists='replace', index=False)
        print(f"✅ enhanced_positions tablosu '{DB_NAME}' içine kaydedildi.")
    else:
        print("⚠️ No defense tables found, enhanced_positions skipped.")

    conn.close()
