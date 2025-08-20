from analysis.create_player_stats import create_position_metric

ID_COLUMNS = ["player", "nation", "pos", "squad", "age", "born", "minutes"]

LIG_PREFIXES =[
    "bundesliga",
    "la_liga",
    "serie_a",
    "premier_league",
    "ligue_1",
]

METRIC_SUFFIXES = [
    "_standard",
    "_shooting",
    "_passing",
    "_goal_and_shot_creating_actions",
    "_possession",
    "_miscellaneous"
]


METRIC_SUFFIX_ABBREVIATIONS = ["std", "shoot", "pass", "gsca", "poss", "misc"]

if __name__ == "__main__":
    create_position_metric(
        db_name="data/data.db",
        output_table="for_metrics",
        lig_prefixes=LIG_PREFIXES, # Yeni parametre
        metric_suffixes=METRIC_SUFFIXES,
        metric_suffix_abbreviations=METRIC_SUFFIX_ABBREVIATIONS,
        id_columns=ID_COLUMNS,
    )