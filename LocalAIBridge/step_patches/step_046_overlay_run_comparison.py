def build():
    from pathlib import Path
    import textwrap

    path = Path("utils/run_compare.py")
    path.parent.mkdir(parents=True, exist_ok=True)

    path.write_text(textwrap.dedent("""
        import json
        from pathlib import Path

        BASELINE_PATH = Path("data/simulator/baseline_run.json")

        def save_baseline_run(peaks):
            BASELINE_PATH.parent.mkdir(parents=True, exist_ok=True)
            with open(BASELINE_PATH, "w") as f:
                json.dump(peaks, f, indent=2)

        def load_baseline_run():
            if BASELINE_PATH.exists():
                with open(BASELINE_PATH, "r") as f:
                    return json.load(f)
            return []

        def has_baseline():
            return BASELINE_PATH.exists()
    """))

    print("Patch 030 applied: Run comparison backend added.")
    return [], [], []

if __name__ == "__main__":
    build()
