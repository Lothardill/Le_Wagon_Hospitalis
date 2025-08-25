import pandas as pd
from src.hospitalis.cleaning import normalize

def test_normalize_basic_types_and_mapping():
    # données brutes "sales-like" avec virgules, NULL, etc.
    raw = pd.DataFrame({
        "Réf. Article": ["A1", "A2"],
        "Libellé Article": ["Seringue 10ml", "Gants Nitrile"],
        "Fournisseur": ["Medisup", "Clinix"],
        "Quantité": ["3", "4,0"],
        "Prix HT": ["10.0", "5,5"],
        "Mnt TTC": ["36,00", None],
        "Dépôt DMI": ["1", "NULL"],
        "Date Insertion": ["2024-01-01", "invalid"],
    })

    out = normalize(raw)

    # colonnes renommées
    assert {"product_ref", "product_label", "supplier", "quantity",
            "unit_price_ex_vat", "amount_inc_vat",
            "consignment_flag", "inserted_at"} <= set(out.columns)

    # types et conversions
    assert out["quantity"].dtype.kind in "iu"          # int
    assert out["unit_price_ex_vat"].dtype.kind == "f"  # float
    assert out["amount_inc_vat"].dtype.kind == "f"     # float

    # flags dépôt: "1"/"NULL" -> 1/0
    assert set(out["consignment_flag"].dropna().unique()) <= {0, 1}

    # parsing date: 1 valide, 1 NaT
    assert pd.notna(out.loc[0, "inserted_at"])
    assert pd.isna(out.loc[1, "inserted_at"])
