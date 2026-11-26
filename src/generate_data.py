from __future__ import annotations

import numpy as np
import pandas as pd

from src.config import CSV_PATH, DATA_DIR, GENE_COUNT


def generate(seed: int = 42, n_per_group: int = 18) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    perturbations = [f"GENE_{i:02d}" for i in range(12)]
    cell_types = ["T_cell", "B_cell", "myeloid"]
    batches = ["B1", "B2", "B3"]

    rows = []
    pert_effects = rng.normal(0, 0.8, size=(len(perturbations), GENE_COUNT))
    cell_effects = rng.normal(0, 0.35, size=(len(cell_types), GENE_COUNT))
    batch_effects = rng.normal(0, 0.08, size=(len(batches), GENE_COUNT))

    idx = 0
    for p_i, perturbation in enumerate(perturbations):
        for c_i, cell_type in enumerate(cell_types):
            for _ in range(n_per_group):
                batch_i = int(rng.integers(0, len(batches)))
                dose = float(rng.uniform(0.2, 1.0))
                expression = (
                    dose * pert_effects[p_i]
                    + cell_effects[c_i]
                    + batch_effects[batch_i]
                    + 0.15 * dose * pert_effects[p_i] * (c_i + 1) / len(cell_types)
                    + rng.normal(0, 0.18, size=GENE_COUNT)
                )
                row = {
                    "sample_id": f"S{idx:05d}",
                    "perturbation": perturbation,
                    "cell_type": cell_type,
                    "dose": dose,
                    "batch": batches[batch_i],
                }
                row.update({f"gene_{j:03d}": float(v) for j, v in enumerate(expression)})
                rows.append(row)
                idx += 1

    return pd.DataFrame(rows)


def main() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    df = generate()
    df.to_csv(CSV_PATH, index=False)
    print(f"wrote {len(df)} rows to {CSV_PATH}")


if __name__ == "__main__":
    main()
