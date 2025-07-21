def build():
    from pathlib import Path
    import json

    file_path = Path("utils/detector_log.py")
    file_path.parent.mkdir(parents=True, exist_ok=True)

    file_path.write_text("""
import json
from pathlib import Path
from datetime import datetime

def get_detector_log_path(instrument_id):
    return Path("data/detectors") / f"{instrument_id}.json"

def save_detector_note(instrument_id: str, detector_type: str, notes: str, severity: str = "normal"):
    log_file = get_detector_log_path(instrument_id)
    log_file.parent.mkdir(parents=True, exist_ok=True)

    if log_file.exists():
        with open(log_file, "r") as f:
            logs = json.load(f)
    else:
        logs = []

    logs.append({
        "timestamp": datetime.now().isoformat(),
        "detector": detector_type,
        "notes": notes,
        "severity": severity
    })

    with open(log_file, "w") as f:
        json.dump(logs, f, indent=4)

def load_detector_notes(instrument_id: str):
    log_file = get_detector_log_path(instrument_id)
    if log_file.exists():
        with open(log_file, "r") as f:
            return json.load(f)
    return []
""")

    print("Patch 023 applied: Detector notes logger added.")
    return [], [], []

# Run on script execution
if __name__ == "__main__":
    build()
