def build():
    from pathlib import Path

    log_path = Path("utils/maintenance_log.py")
    log_path.parent.mkdir(parents=True, exist_ok=True)

    log_path.write_text("""
import json
from pathlib import Path
from datetime import datetime

def get_log_path(instrument_id):
    return Path("data/maintenance") / f"{instrument_id}.json"

def save_maintenance_entry(instrument_id: str, entry: dict):
    log_file = get_log_path(instrument_id)
    log_file.parent.mkdir(parents=True, exist_ok=True)

    if log_file.exists():
        with open(log_file, "r") as f:
            logs = json.load(f)
    else:
        logs = []

    entry["timestamp"] = datetime.now().isoformat()
    logs.append(entry)

    with open(log_file, "w") as f:
        json.dump(logs, f, indent=4)

def load_maintenance_log(instrument_id: str):
    log_file = get_log_path(instrument_id)
    if log_file.exists():
        with open(log_file, "r") as f:
            return json.load(f)
    return []
""")

    print("✅ Patch 021 applied: Maintenance log backend added.")
    return [], [], []

# Run immediately
if __name__ == "__main__":
    build()
