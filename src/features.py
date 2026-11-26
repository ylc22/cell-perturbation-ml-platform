from __future__ import annotations

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler

CATEGORICAL = ["perturbation", "cell_type", "batch"]
NUMERIC = ["dose"]


def build_preprocessor() -> ColumnTransformer:
    return ColumnTransformer([
        ("categorical", OneHotEncoder(handle_unknown="ignore"), CATEGORICAL),
        ("numeric", StandardScaler(), NUMERIC),
    ])


def split_xy(df: pd.DataFrame):
    genes = [c for c in df.columns if c.startswith("gene_")]
    return df[CATEGORICAL + NUMERIC], df[genes]
