import json
from pathlib import Path
from datetime import datetime

def save_method_with_version(method_data: dict, instrument_id: str):
    base_path = Path("data/methods")
    method_path = base_path / f"{instrument_id}.json"
    method_path.parent.mkdir(parents=True, exist_ok=True)

    # Save current method
    with open(method_path, "w") as f:
        json.dump(method_data, f, indent=4)

    # Save versioned snapshot
    history_path = base_path / "history" / instrument_id
    history_path.mkdir(parents=True, exist_ok=True)
    version = datetime.now().strftime("v%Y%m%d_%H%M%S")
    snapshot_path = history_path / f"{version}.json"

    with open(snapshot_path, "w") as f:
        json.dump(method_data, f, indent=4)
