from __future__ import annotations

import pandas as pd


def perturbation_holdout(df: pd.DataFrame, n_holdout: int = 3):
    perturbations = sorted(df["perturbation"].unique())
    holdout = perturbations[-n_holdout:]
    train = df[~df["perturbation"].isin(holdout)].copy()
    test = df[df["perturbation"].isin(holdout)].copy()
    return train, test, holdout
