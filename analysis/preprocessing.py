import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import os 

db_path = os.path.abspath("data/data.db")

def evaluate_columns():
    
    if not os.path.exists(db_path):
        raise FileNotFoundError(f"Database not found: {db_path}")
    
    try: 
        with sqlite3.connect(db_path) as conn:
            print(f"Connected to database: {db_path}")
            
            df = pd.read_sql("SELECT * FROM master_table", conn)
            
            basis_cols = ['rk', 'nation', 'pos', 'squad', 'age', 'born']
            df_non_basis = df.drop(columns=basis_cols)
            
            prefixes = df_non_basis.columns.str.split('_').str[0].value_counts()
            
    except Exception as e:
        print("", str(e))
        
    plt.figure(figsize=(10, 6))
    prefixes.plot(kind='bar')
    plt.title('Player Metric Prefix Distribution')
    plt.xlabel("Prefixes")
    plt.ylabel("Count")
    plt.grid(axis='y')
    plt.tight_layout()
    plt.show()
    
def select_target_columns():
    if not os.path.exists(db_path):
        raise FileNotFoundError(f"Database not found: {db_path}")
    
    try: 
        with sqlite3.connect(db_path) as conn:
            print(f"Connected to database: {db_path}")
            
            df = pd.read_sql("SELECT * FROM master_table", conn)
            
            metrics_dict = {
                'Category': ['Finishing'] * 16 + ['Ball Carrying'] * 16 + ['Individual Impact'] * 16,
                'Metric': [
                    # Finishing (16)
                    'standard_sh',
                    'standard_sot',
                    'standard_sotpct',
                    'standard_sh_90',
                    'standard_sot_90',
                    'standard_g_sh',
                    'standard_g_sot',
                    'standard_dist',
                    'standard_fk',
                    'expected_xg',
                    'expected_npxg',
                    'expected_npxg_sh',
                    'expected_g-xg',
                    'performance_gls',
                    'performance_g-pk',
                    'per_90_minutes_npxg',
                    
                    # Ball Carrying (16)
                    'carries_carries',
                    'carries_totdist',
                    'carries_prgdist',
                    'carries_1_3',
                    'carries_cpa',
                    'carries_mis',
                    'carries_dis',
                    'progression_prgc',
                    'progression_prgr',
                    'take-ons_att',
                    'take-ons_succ',
                    'take-ons_succpct',
                    'take-ons_tkld',
                    'take-ons_tkldpct',
                    'touches_att_3rd',
                    'touches_att_pen',
                    
                    # Individual Impact (16)
                    'sca_sca',
                    'sca_sca90',
                    'sca_types_passlive',
                    'sca_types_to',
                    'sca_types_sh',
                    'sca_types_fld',
                    'gca_gca',
                    'gca_gca90',
                    'gca_types_passlive',
                    'gca_types_to',
                    'gca_types_sh',
                    'expected_xag',
                    'expected_xa',
                    'expected_npxg+xag',
                    'progression_prgp',
                    'kp'
                ],
                # Turkish explanations
                'Description': [
                    # Finishing (16)
                    'Toplam şut sayısı',
                    'İsabetli şut sayısı',
                    'İsabetli şut yüzdesi',
                    '90 dakika başına şut',
                    '90 dakika başına isabetli şut',
                    'Şut başına gol',
                    'İsabetli şut başına gol',
                    'Ortalama şut mesafesi',
                    'Serbest vuruş şutları',
                    'Beklenen gol (xG)',
                    'Penaltısız beklenen gol',
                    'Şut başına beklenen gol',
                    'Gerçek gol - beklenen gol farkı',
                    'Toplam goller',
                    'Penaltı harici goller',
                    '90 dakika başına penaltısız xG',
                    
                    # Ball Carrying (16)
                    'Toplam top taşıma sayısı',
                    'Top taşıma toplam mesafesi',
                    'İleriye doğru top taşıma mesafesi',
                    'Rakip ceza sahasının 1/3\'üne taşıma',
                    'Ceza sahasına taşıma',
                    'Kaybedilen toplar (taşıma sırasında)',
                    'Hatalı kontroller',
                    'İlerletici taşımalar',
                    'İlerletici top alımları',
                    'Dribling denemeleri',
                    'Başarılı driblingler',
                    'Dribling başarı yüzdesi',
                    'Kaybedilen driblingler',
                    'Dribling kaybetme yüzdesi',
                    'Hücum 3. bölgesinde dokunuşlar',
                    'Ceza sahasında dokunuşlar',
                    
                    # Individual Impact (16)
                    'Şut yaratan aksiyonlar',
                    '90 dakika başına SCA',
                    'Canlı pastan SCA',
                    'Rakip hatasından (take-on) SCA',
                    'Şuttan SCA',
                    'Faul çektirerek SCA',
                    'Gol yaratan aksiyonlar',
                    '90 dakika başına GCA',
                    'Canlı pastan GCA',
                    'Rakip hatasından (take-on) GCA',
                    'Şuttan GCA',
                    'Beklenen asist (xAG)',
                    'Beklenen asist (xa)',
                    'Penaltısız xG + xAG toplamı',
                    'İlerletici paslar',
                    'Anahtar paslar'
                ]
            }
            
        metrics_dict = pd.DataFrame(metrics_dict)
        return metrics_dict
            
    except Exception as e:
        print("An error occurred: ", str(e))
        return None

