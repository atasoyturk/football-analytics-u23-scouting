import pandas as pd
import sqlite3
from preprocessing import select_target_columns
import os
import numpy as np

db_path = os.path.abspath("data/data.db")

def reduce_columns():
    if not os.path.exists(db_path):
        raise FileNotFoundError(f"Database not found: {db_path}")
    
    try:
        with sqlite3.connect(db_path) as conn:
            df = pd.read_sql("SELECT * FROM master_table", conn)
            metrics_df = select_target_columns()
            
            selected_metrics = []
            
            for category in metrics_df['Category'].unique():
                metric_names = metrics_df[metrics_df['Category'] == category]['Metric'].tolist()
                availables = [m for m in metric_names if m in df.columns]
                
                if not availables:
                    print(f" No metrics found for category '{category}'")
                    continue
                
                numeric_cols = df[availables].select_dtypes(include=np.number).columns.tolist()
                if not numeric_cols:
                    print(f"No numeric metrics in category '{category}'")
                    continue
                
                data = df[numeric_cols].fillna(0)
                means = data.mean()
                stds = data.std()
                cv = pd.Series(np.where(np.abs(means) > 1e-8, stds / np.abs(means), 0), index=numeric_cols)
                
                if len(numeric_cols) == 1:
                    redundancy = pd.Series([0.0], index=numeric_cols)
                else:
                    corr = data.corr().abs()
                    redundancy = corr.mean(axis=1)
                
                score = cv / (1 + redundancy)
                score = score.sort_values(ascending=False)
                top5 = score.head(5).index.tolist()
                selected_metrics.extend(top5)
            
            selected_metrics = list(dict.fromkeys(selected_metrics))
            
            print(f"\nSelected {len(selected_metrics)} metrics using CV + Redundancy:")
            for metric in selected_metrics:
                row = metrics_df[metrics_df['Metric'] == metric].iloc[0]
                print(f"- [{row['Category']}] {metric}: {row['Description']}")
            
            return selected_metrics

    except Exception as e:
        print("❌ Error:", str(e))
        raise
    
# just one check 
#def outlier_test():
    
    try: 
        with sqlite3.connect(db_path) as conn:
            df = pd.read_sql("SELECT * FROM master_table", conn)
            
            selected_metrics = reduce_columns()
            
            desc = df[selected_metrics].describe(percentiles=[0.01, 0.05, 0.25, 0.5, 0.75, 0.95, 0.99]).T
            desc['iqr'] = desc['75%'] - desc['25%']
            desc['outlier_upper'] = desc['99%'] > (desc['75%'] + 1.5 * desc['iqr'])
            desc['outlier_lower'] = desc['1%'] < (desc['25%'] - 1.5 * desc['iqr'])
            
            result = desc[['count', 'mean', 'std', 'min', '1%', '25%', '50%', '75%', '99%', 'max', 'outlier_upper', 'outlier_lower']]
            
            print("\n Outliers:")
            print(result.head(15).to_string())
            
    except Exception as e:
        print("Error :", str(e))

def assign_profiles(df, selected_metrics):
    from sklearn.preprocessing import StandardScaler, RobustScaler
    import numpy as np
    import pandas as pd

    df = df.copy()
    
    # take-ons_tkld reverse for correct metric
    if 'take-ons_tkld' in selected_metrics:
        df['take-ons_tkld_inv'] = 1 / (1 + df['take-ons_tkld'])
        tkld_col = 'take-ons_tkld_inv'
    else:
        tkld_col = None

    cols_to_scale = [m for m in selected_metrics if m != 'take-ons_tkld']
    if tkld_col:
        cols_to_scale.append(tkld_col)
    
    #outlier ratio to apply correct scale method
    desc = df[cols_to_scale].describe(percentiles=[0.01, 0.25, 0.75, 0.99]).T
    desc['iqr'] = desc['75%'] - desc['25%']
    desc['outlier_upper'] = desc['99%'] > (desc['75%'] + 1.5 * desc['iqr'])
    desc['outlier_ratio'] = desc['outlier_upper'].astype(int)  
    
    # RobustScaler 
    robust_cols = desc[desc['outlier_ratio'] == 1].index.tolist()
    standard_cols = [c for c in cols_to_scale if c not in robust_cols]

    df_scaled = pd.DataFrame(index=df.index)
    
    if standard_cols:
        #Standart scaler
        scaler_std = StandardScaler()
        df_scaled[standard_cols] = scaler_std.fit_transform(df[standard_cols].fillna(0))
    if robust_cols:
        scaler_rob = RobustScaler()
        df_scaled[robust_cols] = scaler_rob.fit_transform(df[robust_cols].fillna(0))

    # Profile assign
    profiles = {
        'Finisher': ['expected_g-xg', 'standard_g_sh', 'standard_sot_90'],
        'Volume Shooter': ['standard_sh_90', 'standard_fk'],
        'Dribbler': [
            'take-ons_att', 'take-ons_succ', 'take-ons_succpct',
            tkld_col if tkld_col else 'take-ons_tkld'
        ],
        'Playmaker': [
            'gca_gca90', 'gca_types_to', 'gca_types_sh',
            'sca_types_to', 'sca_types_fld', 'carries_cpa'
        ]
    }

    #profile scores logic
    profile_scores = {}
    for profile, metrics in profiles.items():
        valid_metrics = [m for m in metrics if m in df_scaled.columns]
        if valid_metrics:
            profile_scores[profile] = df_scaled[valid_metrics].mean(axis=1)
        else:
            profile_scores[profile] = pd.Series(0, index=df.index)

    for profile, scores in profile_scores.items():
        df[f'{profile}_score'] = scores

    df['attack_profile'] = (
        df[[f'{p}_score' for p in profiles.keys()]]
        .idxmax(axis=1)
        .str.replace('_score', '')
    )

    
    print(f"\nScaler results:")
    print(f"Metrics applied RobustScaler: {len(robust_cols)}")
    print(f"Metrics applied StandartScaler: {len(standard_cols)}")

    return df

