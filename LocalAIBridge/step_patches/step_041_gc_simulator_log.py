def build():
    from pathlib import Path
    import textwrap

    file_path = Path("utils/simulator_log.py")
    file_path.parent.mkdir(parents=True, exist_ok=True)

    file_path.write_text(textwrap.dedent("""
        import json
        from pathlib import Path
        from datetime import datetime

        LOG_PATH = Path("data/simulator/diagnostic_log.json")

        def save_sim_event(issue_type, notes=None):
            LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
            log = load_sim_events()

            log.append({
                "timestamp": datetime.now().isoformat(),
                "issue": issue_type,
                "notes": notes or ""
            })

            with open(LOG_PATH, "w") as f:
                json.dump(log, f, indent=4)

        def load_sim_events():
            if LOG_PATH.exists():
                with open(LOG_PATH, "r") as f:
                    return json.load(f)
            return []

        def reset_sim_session():
            if LOG_PATH.exists():
                LOG_PATH.unlink()
    """))

    print("Patch 025 applied: GC simulator diagnostic log added.")
    return [], [], []

if __name__ == "__main__":
    build()
