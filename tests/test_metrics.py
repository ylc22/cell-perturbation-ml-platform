import numpy as np
from src.metrics import evaluate_matrix


def test_perfect_predictions_score_well():
    y = np.array([[0.0, 1.0], [1.0, 2.0], [2.0, 3.0]])
    metrics = evaluate_matrix(y, y.copy())
    assert metrics["mean_r2"] == 1.0
    assert metrics["rmse"] == 0.0
    assert metrics["mean_pearson"] > 0.99
