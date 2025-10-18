import pandas as pd
import sqlite3
from analysis.preprocessing import select_target_columns

from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler, PowerTransformer, QuantileTransformer
from sklearn.metrics import silhouette_score
from scipy.stats import spearmanr



import os
import numpy as np

db_path = os.path.abspath("data/data.db")

def select_non_redundant(metrics, data, scores, corr_threshold=0.85, max_n=5):
    selected = []
    for metric in metrics:
        if len(selected) >= max_n:
            break
        if not selected:
            selected.append(metric)
        else:
            redundant = False
            for sel in selected:
                x, y = data[metric], data[sel]
                valid = ~(x.isna() | y.isna())
                if valid.sum() < 2:
                    corr = 0
                else:
                    corr, _ = spearmanr(x[valid], y[valid])
                if abs(corr) > corr_threshold:
                    redundant = True
                    break
            if not redundant:
                selected.append(metric)
    return selected

def apply_inverse_transform(df, metrics_to_invert):
    
    df = df.copy()
    for col in metrics_to_invert:
        if col in df.columns:
            df[f"{col}_inv"] = 1 / (df[col] + 1)
    return df

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
                    print(f"No metrics found for'{category}'")
                    continue
                
                numeric_cols = df[availables].select_dtypes(include=np.number).columns.tolist()
                if not numeric_cols:
                    print(f"No numeric metrics in '{category}'")
                    continue
                
                print(f"Total metrics in category: {len(numeric_cols)}")
                
                # Step 1: Coefficient of Variation (CV)
                data = df[numeric_cols].fillna(0)
                data = df[numeric_cols].fillna(0).clip(lower=0)
                data_log = np.log1p(data)
                means = data_log.mean()
                stds = data_log.std()
                cv = pd.Series(
                    np.where(np.abs(means) > 1e-8, stds / np.abs(means), 0), 
                    index=numeric_cols
                )
                
                if len(numeric_cols) > 1:
                    cv_values = cv.values.reshape(-1, 1)
                    cv_norm = MinMaxScaler().fit_transform(cv_values).flatten()
                else:
                    cv_norm = [1.0]

                cv_series = pd.Series(cv_norm, index=numeric_cols)
                
                # Step 2: Redundancy (correlation)
                if len(numeric_cols) == 1:
                    redundancy = pd.Series([0.0], index=numeric_cols)
                else:
                    corr = data_log.corr().abs()
                    # highly corr pairs 
                    redundancy = (corr > 0.85).sum(axis=1) / len(numeric_cols)
                                
                score = cv_series / (1 + redundancy)
                
                candidate_metrics = score[score >= 0.05].index.tolist()

                # Non-redundant 
                top_metrics = select_non_redundant(
                    metrics=candidate_metrics,
                    data=data_log[numeric_cols],
                    scores=score,
                    corr_threshold=0.85,
                    max_n=5
                )
                selected_metrics.extend(top_metrics)
                
                print(f"Selected {len(top_metrics)} metrics:")
                for metric in top_metrics:
                    row = metrics_df[metrics_df['Metric'] == metric].iloc[0]
                    print(f"- {metric}")
                    print(f"CV: {cv[metric]:.3f} | Score: {score[metric]:.3f}")
            
            selected_metrics = list(dict.fromkeys(selected_metrics))
            
            if 'carries_dis' in selected_metrics or 'carries_mis' in selected_metrics:
                df = apply_inverse_transform(df, ['carries_dis', 'carries_mis'])

            
            print(f"\n✅ Total selected metrics: {len(selected_metrics)}")
            print("\nFinal metric list:")
            for i, metric in enumerate(selected_metrics, 1):
                if metric in metrics_df['Metric'].values:
                    row = metrics_df[metrics_df['Metric'] == metric].iloc[0]
                    print(f"{i}. [{row['Category']}] {metric}: {row['Description']}")
                else:
                    print(f"{i}. {metric}")
            
            return selected_metrics
    except Exception as e:
        print("Error:", str(e))
        raise


