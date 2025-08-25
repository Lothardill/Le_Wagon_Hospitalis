import pandas as pd

def compute_unit_price(df: pd.DataFrame) -> pd.DataFrame:
    """Calcule un prix unitaire robuste à partir des colonnes disponibles."""
    df = df.copy()
    if "quantity" not in df.columns:
        return df

    qty = df["quantity"].replace(0, pd.NA)

    df["unit_price_computed"] = (
        df.get("unit_price_ex_vat")
        .fillna(df.get("unit_price_inc_vat") * 0.8)
        .fillna(df.get("amount_ex_vat") / qty)
        .fillna((df.get("amount_inc_vat") * 0.8) / qty)
    )

    return df
