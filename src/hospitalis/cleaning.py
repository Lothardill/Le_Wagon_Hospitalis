import pandas as pd

# mapping FR -> EN (adapter si nécessaire)
COLUMN_MAP = {
    "Réf. Article": "product_ref",
    "Libellé Article": "product_label",
    "Fournisseur": "supplier",
    "Quantité": "quantity",
    "Prix HT": "unit_price_ex_vat",
    "Prix TTC": "unit_price_inc_vat",
    "Mnt HT": "amount_ex_vat",
    "Mnt TTC": "amount_inc_vat",
    "Dépôt DMI": "consignment_flag",
    "Date Insertion": "inserted_at",
}

def normalize(df: pd.DataFrame) -> pd.DataFrame:
    """Renomme les colonnes, nettoie les types et standardise un minimum."""
    df = df.rename(columns=COLUMN_MAP)

    if "quantity" in df.columns:
        df["quantity"] = (
            df["quantity"]
            .astype(str)
            .str.replace(",", ".", regex=False)
            .astype(float)
            .fillna(0)
            .round(0)
            .astype(int)
        )

    for col in ["unit_price_ex_vat", "unit_price_inc_vat", "amount_ex_vat", "amount_inc_vat"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    if "consignment_flag" in df.columns:
        df["consignment_flag"] = (
            df["consignment_flag"].replace("NULL", 0).fillna(0).astype(int)
        )

    if "inserted_at" in df.columns:
        df["inserted_at"] = pd.to_datetime(df["inserted_at"], errors="coerce")

    return df