def find_players():
    selected_metrics = reduce_columns()
    
    try:
        with sqlite3.connect(db_path) as conn:
            df = pd.read_sql("SELECT * FROM master_table", conn)
            
            basis_cols = ['player', 'nation', 'pos', 'age', 'playing_time_min', 'squad']
            required_cols = basis_cols + selected_metrics
            
            missing_basis = [col for col in basis_cols if col not in df.columns]
            if missing_basis:
                raise ValueError(f"Missing metadata columns: {missing_basis}")
            
            df = df[required_cols].copy()
            
            # attacking players
            df = df[df['pos'].str.contains(r'FW|MF', case=False, na=False, regex=True)]
            
            # +90 minutes for young players could be threshold for youngs
            MIN_MINUTES = 90
            df = df[df['playing_time_min'] >= MIN_MINUTES]
            
            # Age column cleaning
            df['age_clean'] = df['age'].astype(str).str.split('-').str[0]
            df['age'] = pd.to_numeric(df['age_clean'], errors='coerce')
            df = df.dropna(subset=['age'])
            df['is_youth'] = df['age'] <= 23

            df[selected_metrics] = df[selected_metrics].fillna(0)
            print(f"After filter {len(df)} FW/MF players exist now.")
            print(f"U23 playeers:: {df['is_youth'].sum()}")
            #-----------
            
            #playmaker columns was not in the column
            playmaker_cols = ['gca_gca90','gca_types_to','gca_types_sh','sca_types_to','sca_types_fld','carries_cpa']
            extra_cols = [c for c in playmaker_cols if c in df.columns and c not in selected_metrics]
            if extra_cols:
                print(f"\nPlaymaker metrics are added: {extra_cols}")
                selected_metrics.extend(extra_cols)
            
            #profile assigngin
            df = assign_profiles(df, selected_metrics)
            
            from sklearn.preprocessing import MinMaxScaler
            
            #overall impact metric,  with selected metrics
            scaler_total = MinMaxScaler(feature_range=(0,0.5))
            scaled_total = scaler_total.fit_transform(df[selected_metrics].fillna(0))
            df['overall_impact'] = scaled_total.mean(axis=1)

            # hidden_gem
            df['minutes_rank'] = df['playing_time_min'].rank(pct=True)
            df['impact_rank'] = df['overall_impact'].rank(pct=True)
            df['hidden_gem'] = (df['impact_rank'] >= 0.7) & (df['minutes_rank'] <= 0.4)

            # high_potential
            df['high_potential_youth'] = df['is_youth'] & (df['impact_rank'] >= 0.6)

            # elite_performer
            df['elite_performer'] = df['impact_rank'] >= 0.9
            
            df_youth = df[df['is_youth']]
            df_youth_copy = df_youth.copy()

            #dispaly cols for dashboard
            display_cols = basis_cols + [
                'attack_profile', 'hidden_gem', 'high_potential_youth', 'elite_performer', 'overall_impact',
                'Finisher_score', 'Dribbler_score', 'Playmaker_score', 'Volume Shooter_score'  
            ]
            display_cols = [col for col in display_cols if col in df_youth.columns]
            
            for col in ['Finisher_score', 'Dribbler_score', 'Playmaker_score', 'Volume Shooter_score', 'overall_impact']:
                if col in df_youth_copy.columns:
                    df_youth_copy[col] = df_youth_copy[col].round(4)
                        
            df_youth_copy[display_cols].to_csv("df.csv", index=False, decimal=".")
            
            print("\nTop 10 young stars:")
            print(df_youth[display_cols].head(10).to_string(index=False))
            
            # Profile dist.
            attack_counts = df_youth.groupby('attack_profile').size().sort_values(ascending=False)
            print("\nProfil dağılımı:")
            print(attack_counts)
            
            return df  

    except Exception as e:
        print(f"Error: {str(e)}")
        raise

