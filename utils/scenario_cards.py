
import json
from pathlib import Path

SCENARIO_DIR = Path("data/scenarios")

def list_scenarios():
    return [f.stem.replace("_", " ").title() for f in SCENARIO_DIR.glob("*.json")]

def load_scenario(name):
    filename = f"{name.lower().replace(' ', '_')}.json"
    path = SCENARIO_DIR / filename
    if not path.exists():
        return {}
    with open(path, "r") as f:
        return json.load(f)
