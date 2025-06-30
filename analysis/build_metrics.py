import pandas as pd
from typing import List, Dict, Optional
from analysis.utils import clean_column_names
import sqlite3


def load_tables(db_name: str, lig_prefixes: List[str], metric_suffixes: List[str]) -> Dict[str, pd.DataFrame]:
    """
    Loads tables from an SQLite database based on lig prefixes and metric suffixes.
    Returns a dictionary where keys are 'lig_metric_type' (e.g., 'bundesliga_standard')
    and values are DataFrames.
    """
    conn = sqlite3.connect(db_name)
    query = "SELECT name FROM sqlite_master WHERE type='table'"
    tables = pd.read_sql(query, conn)['name'].tolist()
    conn.close()

    raw_data = {}
    for lig_prefix in lig_prefixes:
        for met_suffix in metric_suffixes:
            # Tablo adı beklenen formatta: lig_prefix + met_suffix (örn. bundesliga_standard)
            expected_table_name = f"{lig_prefix}{met_suffix}"
            
            if expected_table_name in tables:
                conn = sqlite3.connect(db_name)
                df = pd.read_sql(f'SELECT * FROM "{expected_table_name}"', conn)
                conn.close()
                raw_data[expected_table_name] = df
            # else:
            #     print(f"Uyarı: '{expected_table_name}' tablosu veritabanında bulunamadı.")

    return raw_data


def join_tables(frames: List[pd.DataFrame], on: List[str]) -> pd.DataFrame:
    """Performs an OUTER JOIN on the specified common columns."""
    if not frames:
        return pd.DataFrame()

    combined = frames[0]
    for df in frames[1:]:
        combined = pd.merge(combined, df, on=on, how="outer")
    return combined


