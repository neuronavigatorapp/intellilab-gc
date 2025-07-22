
import json
from pathlib import Path

CONFIG_FILE = Path("data/simulator/method_config.json")

default_config = {
    "column_length_m": 30,
    "column_id_mm": 0.25,
    "carrier_gas": "Helium",
    "flow_mL_min": 1.2,
    "oven_temp_C": 150
}

def save_sim_method_config(config: dict):
    CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=4)

def load_sim_method_config():
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    return default_config
