import pandas as pd

def clean_column_names(df):
    # MultiIndex ise kolonları düzleştir
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = ['_'.join([str(i) for i in col]).strip() for col in df.columns.values]

    new_cols = []
    for col in df.columns:
        if col.startswith('Unnamed'):
            new_col = col.split('_')[-1]
            new_cols.append(new_col)
        else:
            new_cols.append(col)
    df.columns = new_cols
    return df
