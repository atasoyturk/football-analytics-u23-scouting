import pandas as pd
import sqlite3

import os
import numpy as np

from analysis.profile_assign import reduce_columns, assign_profiles, validate_profile_consistency, validate_profile_overlap, validate_profile_realism
from analysis.profile_assign import profiles
from analysis.flag_assign import assign_flag, flag_confidence, flag_purity, flag_validation

db_path = os.path.abspath("data/data.db")


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
            df = df[df['pos'].str.fullmatch(r'(FW|MF)(,\s*(FW|MF))*', case=False, na=False)]            
            
            # +90 minutes could be threshold for young players
            MIN_MINUTES = 90
            df = df[df['playing_time_min'] >= MIN_MINUTES]
            
            # Age column cleaning
            df['age_clean'] = df['age'].astype(str).str.split('-').str[0]
            df['age'] = pd.to_numeric(df['age_clean'], errors='coerce')
            df = df.dropna(subset=['age'])
            
            #u23 seelction
            df['is_youth'] = df['age'] <= 23
            df_youth = df[df['is_youth']].copy()

            df[selected_metrics] = df[selected_metrics].fillna(0)
            print(f"After filter {len(df)} FW/MF players exist now.")
            print(f"U23 playeers:: {df['is_youth'].sum()}")
            #-----------
            
            # profile and flag assigning
            df_youth, _ = assign_profiles(df_youth, selected_metrics, profiles)
            df_youth = assign_flag(df_youth)

            #flag confidence 
            df_youth['confidence_score'] = df_youth.apply(flag_confidence, axis=1)
            
            #flag validation 
            validation_results = flag_validation(df_youth)

            if validation_results['high_confidence_rate'] < 0.3:
                print("Low flag confidence rate - adjust thresholds")
            elif validation_results['top_priority_count'] < 10:
                print("Limited top priority talents")
            else:
                print("No problems about flag confidence and priority talents number")
                
            purity_df = flag_purity(df_youth)
            print(purity_df)
            
            
            print(f"High Confidence Rate: {validation_results['high_confidence_rate']:.1%}")
            print(f"Top Priority Talents: {validation_results['top_priority_count']}")
            print(f"Profile Balance: {'Good' if validation_results['profile_balance'] else 'Needs attention'}")
            
            #CSV
            player_flags = ['hidden_gem', 'high_potential', 'elite_performer']
            
            display_cols = basis_cols + [
                'Finisher_score', 'Dribbler_score', 'Playmaker_score', 'Volume_Shooter_score',
                'attack_profile', 'overall_impact', 'confidence_score'
            ] + player_flags 
            
                        
            stability_metrics = ['impact_std', 'minutes_std', 'purity_score', 'profile_percentage']
            
            
            for flag in player_flags:
                purity_info = purity_df[purity_df['player_flag'] == flag]
                if not purity_info.empty:
                    for metric in stability_metrics:
                        df_youth.loc[df_youth[flag], f"{flag}_{metric}"] = purity_info.iloc[0][metric]
                        display_cols.append(f"{flag}_{metric}")   
                        
            round_cols = ['Finisher_score', 'Dribbler_score', 'Playmaker_score', 'Volume_Shooter_score','overall_impact', 'confidence_score',
                          'hidden_gem_impact_std','hidden_gem_minutes_std','hidden_gem_purity_score','hidden_gem_profile_percentage',
                          'high_potential_impact_std','high_potential_minutes_std','high_potential_purity_score','high_potential_profile_percentage',
                          'elite_performer_impact_std','elite_performer_minutes_std','elite_performer_purity_score','elite_performer_profile_percentage']
            
            for col in round_cols:
                if col in df_youth.columns:
                    df_youth[col] = df_youth[col].fillna(0).round(4)
            
            display_cols = list(dict.fromkeys(display_cols))     
            df_youth[display_cols].to_csv("final_df.csv", index=False, decimal=".")
   
            
            # Profile dist.
            attack_counts = df_youth.groupby('attack_profile').size().sort_values(ascending=False)
            print("\nProfile Distrb. :")
            print(attack_counts)
            
            #profile distrb. validation
            consistency_results = validate_profile_consistency(df_youth, profiles)
            overlap_results = validate_profile_overlap(df_youth, selected_metrics)  
            realism_results = validate_profile_realism(df_youth, profiles)
            
            print(consistency_results)
            print(overlap_results)
            print(realism_results)
            
                        
            return df_youth

    except Exception as e:
        print(f"Error: {str(e)}")
        raise


if __name__ == "__main__":
    
    df = find_players()
    