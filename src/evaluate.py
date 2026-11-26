import json
from src.config import REGISTRY_PATH

if not REGISTRY_PATH.exists():
    raise SystemExit("Run python -m src.train first.")

print(json.dumps(json.loads(REGISTRY_PATH.read_text())["metrics"], indent=2))
