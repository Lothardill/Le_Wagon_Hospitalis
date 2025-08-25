import sys
from .io import read_series, to_parquet, from_parquet
from .config import INTERIM, PROCESSED
from .cleaning import normalize
from .pricing import compute_unit_price
from .rfid_selection import score_products_for_rfid

def ingest():
    # Adapter le pattern si besoin (parquet/csv)
    df = read_series("file{i}.parquet", start=1, end=3)
    to_parquet(df, INTERIM / "ingested.parquet")
    print(f"[ingest] -> {INTERIM / 'ingested.parquet'}")

def clean():
    df = from_parquet(INTERIM / "ingested.parquet")
    df = normalize(df)
    to_parquet(df, INTERIM / "clean.parquet")
    print(f"[clean] -> {INTERIM / 'clean.parquet'}")

def enrich():
    df = from_parquet(INTERIM / "clean.parquet")
    df = compute_unit_price(df)
    df = score_products_for_rfid(df)
    to_parquet(df, PROCESSED / "hospitalis.parquet")
    print(f"[enrich] -> {PROCESSED / 'hospitalis.parquet'}")

def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else "help"
    if cmd == "ingest":
        ingest()
    elif cmd == "clean":
        clean()
    elif cmd == "enrich":
        enrich()
    else:
        print("Usage: python -m src.hospitalis.pipeline [ingest|clean|enrich]")

if __name__ == "__main__":
    main()
