def build():
    from pathlib import Path
    import json
    import textwrap

    base_path = Path("data/scenarios")
    base_path.mkdir(parents=True, exist_ok=True)

    samples = {
        "Ghost Peaks": {
            "faults": ["ghost_peaks", "baseline_noise"],
            "notes": "Residual contamination or dirty syringe.",
        },
        "Inlet Leak": {
            "faults": ["inlet_leak", "shift_rt"],
            "notes": "Simulates retention time instability due to small leak.",
        },
        "Coelution": {
            "faults": ["coelution"],
            "notes": "Simulates unresolved peaks — method may need rework.",
        },
        "Tailing Peaks": {
            "faults": ["tailing"],
            "notes": "Could indicate dirty inlet, reactive sites in column.",
        },
        "Overload Fronting": {
            "faults": ["fronting"],
            "notes": "Column overload or injection volume too high.",
        }
    }

    for name, content in samples.items():
        fname = f"{name.lower().replace(' ', '_')}.json"
        with open(base_path / fname, "w") as f:
            json.dump(content, f, indent=2)

    scenario_loader = Path("utils/scenario_cards.py")
    scenario_loader.write_text(textwrap.dedent("""
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
    """))

    print("Patch 032 applied: Sample scenario cards installed.")
    return [], [], []

if __name__ == "__main__":
    build()
