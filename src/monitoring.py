def standardized_mean_shift(observed_mean: float, reference_mean: float, reference_std: float) -> float:
    if reference_std <= 0:
        return 0.0
    return abs(observed_mean - reference_mean) / reference_std


def drift_status(shift: float, threshold: float = 1.0) -> str:
    return "drift_detected" if shift >= threshold else "ok"
