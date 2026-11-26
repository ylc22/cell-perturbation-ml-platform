import pandas as pd
from src.split import perturbation_holdout


def test_holdout_has_no_perturbation_leakage():
    df = pd.DataFrame({
        "perturbation": ["A", "A", "B", "B", "C", "C", "D", "D"],
        "x": range(8),
    })
    train, test, holdout = perturbation_holdout(df, n_holdout=2)
    assert set(train["perturbation"]).isdisjoint(set(test["perturbation"]))
    assert set(test["perturbation"]) == set(holdout)