profiles = {
    'Finisher': [
        'standard_g_sh',       # Goals per shot 
        'expected_xg',         # Expected Goals (xG)
        'standard_sot',        # Shots on target – accuracy and ability to hit the target
        'standard_sh_90',      # Shots per 90 minutes 
        'sca_types_sh'         # Shot-Creating Actions from shots – contribution to team's shooting opportunities
    ],
    'Dribbler': [
        'gca_types_to',        # Goal-Creating Actions from take-ons – directly leads to goals by beating defender
        'sca_types_to',        # Shot-Creating Actions from take-ons – generates scoring chances via dribbling
        'carries_cpa',         # Carries into the penalty area – 
        'carries_1_3',         # Carries into the final third – progressive ball progression into attacking areas
        'progression_prgc',    # Progressive carries – carries that significantly advance the ball toward goal
        'carries_mis',         # Miscontrols during carries – loss of possession due to poor first touch or control
        'carries_dis'          # Dispossessed during carries – loss of possession due to opponent pressure
    ],
    'Playmaker': [
        'gca_gca',             # Total Goal-Creating Actions – overall contribution to goal-scoring sequences
        'sca_types_fld',       # Shot-Creating Actions from drawing fouls 
        'sca_types_to',        # Shot-Creating Actions from take-ons 
        'carries_cpa',         # Carries into the penalty area 
        'progression_prgc',    # Progressive carries – key metric for build-up and ball progression
        'carries_mis',         # Miscontrols during carries – reflects technical reliability under pressure
        'carries_dis'          # Dispossessed during carries – indicates vulnerability when retaining possession
    ],
    'Volume_Shooter': [
        'standard_fk',         # Free kick shots 
        'standard_sh_90',      # Shots per 90 minutes 
        'standard_sot',        # Shots on target – ensures volume isn't purely speculative
        'sca_types_sh',        # Shot-Creating Actions from shots – involvement in team's shooting plays
        'expected_xg'          # Expected Goals (xG) 
    ]
}


