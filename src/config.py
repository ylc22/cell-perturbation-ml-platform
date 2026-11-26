from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data" / "generated"
ARTIFACT_DIR = ROOT / "artifacts"
DB_PATH = DATA_DIR / "perturbations.duckdb"
CSV_PATH = DATA_DIR / "perturbations.csv"
MODEL_PATH = ARTIFACT_DIR / "model.joblib"
REGISTRY_PATH = ARTIFACT_DIR / "registry.json"
FEATURE_SCHEMA_VERSION = "1.0.0"
GENE_COUNT = 32
