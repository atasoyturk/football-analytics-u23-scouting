import pandas as pd
import sqlite3

DB_NAME = "data/data.db"

def main():
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql("SELECT * FROM enhanced_positions", conn)
    conn.close()

    print(f"Satır sayısı: {len(df)}")
    print("İlk 5 satır:")
    print(df.head())

    print("\nKolon isimleri:")
    for c in df.columns:
        print(f"'{c}'")

    defense_keywords = [
        'tackle', 'challenge', 'block', 'interception', 'int', 'clr', 'clearance', 'error', 'err',
        'def', 'defense', 'defensive', 'duel', 'aerial', 'recover', 'possession', 'foul', 'miscontrol'
    ]

    # Anahtar kelimelerden en az biri geçen kolonlar
    defense_metrics = [c for c in df.columns if any(keyword in c.lower() for keyword in defense_keywords)]

    print("\nBulunan tüm defans metrik kolonları:")
    for c in defense_metrics:
        print(c)

    # Sayısala dönüştürme (bazı kolonlar object olabilir)
    for col in defense_metrics:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    # Pozisyon kolonunu bul
    pos_col = [c for c in df.columns if 'pos' in c.lower()][0]
    print(f"\nPozisyon kolonu: '{pos_col}'")

    # Grup ve ortalama
    grouped = df.groupby(pos_col)[defense_metrics].mean().sort_values(by=defense_metrics[0], ascending=False)

    print("\nPozisyona göre tüm defans metriklerinin ortalamaları:\n")
    print(grouped.round(2))


if __name__ == "__main__":
    main()
