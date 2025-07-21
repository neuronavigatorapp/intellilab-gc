import os
import time
import subprocess

NEURO_COMMANDS_FILE = "neuro_commands.txt"
STEP_PATCH_DIR = "step_patches"
COMMAND_CHAIN_DIR = "command_chain"

def get_next_available_step_number():
    existing_steps = [f for f in os.listdir(COMMAND_CHAIN_DIR) if f.startswith("step_") and f.endswith(".txt")]
    step_numbers = sorted([int(f.split("_")[1]) for f in existing_steps if f.split("_")[1].isdigit()])
    return step_numbers[-1] + 1 if step_numbers else 1

def run_build_command(step_txt_filename):
    print(f"🧠 Running build step for: {step_txt_filename}")
    subprocess.run(["python", "build.py", "--step", step_txt_filename])

def main():
    print("🧠 PatchRunner AI is watching for neuro_commands.txt... (Ctrl+C to stop)")
    already_processed = set()

    while True:
        if os.path.exists(NEURO_COMMANDS_FILE):
            with open(NEURO_COMMANDS_FILE, "r", encoding="utf-8") as f:
                lines = [line.strip() for line in f if line.strip()]
                for line in lines:
                    if line in already_processed:
                        continue

                    # Generate next step number
                    step_num = get_next_available_step_number()
                    safe_name = line.replace(" ", "_").replace("-", "_").lower()
                    patch_py = f"step_{step_num:03}_{safe_name}_patch.py"
                    patch_txt = f"step_{step_num:03}_{safe_name}.txt"

                    patch_py_path = os.path.join(STEP_PATCH_DIR, patch_py)
                    patch_txt_path = os.path.join(COMMAND_CHAIN_DIR, patch_txt)

                    # Write placeholder patch file
                    with open(patch_py_path, "w", encoding="utf-8") as patch_file:
                        patch_file.write(f"def build():\n    print('TODO: {line}')\n    return [], [], []\n")

                    # Write command file
                    with open(patch_txt_path, "w", encoding="utf-8") as txt_file:
                        txt_file.write(f"Patch request: {line}\n")

                    print(f"🧩 Created patch + command: {patch_py}, {patch_txt}")
                    run_build_command(patch_txt)

                    already_processed.add(line)
                    
                    already_processed.add(line)

                    # Run the newly created patch immediately
                    try:
                        patch_globals = {}
                        with open(patch_py_path, "r", encoding="utf-8") as f:
                            exec(f.read(), patch_globals)

                        # Call the build() function if defined
                        if "build" in patch_globals:
                            patch_globals["build"]()
                    except Exception as e:
                        print(f"❌ Error while executing patch: {e}")


        time.sleep(3)

if __name__ == "__main__":
    main()
