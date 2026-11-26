from __future__ import annotations

import numpy as np
from scipy.stats import pearsonr
from sklearn.metrics import mean_squared_error, r2_score


def evaluate_matrix(y_true: np.ndarray, y_pred: np.ndarray) -> dict[str, float]:
    r2_values = []
    corr_values = []

    for j in range(y_true.shape[1]):
        r2_values.append(r2_score(y_true[:, j], y_pred[:, j]))
        if np.std(y_true[:, j]) > 0 and np.std(y_pred[:, j]) > 0:
            corr_values.append(pearsonr(y_true[:, j], y_pred[:, j]).statistic)

    top_true = set(np.argsort(np.mean(np.abs(y_true), axis=0))[-10:])
    top_pred = set(np.argsort(np.mean(np.abs(y_pred), axis=0))[-10:])

    return {
        "mean_r2": float(np.mean(r2_values)),
        "mean_pearson": float(np.mean(corr_values)) if corr_values else 0.0,
        "rmse": float(np.sqrt(mean_squared_error(y_true, y_pred))),
        "top10_gene_overlap": float(len(top_true & top_pred) / 10),
    }