def assign_profiles(df, selected_metrics, profiles):
    
    df = df.copy()
    
    # take-ons_tkld reverse for the logic of the metric
    if 'take-ons_tkld' in selected_metrics:
        df['take-ons_tkld_inv'] = 1 / (1 + df['take-ons_tkld'])
        tkld_col = 'take-ons_tkld_inv'
    else:
        tkld_col = None

    cols_to_scale = [m for m in selected_metrics if m != 'take-ons_tkld']
    if tkld_col:
        cols_to_scale.append(tkld_col)
    
    #scaling decisions to distrb.
    scaling_decisions = {}

    for col in cols_to_scale:
        data = df[col].fillna(0)
        
        # upper / lower outliers and skewness examined
        Q1, Q3 = data.quantile([0.25, 0.75])
        IQR = Q3 - Q1
        upper_outliers = data.quantile(0.99) > (Q3 + 1.5 * IQR)
        lower_outliers = data.quantile(0.01) < (Q1 - 1.5 * IQR)
        
        skew_val = data.skew()
        
        if upper_outliers or lower_outliers:
            scaling_decisions[col] = 'quantile' if abs(skew_val) > 3 else 'robust'
        elif abs(skew_val) > 1.5:
            scaling_decisions[col] = 'power'
        else:
            scaling_decisions[col] = 'standard'

    
    df_scaled = pd.DataFrame(index=df.index)
    for col, scaler_type in scaling_decisions.items():
        if scaler_type == 'standard':
            df_scaled[col] = StandardScaler().fit_transform(df[[col]].fillna(0))
        elif scaler_type == 'robust':
            df_scaled[col] = RobustScaler().fit_transform(df[[col]].fillna(0))
        elif scaler_type == 'power':
            df_scaled[col] = PowerTransformer().fit_transform(df[[col]].fillna(0))
        elif scaler_type == 'quantile':
            df_scaled[col] = QuantileTransformer(output_distribution='normal').fit_transform(df[[col]].fillna(0))


    # Profile assign
    
    #profile scores logic
    profile_data = []
    for profile in profiles.keys():
        valid_metrics = [m for m in profiles[profile] if m in df_scaled.columns]
        if valid_metrics:
            profile_data.append(df_scaled[valid_metrics].mean(axis=1))
        else:
            profile_data.append(pd.Series(0, index=df.index))
    
    
    normalized_profile_scores = {}
    scaling_reports = {}
    
    for i, profile in enumerate(profiles.keys()):
        raw_scores = profile_data[i]
        
        # Scaler selectiın (same logic as before)
        data = raw_scores.fillna(0)
        Q1, Q3 = data.quantile([0.25, 0.75])
        IQR = Q3 - Q1
        upper_outliers = data.quantile(0.99) > (Q3 + 1.5 * IQR)
        lower_outliers = data.quantile(0.01) < (Q1 - 1.5 * IQR)
        skew_val = data.skew()
        
        # apply optimal scaler
        if upper_outliers or lower_outliers:
            if abs(skew_val) > 3:
                scaler = QuantileTransformer(output_distribution='normal', random_state=42)
                scaler_type = 'quantile'
            else:
                scaler = RobustScaler()
                scaler_type = 'robust'
        elif abs(skew_val) > 1.5:
            scaler = PowerTransformer()
            scaler_type = 'power'
        else:
            normalized_scores = (data - data.mean()) / data.std()
            normalized_profile_scores[profile] = normalized_scores
            scaling_reports[profile] = 'standard'
            continue
        
        normalized_scores = scaler.fit_transform(data.values.reshape(-1, 1)).flatten()
        normalized_profile_scores[profile] = pd.Series(normalized_scores, index=data.index)
        scaling_reports[profile] = scaler_type
    
    #RDA (ref. distrb. alignment)
    # Profile assign - PROFESYONEL RDA
    profile_data = []
    for profile in profiles.keys():
        valid_metrics = [m for m in profiles[profile] if m in df_scaled.columns]
        if valid_metrics:
            profile_data.append(df_scaled[valid_metrics].mean(axis=1))
        else:
            profile_data.append(pd.Series(0, index=df.index))
    
    # HAM PROFİL SKORLARI
    raw_profile_scores = {}
    for i, profile in enumerate(profiles.keys()):
        raw_profile_scores[profile] = profile_data[i]
    
    raw_df = pd.DataFrame(raw_profile_scores)
    
    #RDA apply    
    
    print("BEFORE RDA")
    pre_stats = raw_df.agg(['mean', 'std']).round(3)
    print(pre_stats)
    
    # RDA: Moment-preserving alignment
    aligned_scores = {}
    target_mean = raw_df.mean().mean()  # Global mean
    target_std = raw_df.std().mean()    # Global std
    
    for profile in profiles.keys():
        scores = raw_df[profile]
        
        if scores.std() > 0:
            z_scores = (scores - scores.mean()) / scores.std()
            # align the center but preserve distrb 
            aligned = (z_scores * target_std) + target_mean
        else:
            
            aligned = pd.Series(target_mean, index=scores.index)
        
        aligned_scores[profile] = aligned
    
    aligned_df = pd.DataFrame(aligned_scores)
    
    print("AFTER RDA")
    post_stats = aligned_df.agg(['mean', 'std']).round(3)
    print(post_stats)
    
    # RDA success metrics
    post_means = aligned_df.mean()
    mean_alignment = post_means.std() / post_means.mean()
    print(f"RDA Success - Mean Alignment: {mean_alignment:.3f} (should be close enough to 0))")
    
    for profile in profiles.keys():
        scores = aligned_df[profile].values.reshape(-1, 1)  # 2D array 
        
        scaler = MinMaxScaler(feature_range=(0, 100))  #
        final_scores = scaler.fit_transform(scores).flatten()  # retransform 1d array after scaling
        
        # if no variance, 
        if aligned_df[profile].std() == 0:
            final_scores = final_scores * 0 + 50
        
        df[f'{profile}_score'] = final_scores
            
        
    # Profile assign
    profile_cols = [f'{profile}_score' for profile in profiles.keys()]
    df['attack_profile'] = df[profile_cols].idxmax(axis=1).str.replace('_score', '')
    
    # Profile distrb.
    profile_dist = df['attack_profile'].value_counts()
    print(f"📈 Final Profile Distribution:\n{profile_dist}")
    
    return df, profiles


