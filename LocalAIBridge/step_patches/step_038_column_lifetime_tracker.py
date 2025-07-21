def build():
    from pathlib import Path
    import json

    tracker_path = Path("utils/column_tracker.py")
    tracker_path.parent.mkdir(parents=True, exist_ok=True)

    tracker_path.write_text("""
import json
from pathlib import Path
from datetime import datetime, timedelta

def get_column_path(instrument_id):
    return Path("data/columns") / f"{instrument_id}.json"

def set_column_metadata(instrument_id, install_date=None, max_days=30, max_injections=500):
    path = get_column_path(instrument_id)
    path.parent.mkdir(parents=True, exist_ok=True)

    data = {
        "install_date": install_date or datetime.now().strftime("%Y-%m-%d"),
        "max_days": max_days,
        "max_injections": max_injections,
        "injections": 0
    }

    with open(path, "w") as f:
        json.dump(data, f, indent=4)

def increment_injection_count(instrument_id, count=1):
    path = get_column_path(instrument_id)
    if not path.exists():
        return

    with open(path, "r") as f:
        data = json.load(f)

    data["injections"] += count

    with open(path, "w") as f:
        json.dump(data, f, indent=4)

def check_column_status(instrument_id):
    path = get_column_path(instrument_id)
    if not path.exists():
        return "No column info."

    with open(path, "r") as f:
        data = json.load(f)

    install_date = datetime.strptime(data["install_date"], "%Y-%m-%d")
    age_days = (datetime.now() - install_date).days
    expired_by_days = age_days > data["max_days"]
    expired_by_injections = data["injections"] > data["max_injections"]

    if expired_by_days or expired_by_injections:
        return "Column expired — consider replacing."

    return "Column within expected limits."
""")

    print("Patch 022 applied: Column lifetime tracker backend added.")
    return [], [], []

# Run immediately
if __name__ == "__main__":
    build()
