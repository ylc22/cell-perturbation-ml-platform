from __future__ import annotations

import duckdb

from src.config import CSV_PATH, DB_PATH


def build_warehouse() -> None:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    con = duckdb.connect(str(DB_PATH))
    con.execute("DROP TABLE IF EXISTS perturbation_samples")
    con.execute(
        "CREATE TABLE perturbation_samples AS SELECT * FROM read_csv_auto(?)",
        [str(CSV_PATH)],
    )
    con.close()


if __name__ == "__main__":
    build_warehouse()
