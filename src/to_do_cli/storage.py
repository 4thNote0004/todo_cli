import json
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[2]
DATA_FILE = ROOT_DIR / "data" / "tasks.json"


def load_tasks():
    if not DATA_FILE.exists():
        save_tasks([])
        return []

    try:
        with DATA_FILE.open(encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []


def save_tasks(data):
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    with DATA_FILE.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