def validate_profile_consistency(df, profiles):
    
    results = {}
    
    for profile, metrics in profiles.items():
        profile_players = df[df['attack_profile'] == profile]
        
        if len(profile_players) > 1:
            available_metrics = [m for m in metrics if m in profile_players.columns]
            if len(available_metrics) == 0:
                continue
            
            profile_score_col = f'{profile}_score'
            
            if profile_score_col in profile_players.columns:
                profile_scores = profile_players[profile_score_col]
            else:
                # Fallback: raw metrics
                profile_scores = profile_players[available_metrics].mean(axis=1)
            
            internal_consistency = profile_scores.std()
            
            
            profile_power = profile_scores.mean() / 100 if profile_score_col in profile_players.columns else profile_scores.mean()
            
            # Dominance ratio: power / internal variaton
            if internal_consistency > 0:
                dominance_ratio = profile_power / internal_consistency
            else:
                dominance_ratio = 0
            
            results[profile] = {
                'player_count': len(profile_players),
                'internal_consistency': round(internal_consistency, 4),  # low is good
                'profile_power': round(profile_power, 4),               # high = good (0-1)
                'dominance_ratio': round(dominance_ratio, 4),          # high = good
                'metrics_used': len(available_metrics)
            }
    
    return pd.DataFrame(results).T


def validate_profile_overlap(df, selected_metrics):
    
    youth_df = df[df['is_youth']].copy()
    
    if len(youth_df) < 10:
        return {"error": "Not enough youth players for overlap analysis"}
    
    #labeling attack profile. 
    profile_mapping = {'Finisher': 0, 'Dribbler': 1, 'Playmaker': 2, 'Volume_Shooter': 3}
    youth_df = youth_df.dropna(subset=['attack_profile'])
    youth_df['profile_label'] = youth_df['attack_profile'].map(profile_mapping)
    
    youth_df = youth_df[youth_df['profile_label'].notna()]
    
    available_metrics = [col for col in selected_metrics if col in youth_df.columns]
    
    if len(available_metrics) < 5:  
        return {"error": f"Not enough metrics available. Found: {available_metrics}"}
    
    # fill na 0 before scaleing
    X_data = youth_df[available_metrics].fillna(0)
    
    if (X_data == 0).all().all():
        return {"error": "All metric values are zero"}
    
    X = StandardScaler().fit_transform(X_data)
    labels = youth_df['profile_label'].values
    
    # En az 2 profil ve her profilde en az 2 oyuncu olmalı
    unique_labels, label_counts = np.unique(labels, return_counts=True)
    if len(unique_labels) < 2:
        return {"error": f"Need at least 2 profiles, found: {len(unique_labels)}"}
    
    if (label_counts < 2).any():
        return {"error": f"Need at least 2 players per profile. Counts: {dict(zip(unique_labels, label_counts))}"}
    
    silhouette = silhouette_score(X, labels)
    
    profile_counts = youth_df['attack_profile'].value_counts()
    
    return {
        'silhouette_score': round(silhouette, 3),
        'profile_balance': round(profile_counts.std() / profile_counts.mean(), 3),
        'min_profile_players': int(profile_counts.min()),
        'profile_distribution': profile_counts.to_dict(),
        'metrics_used': len(available_metrics),
        'total_players': len(youth_df)
    }
    
def validate_profile_realism(df, profiles):
    
    realism_checks = {}
    
    for profile, metrics in profiles.items():
        profile_players = df[df['attack_profile'] == profile]
        
        if len(profile_players) > 0:
            available_metrics = [m for m in metrics if m in profile_players.columns]
            
            if len(available_metrics) > 0:
                profile_score_col = f'{profile}_score'
                
                if profile_score_col in profile_players.columns:
                    # profile power in 0-100 scaling
                    profile_power = profile_players[profile_score_col].mean() / 100
                    realism_checks[f'{profile.lower()}_power'] = round(profile_power, 4)
                else:
                    profile_power = profile_players[available_metrics].mean(axis=1).mean()
                    realism_checks[f'{profile.lower()}_power'] = round(profile_power, 4)
    
    return realism_checks

