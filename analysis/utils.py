from narwhals import col
import pandas as pd
from typing import List


def clean_column_names(df):
    # MultiIndex → tek seviye kolon adı yapısına çevir
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = ['_'.join(str(x).strip() for x in col if str(x).strip() not in ['', 'Unnamed']) for col in df.columns.values]

    # Unnamed kolonları sadeleştir
    new_cols = []
    for col in df.columns:
        if str(col).lower().startswith('unnamed'):
            new_col = str(col).split('_')[-1].strip() #strip() methodu ile baştaki ve sondaki boşlukları kaldır
            new_cols.append(new_col)
        else:
            new_cols.append(str(col).strip())

    df.columns = new_cols

    # Tüm kolon isimlerini küçük harfe çevir ve boşlukları düzenle
    df.columns = [col.lower().replace(' ', '_').replace('/', '_') for col in df.columns]

    metric_columns = [col for col in df.columns if col not in ["player", "nation", "pos", "squad", "age", "born", "matches"]]

    for col in metric_columns:
        # Sadece metrik kolonlara uygula
        df[col] = df[col].astype(str).str.replace(r"[,%]", "", regex=True)  # % ve virgülleri kaldır
        df[col] = pd.to_numeric(df[col], errors="coerce")
    
    return df