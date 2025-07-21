import os
import json
import argparse
from datetime import datetime

STEP_DIR = "command_chain"
LOG_FILE = "output_log.txt"
SUMMARY_FILE = "summary.json"

def get_all_step_files():
    return sorted([f for f in os.listdir(STEP_DIR) if f.startswith("step_") and f.endswith(".txt")])

def execute_step(step_file):
    created_dirs = []
    created_files = []
    errors = []
    step = step_file.strip().lower()

    print(f"🧠 Executing {step_file}...")

    try:
        if "step_008" in step:
            from app.pages.gc_csv_analyzer import main as create_gc_csv_ui
            created_files = create_gc_csv_ui()
            result = "SUCCESS"
        elif "step_009" in step:
            from app.pages.gc_troubleshooter import main as create_gc_troubleshooter_ui
            created_files = create_gc_troubleshooter_ui()
            result = "SUCCESS"
        elif "step_010" in step:
            from app.pages.maintenance_calendar import main as create_maintenance_calendar_ui
            created_files = create_maintenance_calendar_ui()
            result = "SUCCESS"
        elif "step_011" in step:
            from app.pages.method_builder import main as create_method_builder_ui
            created_files = create_method_builder_ui()
            result = "SUCCESS"
        elif "step_012" in step:
            from app.pages.assign_method import main as create_assign_method_ui
            created_files = create_assign_method_ui()
            result = "SUCCESS"
        elif "step_013" in step:
            from app.pages.method_preview import main as create_method_preview_ui
            created_files = create_method_preview_ui()
            result = "SUCCESS"
        elif "step_014" in step:
            from app.pages.column_inventory import main as create_column_inventory_ui
            created_files = create_column_inventory_ui()
            result = "SUCCESS"
        elif "step_015" in step:
            from app.pages.instrument_dashboard import main as create_instrument_dashboard_ui
            created_files = create_instrument_dashboard_ui()
            result = "SUCCESS"
        elif "step_016" in step:
            from app.pages.instrument_dashboard import update_dashboard_widgets
            created_files = update_dashboard_widgets()
            result = "SUCCESS"

        else:
            result = "SKIPPED"
            errors.append("Unrecognized step file.")
    except Exception as e:
        result = "FAILED"
        errors.append(str(e))

    log_entry = f"[{datetime.now()}] Executed: {step_file}\nResult: {result}\n"
    with open(LOG_FILE, "a", encoding="utf-8") as log:
        log.write(log_entry)

    summary = {
        "status": result.lower(),
        "step_executed": step_file,
        "folders_created": created_dirs,
        "files_created": created_files,
        "errors": errors
    }

    with open(SUMMARY_FILE, "w", encoding="utf-8") as summary_file:
        json.dump(summary, summary_file, indent=2)

    print("✅", step_file, "->", result)

def main():
    parser = argparse.ArgumentParser(description="NeuroBuilder with Batch Mode")
    parser.add_argument("--all", action="store_true", help="Execute all steps in order")
    parser.add_argument("--step", type=str, help="Execute a single step file")
    args = parser.parse_args()

    if args.all:
        for step_file in get_all_step_files():
            execute_step(step_file)
    elif args.step:
        execute_step(args.step)
    else:
        print("No mode selected. Use --all or --step <file>")

if __name__ == "__main__":
    main()
