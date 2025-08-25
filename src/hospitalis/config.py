from pathlib import Path

# Racine du projet
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Répertoires de données (vides par défaut, car pas de données réelles)
DATA_DIR = PROJECT_ROOT / "data"
RAW = DATA_DIR / "raw"
INTERIM = DATA_DIR / "interim"
PROCESSED = DATA_DIR / "processed"

# Crée les dossiers s’ils n’existent pas (facultatif)
for p in (RAW, INTERIM, PROCESSED):
    p.mkdir(parents=True, exist_ok=True)
