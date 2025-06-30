from analysis.build_metrics import create_position_metric

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
    "_defense",
    "_passing",
    "_passing_types",
    "_possession",
    "_goal_and_shot_creating_actions",
    "_miscellaneous"
]


METRIC_SUFFIX_ABBREVIATIONS = ["std", "def", "pass", "pass_type", "poss", "gsca", "misc"]

if __name__ == "__main__":
    create_position_metric(
        db_name="data/data.db",
        output_table="mid_metrics",
        lig_prefixes=LIG_PREFIXES, # Yeni parametre
        metric_suffixes=METRIC_SUFFIXES,
        metric_suffix_abbreviations=METRIC_SUFFIX_ABBREVIATIONS, # Kısaltmalar
        id_columns=ID_COLUMNS,
    )