def create_position_metric(
    db_name: str,
    output_table: str,
    lig_prefixes: List[str], # Yeni: Lig önekleri
    metric_suffixes: List[str], # Metrik türlerinin son ekleri (örn. _standard)
    metric_suffix_abbreviations: List[str], # Metrik türlerinin kısaltmaları (örn. std)
    id_columns: List[str],
    non_metric_columns: Optional[List[str]] = None
) -> None:
    """
    Creates a position-specific metric table by joining data from different leagues and metric types.
    """

    non_metric_columns = non_metric_columns or []
    
    # METRIC_SUFFIXES ve METRIC_SUFFIX_ABBREVIATIONS uzunlukları aynı olmalı
    if len(metric_suffixes) != len(metric_suffix_abbreviations):
        raise ValueError("metric_suffixes ve metric_suffix_abbreviations listelerinin uzunlukları aynı olmalıdır.")
    
    # Suffix ve kısaltma eşleşmesini bir sözlükte tutalım
    suffix_to_abbr = dict(zip(metric_suffixes, metric_suffix_abbreviations))


    print(f"🔄 '{output_table}' oluşturuluyor...")

    # load_tables fonksiyonunu yeni parametrelerle çağırın
    raw_data = load_tables(db_name, lig_prefixes, metric_suffixes)
    if not raw_data:
        print(f"⚠️ '{output_table}' oluşturulamadı. Uygun tablo bulunamadı.")
        return

    print("🔍 Yüklenecek tablolar:", list(raw_data.keys()))

    processed_frames = []

    # raw_data'nın anahtarları artık 'lig_metric_type' formatında olacak (örn. 'bundesliga_standard')
    for table_name, df in raw_data.items():
        print(f"\n--- Tablo İşleniyor: {table_name} ---")
        
        # Lig önekini ve metrik son ekini table_name'den ayıklayın
        # Örn: 'bundesliga_standard' -> lig_prefix='bundesliga', met_suffix='_standard'
        found_lig_prefix = None
        found_metric_suffix = None
        
        for lp in lig_prefixes:
            if table_name.startswith(lp):
                found_lig_prefix = lp
                break
        
        for ms in metric_suffixes:
            if table_name.endswith(ms):
                found_metric_suffix = ms
                break

        if not found_lig_prefix or not found_metric_suffix:
            print(f"Hata: '{table_name}' için lig öneki veya metrik son eki bulunamadı. Atlanıyor.")
            continue
        
        # Kısaltmayı alın
        metric_abbr = suffix_to_abbr.get(found_metric_suffix, f"unknown_{found_metric_suffix.replace('_', '')}")
        
        # Kolon öneki artık hem ligi hem de metrik türünü içerecek
        column_prefix = f"{found_lig_prefix}_{metric_abbr}"


        df = clean_column_names(df)

        if "player" in df.columns:
            df["player"] = df["player"].str.strip().str.lower()
        else:
            print(f"⚠️ Tablo '{table_name}' 'player' kolonu içermiyor. Atlanıyor.")
            continue

        if "90s" in df.columns and "minutes" not in df.columns:
            df["minutes"] = pd.to_numeric(df["90s"], errors='coerce')
        
        for col in id_columns:
            if col not in df.columns:
                df[col] = pd.NA

        current_id_columns_for_this_df = ["player"] + [col for col in id_columns if col != "player" and col in df.columns]
        current_metric_columns = [col for col in df.columns if col not in current_id_columns_for_this_df]

        for col in current_metric_columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

        # _rk ve _born kolonlarını burada, yani her tabloyu tek tek işlerken düşürüyoruz.
        cols_to_drop_pre_agg = [
            col for col in df.columns
            if "matches" in col.lower() or col.endswith("_rk") or col.endswith("_born")
        ]
        df.drop(columns=cols_to_drop_pre_agg, inplace=True, errors='ignore')
        print(f"Düşürülen Kolonlar ({table_name}): {cols_to_drop_pre_agg}")
        
        agg_dict = {col: 'mean' for col in current_metric_columns if col in df.columns}
        
        for id_col in current_id_columns_for_this_df:
            if id_col != "player":
                # 'age' ve '90s' gibi sayısal ID'ler için 'first' veya 'mean' kullanabilirsiniz.
                # Burada 'first' daha mantıklı çünkü oyuncunun tek bir yaş ve 90s değeri olmalı.
                if df[id_col].dtype == 'object' or id_col in ['age', '90s', 'minutes']:
                    agg_dict[id_col] = 'first'
                else: # Diğer sayısal ID'ler için (eğer varsa)
                    agg_dict[id_col] = 'first' # Genellikle ID'ler mean alınmaz

        if not agg_dict:
            aggregated_df = df[["player"]].drop_duplicates()
        else:
            cols_to_groupby_agg = [c for c in df.columns if c in agg_dict] + ["player"]
            cols_to_groupby_agg = list(set(cols_to_groupby_agg) & set(df.columns))
            
            df_for_agg = df[cols_to_groupby_agg]
            valid_agg_dict = {k: v for k, v in agg_dict.items() if k in df_for_agg.columns}

            aggregated_df = df_for_agg.groupby("player", as_index=False).agg(valid_agg_dict)
        
        rename_dict = {}
        for col in aggregated_df.columns:
            if col == "player":
                continue
            # Kolonları hem lig hem de metrik kısaltması ile önekle
            rename_dict[col] = f"{column_prefix}_{col}"
        
        aggregated_df.rename(columns=rename_dict, inplace=True)
        processed_frames.append(aggregated_df)

    print("\n--- Birleştirme Aşaması ---")
    merged_df = join_tables(processed_frames, on=["player"])
    print(f"Birleştirilmiş DataFrame Bilgisi (merged_df):")
    merged_df.info(verbose=True, show_counts=True)
    print(f"Birleştirilmiş DataFrame NaN Sayıları (merged_df):\n{merged_df.isnull().sum()[merged_df.isnull().sum() > 0]}")
    
    print("\n--- ID Kolonlarını Konsolide Etme Aşaması ---")
    final_id_columns_base = ["player"] + [col for col in id_columns if col != "player"]

    for base_col in [col for col in id_columns if col != "player"]:
        # Lig önekli ID kolonlarını bulmak için dinamik regex kullanın
        # Örn: 'bundesliga_std_nation', 'la_liga_std_nation'
        potential_id_cols = sorted([col for col in merged_df.columns if col.endswith(f"_{base_col}")])
        
        if potential_id_cols:
            temp_series = pd.Series(pd.NA, index=merged_df.index, dtype='object')

            for p_col in potential_id_cols:
                if p_col in merged_df.columns:
                    temp_series = temp_series.fillna(merged_df[p_col])
            
            merged_df[base_col] = temp_series
            merged_df.drop(columns=potential_id_cols, inplace=True, errors='ignore')
            
            print(f"ID Kolonu '{base_col}' Konsolidasyon Sonrası NaN Sayısı: {merged_df[base_col].isnull().sum()}")


    for base_col in [col for col in id_columns if col != "player"]:
        if base_col in merged_df.columns and merged_df[base_col].isnull().all():
            merged_df.drop(columns=[base_col], inplace=True)
            print(f"🗑️ Tamamen boş olan '{base_col}' ID kolonu silindi.")
        
    print("🗑️ Gereksiz ID kolonları silindi ve ana ID kolonları konsolide edildi.")
    print(f"ID Konsolidasyonu Sonrası Merged DataFrame NaN Sayıları:\n{merged_df.isnull().sum()[merged_df.isnull().sum() > 0]}")


    print("\n--- Metrik Kolonları Filtreleme Aşaması ---")
    final_metric_cols = []
    # Yeni bir yaklaşım: ID kolonları ve "player" dışındaki her şey metrik olmalı.
    # Ancak _rk ve _born gibi istenmeyenleri hala hariç tutmalıyız.
    
    # Temizlenmiş ID kolonları dışındaki tüm kolonları metrik olarak kabul et
    current_final_id_columns = [col for col in id_columns if col in merged_df.columns]
    
    for col in merged_df.columns:
        if col not in current_final_id_columns and col != "player":
            # Yine de _rk ve _born ile bitenleri metrik olarak almayalım
            is_rk_or_born_suffix = col.endswith("_rk") or col.endswith("_born")
            if not is_rk_or_born_suffix:
                final_metric_cols.append(col)
    
    print(f"Final Metrik Kolonları Sayısı: {len(final_metric_cols)}")
    print(f"Final Metrik Kolonları Örnekleri: {final_metric_cols[:5]}...")


    final_id_columns_present = [col for col in id_columns if col in merged_df.columns]

    print(f"\n--- Son NaN Satırları Silme Aşaması (Metrikler Bazında) ---")
    if final_metric_cols:
        initial_rows = len(merged_df)
        merged_df = merged_df.dropna(subset=final_metric_cols, how="all")
        print(f"Başlangıç satır sayısı: {initial_rows}, Silinen satır sayısı: {initial_rows - len(merged_df)}")
    else:
        print("Final metrik kolonu bulunamadı, bu yüzden NaN satırları silinmedi.")

    print("🗑️ Tüm metriği eksik olan satırlar silindi.")
    print(f"Final DataFrame Oluşmadan Önce NaN Sayıları:\n{merged_df.isnull().sum()[merged_df.isnull().sum() > 0]}")


    final_columns = [col for col in final_id_columns_present + final_metric_cols if col in merged_df.columns]
    final_df = merged_df[final_columns].copy()

    if "player" in final_df.columns:
        final_df["player"] = final_df["player"].str.title()

    conn = sqlite3.connect(db_name)
    final_df.to_sql(output_table, conn, if_exists="replace", index=False)
    conn.close()

    print(f"\n✅ '{output_table}' başarıyla oluşturuldu ve '{db_name}' içine kaydedildi.")
    print("📊 Oluşturulan tablo ilk 5 satır:")
    print(final_df.head(5).to_string(index=False))