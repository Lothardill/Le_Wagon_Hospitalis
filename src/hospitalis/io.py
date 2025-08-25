from pathlib import Path
import pandas as pd
from .config import RAW, INTERIM, PROCESSED

def read_series(pattern: str, start: int, end: int) -> pd.DataFrame:
    """
    Lit une série de fichiers dans data/raw avec un pattern du type 'file{i}.parquet' ou 'file{i}.csv'.
    """
    dfs = []
    for i in range(start, end + 1):
        base = RAW / pattern.format(i=i)
        if base.suffix == ".parquet" and base.exists():
            dfs.append(pd.read_parquet(base, engine="pyarrow"))
        elif base.suffix == ".csv" and base.exists():
            dfs.append(pd.read_csv(base))
        else:
            # si pas d'extension dans le pattern, tester parquet puis csv
            p_parquet = base.with_suffix(".parquet")
            p_csv = base.with_suffix(".csv")
            if p_parquet.exists():
                dfs.append(pd.read_parquet(p_parquet, engine="pyarrow"))
            elif p_csv.exists():
                dfs.append(pd.read_csv(p_csv))
    if not dfs:
        raise FileNotFoundError("Aucun fichier trouvé dans data/raw pour ce pattern.")
    return pd.concat(dfs, ignore_index=True)

def to_parquet(df: pd.DataFrame, path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(path, index=False, engine="pyarrow")

def from_parquet(path: Path) -> pd.DataFrame:
    return pd.read_parquet(path, engine="pyarrow")
