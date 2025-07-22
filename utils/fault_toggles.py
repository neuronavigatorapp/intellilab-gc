
import json
from pathlib import Path

FAULTS_FILE = Path("data/simulator/faults.json")

def save_fault_config(faults: list):
    FAULTS_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(FAULTS_FILE, "w") as f:
        json.dump(faults, f, indent=2)

def load_fault_config():
    if FAULTS_FILE.exists():
        with open(FAULTS_FILE, "r") as f:
            return json.load(f)
    return []

def reset_fault_config():
    if FAULTS_FILE.exists():
        FAULTS_FILE.unlink()
