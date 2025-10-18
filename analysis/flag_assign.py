import pandas as pd
import sqlite3
from analysis.preprocessing import select_target_columns

from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler, PowerTransformer, QuantileTransformer
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score
import matplotlib.pyplot as plt

import os
import numpy as np

from analysis.profile_assign import reduce_columns, assign_profiles
from analysis.profile_assign import profiles

def assign_flag(df_youth):
    
    selected_metrics = reduce_columns()
    df_youth, _ = assign_profiles(df_youth, selected_metrics, profiles)
            
    profile_cols = [f'{profile}_score' for profile in profiles.keys()]
    
    print(f"Expected profile columns: {profile_cols}")
    print(f"Available columns: {[col for col in profile_cols if col in df_youth.columns]}")
    
    pct_cols = []
    for col in profile_cols:
        if col in df_youth.columns:
            pct_col = f"{col}_pct"
            df_youth[pct_col] = df_youth[col].rank(pct=True, method='average')
            pct_cols.append(pct_col)
        else:
            print(f"{col} not found, skipping...")
    
    if len(pct_cols) == 0:
        raise ValueError("No profile score columns available for calculation!")
    
    print(f"Successfully processed {len(pct_cols)} profile columns")
    
    df_youth['overall_impact_raw'] = df_youth[pct_cols].sum(axis=1)
    df_youth['overall_impact'] = df_youth['overall_impact_raw'].rank(pct=True) * 100

    # player stable value flag examination (by quantile range)
    df_youth['minutes_rank'] = df_youth['playing_time_min'].rank(pct=True)
    df_youth['impact_rank'] = df_youth['overall_impact'].rank(pct=True)
    
    
    # Boolean flags
    df_youth['hidden_gem'] = (df_youth['impact_rank'] >= 0.75) & (df_youth['minutes_rank'] <= 0.30)
    df_youth['high_potential'] = df_youth['impact_rank'].between(0.60, 0.85) & df_youth['minutes_rank'].between(0.45, 0.75)
    df_youth['elite_performer'] = (df_youth['impact_rank'] >= 0.80) & (df_youth['minutes_rank'] >= 0.65)

    df_youth['hidden_gem_score'] = 0.65 * df_youth['impact_rank'] + 0.35 * (1 - df_youth['minutes_rank'])
    df_youth['high_potential_score'] = 0.6 * df_youth['impact_rank'] + 0.4 * df_youth['minutes_rank']
    df_youth['elite_performer_score'] = 0.7 * df_youth['impact_rank'] + 0.3 * df_youth['minutes_rank']
    
    return df_youth


def flag_confidence(row):
    
    imp, minr = row['impact_rank'], row['minutes_rank']
    hidden, elite, highpot = row['hidden_gem'], row['elite_performer'], row['high_potential']
    
    scores = []

    if hidden:
        scores.append(0.5 + 0.5 * (imp - minr))

    if elite:
        scores.append(0.6 + 0.4 * ((imp + minr) / 2))

    if highpot:
        scores.append(0.55 + 0.45 * ((imp + minr) / 2))

    if not any([hidden, elite, highpot]):
        scores.append(0.4 + 0.4 * imp)

    # when multiple flags 
    confidence = max(scores)

    return round(confidence, 2)


def flag_validation(df):

    youth_df = df[df['is_youth']]
    
    print("\n🔍 QUICK VALIDATION RESULTS:")
    print("=" * 50)
    
    # Boolean flags
    player_flags = ['hidden_gem', 'high_potential', 'elite_performer']
    
    print("📊 Talent Distribution (boolean flags):")
    for flag in player_flags:
        pct = youth_df[flag].mean()
        print(f"   {flag}: {pct:.1%}")
    

    other_pct = (~youth_df[player_flags].any(axis=1)).mean()
    print(f"   other: {other_pct:.1%}")
    
    # High confidence
    threshold = youth_df['confidence_score'].quantile(0.65)
    high_conf = (youth_df['confidence_score'] >= threshold).mean()
    print(f"🎯 High Confidence Players: {high_conf:.1%}")
    
    # flag quality 
    for flag in player_flags + ['other']:
        if flag == 'other':
            subset = youth_df[~youth_df[player_flags].any(axis=1)]
        else:
            subset = youth_df[youth_df[flag]]
        
        if len(subset) == 0:
            continue
        
        if flag == 'hidden_gem':
            quality = (subset['minutes_rank'] <= 0.25).mean()
            print(f"{flag} Quality: {quality:.1%} have low minutes")
            
        elif flag == 'elite_performer':
            quality = (subset['minutes_rank'] >= 0.75).mean()
            print(f"{flag} Quality: {quality:.1%} have high minutes")
            
        elif flag == 'high_potential':
            quality = (
                (subset['impact_rank'].between(0.60, 0.80)) &
                (subset['minutes_rank'].between(0.50, 0.70))
            ).mean()
            print(f"{flag} Quality: {quality:.1%} fit ideal impact/minutes range")
            
        else:  # other
            mid_zone = (subset['impact_rank'].between(0.40, 0.70)).mean()
            print(f"⚙️ {flag} Quality: {mid_zone:.1%} have mid-range impact")
    
    # Top priority
    top_priority = (youth_df['confidence_score'] >= 0.85).sum()
    print(f"Top Priority: {top_priority} players")
    
    return {
        'high_confidence_rate': high_conf,
        'top_priority_count': top_priority,
        'profile_balance': max(youth_df[player_flags].mean()) < 0.6
    }
    
    

def flag_purity(df):

    total_count = len(df)
    player_flags = ['hidden_gem', 'high_potential', 'elite_performer']
    purity_results = []

    for flag in player_flags:
        subset = df[df[flag]]
        count = len(subset)
        if count > 1:
            impact_std = subset['impact_rank'].std()
            minutes_std = subset['minutes_rank'].std()
            purity = 1 - ((impact_std + minutes_std) / 2)
            profile_percentage = count / total_count
        else:
            impact_std = minutes_std = purity = profile_percentage = None

        purity_results.append({
            'player_flag': flag,
            'impact_std': impact_std,
            'minutes_std': minutes_std,
            'purity_score': purity,
            'profile_percentage': profile_percentage
        })

    other_subset = df[~df[player_flags].any(axis=1)]
    count = len(other_subset)
    if count > 1:
        impact_std = other_subset['impact_rank'].std()
        minutes_std = other_subset['minutes_rank'].std()
        purity = 1 - ((impact_std + minutes_std) / 2)
        profile_percentage = count / total_count
    else:
        impact_std = minutes_std = purity = profile_percentage = None

    purity_results.append({
        'player_flag': 'other',
        'impact_std': impact_std,
        'minutes_std': minutes_std,
        'purity_score': purity,
        'profile_percentage': profile_percentage
    })

    return pd.DataFrame(purity_results)
