
POSITION_MAPPINGS = {
    'Goalkeepers': ['GK'],
    'Defenders': ['DF'],
    'Midfielders': ['MF'],
    'Forwards': ['FW']
}

DEFENDER_CATEGORIES = {
    'Defensive Actions': [
        'Tackles_Tkl',               # Tackles
        'Tackles_TklW',              # Tackles won  
        'Tackles_Tkl%',              # Tackle success %
        'Tkl+Int'                    # Tackles + Interceptions
    ],
    'Ball Recovery': [
        'Int',                       # Interceptions
        'Misc_Int',                  # Interceptions (misc)
        'Misc_Recov',                # Ball recoveries
        'Clr'                        # Clearances
    ],
    'Blocking & Protection': [
        'Blocks',             # Blocks
        'Blocks_Sh',                 # Shots blocked
        'Blocks_Pass',               # Passes blocked
        'Err'                        # Errors leading to shots
    ],
    'Aerial Dominance': [
        'Aerial_Duels_Won',         # Aerial duels won
        'Aerial_Duels_Won%',        # Aerial duels won %
        'Aerial_Duels_Lost',        # Aerial duels lost
        'Touches_Def_Pen'           # Touches in def penalty area
    ],
    'Passing Accuracy': [
        'Total_Cmp%',               # Pass completion %
        'Short_Cmp%',               # Short pass completion %
        'Medium_Cmp%',              # Medium pass completion %
        'Long_Cmp%'                 # Long pass completion %
    ],
    'Progressive Passing': [
        'Prgp',                     # Progressive passes
        'Progression_Prgp',          # Progressive passes (std)
        '1_3',                      # Passes into final third
        'Total_Prgdist'             # Progressive passing distance
    ],
    'Ball Playing': [
        'Carries_Prgc',             # Progressive carries
        'Carries_Carries',          # Total carries
        'Total_Totdist',            # Total passing distance
        'Touches_Touches'           # Touches
    ],
    'Set Pieces & Distribution': [
        'Type_Pass_Types_FK',       # Free kicks
        'Type_Pass_Types_CK',       # Corner kicks
        'Type_Pass_Types_Dead',     # Dead ball passes
        'Long_Att'                  # Long passes attempted
    ]
}

MIDFIELDER_CATEGORIES = {
    'Passing Accuracy': [
        'Total_Cmp%',               # Pass completion %
        'Short_Cmp%',               # Short pass completion %
        'Medium_Cmp%',              # Medium pass completion %
        'Long_Cmp%'                 # Long pass completion %
    ],
    'Progressive Passing': [
        'Prgp',                     # Progressive passes
        'Progression_Prgp',          # Progressive passes (std)
        '1_3',                      # Passes into final third
        'Total_Prgdist'             # Progressive passing distance
    ],
    'Creativity': [
        'KP',                       # Key passes
        'Expected_xAG',              # Expected Assisted Goals
        'Expected_xA',              # Expected Assists
        'Performance_Ast'            # Assists
    ],
    'Ball Carrying': [
        'Carries_Prgc',             # Progressive carries
        'Carries_Carries',          # Total carries
        'Carries_Prgdist',          # Progressive carry distance
        'Carries_1_3'               # Carries into final third
    ],
    'Defensive Actions': [
        'Performance_TklW',         # Tackles won
        'Performance_Int',          # Interceptions
        'Performance_Recov',        # Ball recoveries
        'Performance_Aerial_Duels_Won%'         # Aerial duels won %
    ],
    'Ball Retention': [
        'Carries_Mis',              # Miscontrols
        'Carries_Dis',              # Dispossessed
        'Receiving_Rec',            # Passes received
        'Touches_Touches'           # Touches
    ],
    'Set Pieces': [
        'Performance_Pkcon',        # Penalty kicks conceded
        'Performance_Pkwon',        # Penalty kicks won
        'Pass_Types_Fk',       # Free kicks
        'Performance_Crs'           # Crosses
    ],
    'Discipline': [
        'Performance_CrdY',          # Yellow cards
        'Performance_CrdR',          # Red cards
        'Performance_Fls',          # Fouls committed
        'Performance_Fld'           # Fouls drawn
    ]
}

FORWARD_CATEGORIES = {
    'Goal Scoring': [
        'Performance_Gls',           # Goals
        'Performance_Gls_90',        # Goals per 90
        'Performance_xG',            # Expected Goals
        'Performance_G-xG'           # Goals - xG
    ],
    'Shooting Quality': [
        'Standard_Sot%',           # Shots on target %
        'Standard_G_Sh',           # Goals per shot
        'Standard_Sh_90',          # Shots per 90
        'Expected_Npxg_Sh'         # npxG per shot
    ],
    'Creativity & Assists': [
        'Performance_Ast',           # Assists
        'Pass_Kp',                       # Key passes
        'Performance_xAG',              # Expected Assisted Goals
        'Pass_Expected_xA'               # Expected Assists
    ],
    'Central Play': [
        'Touches_Att_Pen',          # Touches in att penalty area
        'Aerial_Duels_Won%',        # Aerial duels won %
        'Passes_Received_Rec',            # Passes received (hold-up)
        'Progression_Prgr'           # Progressive passes received
    ],
    'Wide Play': [
        'Performance_Crs',          # Crosses
        'CrsPA',                    # Crosses into penalty area
        'Carries_1_3',                      # Carries into final third
        'Touches_Att_3rd'           # Touches in attacking third
    ],
    'Dribbling & 1v1': [
        'Take_Ons_Succ%',           # Successful take-ons %
        'Take_Ons_Att',             # Take-ons attempted
        'Carries_Prgc',             # Progressive carries
        'Performance_Fld'           # Fouls drawn
    ],
    'Ball Carrying': [
        'Carries_Carries',          # Total carries
        'Carries_TotDist',          # Total carry distance
        'Carries_PrgDist',          # Progressive carry distance
        'Carries_CPA'               # Carries into penalty area
    ],
    'Work Rate': [
        'Performance_Recov',        # Ball recoveries
        'Performance_TklW',         # Tackles won
        'Performance_Int',          # Interceptions
        'Aerial_Duels_Won'          # Aerial duels won
    ]
}

# === GOALKEEPERS CATEGORIES ===
# Not implemented yet - requires goalkeeper specific stats

GOALKEEPER_CATEGORIES = {
    'Shot Stopping': [
        # Bu kategoriler goalkeeper-specific tablolardan gelecek
        # Şu an için boş bırakıyoruz
    ],
    'Distribution': [],
    'Sweeping': [],
    'Cross Handling': [],
    'Pass Accuracy': [],
    'High Claims': [],
    'Long Passing': [],
    'Penalty Saves': []
}

ALL_POSITION_CATEGORIES = {
    'Goalkeepers': GOALKEEPER_CATEGORIES,
    'Defenders': DEFENDER_CATEGORIES,
    'Midfielders': MIDFIELDER_CATEGORIES,
    'Forwards': FORWARD_CATEGORIES
}

def clean_column_name(col_name):
    """Lig prefix'ini temizle (bundesliga_shoot_standard_gls → shoot_standard_gls)"""
    parts = col_name.split('_')
    if len(parts) > 1 and parts[0] in ['bundesliga', 'premier_league', 'la_liga', 'serie_a', 'ligue_1']:
        return '_'.join(parts[1:]) # '_'.join() bu elemanları alt çizgi ile birleştirir. parts[1:] ifadesi ise 1. indexten sonraki elemanları ifade eder.
    return col_name

LEAGUE_PREFIXES = ['bundesliga', 'premier_league', 'la_liga', 'serie_a', 'ligue_1']