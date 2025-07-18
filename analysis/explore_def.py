# analysis/explore_def.py

from analysis.build_metrics import create_position_metric

# Artık 'player' dışındaki ID kolonlarını da buraya ekliyoruz
ID_COLUMNS = ["player", "nation", "pos", "squad", "age", "90s"]

# 1. Adım: Tüm lig öneklerini buraya ekleyin.
# Bu liste, veritabanınızdaki tablo isimlerinin başındaki lig adlarını içermeli.
LIG_PREFIXES = [
    "bundesliga",
    "la_liga",
    "serie_a",
    "premier_league",
    "ligue_1",
    # ... varsa diğer ligleriniz
]

# 2. Adım: Tüm metrik tablosu son eklerini buraya ekleyin.
# Bu liste, her lig için aynı olan metrik kategorisi son eklerini içermeli.
# NOT: _standard, _defense, _passing gibi isimler veritabanında nasılsa öyle olmalı.
METRIC_SUFFIXES = [
    "_standard",
    "_defense",
    "_passing",
    "_passing_types",
    "_possession",
    "_miscellaneous",
    # ... varsa diğer metrik türleri (örn. _goalkeeping, _shooting, _gca, _keepers, _keepers_adv)
]

# 3. Adım: Metrik son ekleri için kısaltmalar belirleyin.
# Bu liste, yukarıdaki METRIC_SUFFIXES ile aynı sırada ve uzunlukta olmalı.
# Her son ek için kısa, benzersiz bir ön ek.
METRIC_SUFFIX_ABBREVIATIONS = [
    "std",
    "def",
    "pass",
    "pass_type", # 'pt' yerine daha açıklayıcı bir isim.
    "poss",
    "misc",
    # ... diğer kısaltmalarınız (örn. "gk", "sht", "gca", "keep", "keep_adv")
]


if __name__ == "__main__":
    create_position_metric(
        db_name="data/data.db",
        output_table="def_metrics",
        lig_prefixes=LIG_PREFIXES, 
        metric_suffixes=METRIC_SUFFIXES, 
        metric_suffix_abbreviations=METRIC_SUFFIX_ABBREVIATIONS, 
        id_columns=ID_COLUMNS
    )