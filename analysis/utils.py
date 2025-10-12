import pandas as pd
import sqlite3
import os 


def clean_column_names(df):
    # multiindex columns were in raw table
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = [
            '_'.join(str(x).strip() for x in col if str(x).strip() not in ['', 'Unnamed'])
            for col in df.columns.values
        ]

    # unnamed columns removed
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
    
    #dummy rows removed
    df = df[df['player'] != 'player']


    non_metric_cols = ["player", "nation", "pos", "squad", "age", "born", "matches"]
    metric_columns = [col for col in df.columns if col not in non_metric_cols]

    for col in metric_columns:
        df[col] = df[col].astype(str).str.replace(r'[,%]', '', regex=True)
        df[col] = pd.to_numeric(df[col], errors='coerce')
        
    
    return df


#remove 1 column if pairs have corr >0.98
#run this function 1 time only.
def remove_highcorr_columns():
    
    db_path = os.path.abspath("data/data.db")

    try:
        with sqlite3.connect(db_path) as conn:
            print(f"[INFO] Connected to database: {db_path}")
            
            
            df = pd.read_sql("SELECT * FROM master_table", conn)
            
            # Backup table for any issue 
            backup_table = "master_table" + "_backup"
            df.to_sql(backup_table, conn, if_exists='replace', index=False)
            print(f"[INFO] Backup created: {backup_table}")
            
            # just numeric cols
            num_cols = df.select_dtypes(include='number').columns
            corr_matrix = df[num_cols].corr()
            
            #High corr columns does not explain right thing
            to_drop = set()
            for i, col1 in enumerate(num_cols):
                for j, col2 in enumerate(num_cols):
                    if i < j and abs(corr_matrix.loc[col1, col2]) >= 0.98:
                        to_drop.add(col2)
                        print(f"Dropping {col2} (highly correlated with {col1}, corr={corr_matrix.loc[col1, col2]:.3f})")
            
            #writing again to db
            if to_drop:
                df = df.drop(columns=list(to_drop))
                df.to_sql("master_table", conn, if_exists='replace', index=False)
                print(f"Dropped {len(to_drop)} columns. Database updated")
            else:
                print("No highly correlated columns")
                
    except Exception as e:
        print( str(e))
        
        
def remove_empty_rows():
   db_path = os.path.abspath("data/data.db")
   

   try:
        with sqlite3.connect(db_path) as conn:
            print(f"[INFO] Connected to database: {db_path}")

            df = pd.read_sql("SELECT * FROM master_table", conn)

            before_count = len(df)
            df = df[df['player'] != 'Player']
            after_count = len(df)
            removed = before_count - after_count

            if removed != 0 :
                df.to_sql("master_table", conn, if_exists='replace', index=False)
            else:
                print("No rows to remove.")

            print(f"Removed {removed} rows where player='Player'. Database updated.")

   except Exception as e:
        print( str(e))            


if __name__ == "__main__":
    remove_highcorr_columns()
    remove_empty_rows()
    
    
    


