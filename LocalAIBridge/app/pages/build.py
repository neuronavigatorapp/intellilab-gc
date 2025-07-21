# === build.py ===
# One-stop launcher for NeuroBuilder steps, patches, validation, and streamlit preview.

import os
import json
import importlib.util
from datetime import datetime

STEP_DIR = "command_chain"
PATCH_DIR = "step_patches"
SUMMARY_FILE = "summary.json"
LOG_FILE = "output_log.txt"
APP_DIR = "app/pages"

# --- Utilities ---
def load_patch_function(patch_path):
    spec = importlib.util.spec_from_file_location("step_patch", patch_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return getattr(module, "build")

def run_patch(step_file):
    patch_name = step_file.replace(".txt", "_patch.py")
    patch_path = os.path.join(PATCH_DIR, patch_name)
    if os.path.exists(patch_path):
        build_fn = load_patch_function(patch_path)
        try:
            created_files = build_fn()
            return "SUCCESS", created_files, []
        except Exception as e:
            return "FAILED", [], [str(e)]
    return "SKIPPED", [], ["No patch found"]

def get_all_steps():
    return sorted([f for f in os.listdir(STEP_DIR) if f.startswith("step_") and f.endswith(".txt")])

def write_summary(step, result, files, errors):
    summary = {
        "status": result.lower(),
        "step_executed": step,
        "folders_created": [],
        "files_created": files,
        "errors": errors
    }
    with open(SUMMARY_FILE, "w") as f:
        json.dump(summary, f, indent=2)

def log_step(step, result):
    with open(LOG_FILE, "a") as f:
        f.write(f"[{datetime.now()}] {step} -> {result}\n")

def preview_created_files(files):
    print("\n📁 Created:")
    for f in files:
        print(" -", f)

def execute_step(step_file):
    print("\n🧠 Executing:", step_file)
    result, files, errors = run_patch(step_file)
    write_summary(step_file, result, files, errors)
    log_step(step_file, result)
    if result == "SUCCESS":
        preview_created_files(files)
    else:
        print("❌ Errors:", errors)

def launch_streamlit():
    print("\n🚀 Launching Streamlit app...")
    os.system("streamlit run app/pages/home.py")

# --- Main ---
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--all", action="store_true", help="Run all steps")
    parser.add_argument("--step", type=str, help="Run single step")
    parser.add_argument("--launch", action="store_true", help="Launch streamlit UI")
    args = parser.parse_args()

    if args.all:
        for step in get_all_steps():
            execute_step(step)
    elif args.step:
        execute_step(args.step)

    if args.launch:
        launch_streamlit()
