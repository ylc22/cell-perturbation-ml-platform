from src.monitoring import drift_status, standardized_mean_shift


def test_standardized_mean_shift():
    assert standardized_mean_shift(1.5, 1.0, 0.5) == 1.0


def test_drift_threshold():
    assert drift_status(0.9) == "ok"
    assert drift_status(1.0) == "drift_detected"
