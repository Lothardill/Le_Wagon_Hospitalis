import pandas as pd

def score_products_for_rfid(df: pd.DataFrame) -> pd.DataFrame:
    """
    Score simple et lisible pour prioriser la RFID.
    Idée: volume × valeur × dépôt (bonus si dépôt DMI).
    """
    out = df.copy()

    qty = out.get("quantity")
    price = out.get("unit_price_computed")
    depot = out.get("consignment_flag")

    # garde-fous si colonnes manquent
    if qty is None or price is None:
        out["rfid_score"] = pd.NA
        return out

    depot_factor = 1 + (depot.fillna(0) if depot is not None else 0)
    out["rfid_score"] = qty.fillna(0) * price.fillna(0) * depot_factor

    # optionnel: normalisation 0-1 pour lecture rapide
    maxv = out["rfid_score"].max()
    if pd.notna(maxv) and maxv > 0:
        out["rfid_score_norm"] = out["rfid_score"] / maxv

    return out
