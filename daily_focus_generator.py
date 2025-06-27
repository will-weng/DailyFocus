import os
import re
from datetime import datetime, timedelta
import subprocess

# Directory of the running script: .../Target Folder/Scripts
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Path to the template in the same folder
TEMPLATE_PATH = os.path.join(SCRIPT_DIR, "daily_focus_template.md")
TARGET_FOLDER = os.path.dirname(SCRIPT_DIR)
SUBLIME_PATH = r"D:\Programs\Sublime Text\subl.exe"

# === Dates ===
today = datetime.now()

# If today is Monday (weekday() == 0), set 'yesterday' to last Friday
if today.weekday() == 0:
    yesterday = today - timedelta(days=3)
else:
    yesterday = today - timedelta(days=1)

# Format strings
today_str = today.strftime('%Y-%m-%d')
yesterday_str = yesterday.strftime('%Y-%m-%d')

# === Determine output file name with counter if needed ===
base_filename = f"{today_str}_daily_focus"
target_file = os.path.join(TARGET_FOLDER, base_filename + ".md")

counter = 1
while os.path.exists(target_file):
    target_file = os.path.join(TARGET_FOLDER, f"{base_filename}_{counter}.md")
    counter += 1

# === Path to yesterday's file (just default, no suffix logic) ===
yesterday_file = os.path.join(TARGET_FOLDER, f"{yesterday_str}_daily_focus.md")

# === Load template ===
with open(TEMPLATE_PATH, 'r', encoding='utf-8') as f:
    content = f.read()

# === Extract from yesterday ===
first_task = ""
rollover_tasks = []
hold_tasks = []
if os.path.exists(yesterday_file):
    with open(yesterday_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        capture_tomorrow_task = False

        for line in lines:
            stripped = line.strip()

            # Detect "Tomorrow’s first task" section
            if "Tomorrow’s first task" in stripped:
                capture_tomorrow_task = True
                continue

            if capture_tomorrow_task and stripped.startswith("- [ ]"):
                task_text = stripped[6:].strip()
                if task_text and task_text != "_______________________":
                    first_task = task_text
                capture_tomorrow_task = False
                continue

            # Roll over unchecked tasks
            if stripped.startswith("- [ ]"):
                task_text = stripped[6:].strip()
                if task_text and task_text != "_______________________":
                    rollover_tasks.append(f"- [ ] [RO] {task_text}")

            # Hold tasks
            if stripped.startswith("- [h]"):
                task_text = stripped[6:].strip()
                if task_text and task_text != "_______________________":
                    hold_tasks.append(f"- [h] {task_text}")

# === Inject content ===
# Replace date placeholder (supports either [DATE] or {{DATE}})
content = content.replace("[DATE]", today_str)

# Replace "Task:" line
content = re.sub(r"(\*\*Task\*\*:\s).*", rf"\1{first_task}", content)

# Replace Block 1
block_1_pattern = r"(### 🔹 TODO List.*?\n)(- \[ \].*\n?)*"
rollover_text = "\n".join(rollover_tasks) + "\n" if rollover_tasks else ""
content = re.sub(block_1_pattern, rf"\1{rollover_text}", content)

# Replace Hold Tasks
hold_tasks_pattern = r"(### 🔹 Hold Tasks.*?\n)(- \[ \].*\n?)*"
hold_text = "\n".join(hold_tasks) + "\n" if hold_tasks else ""
content = re.sub(hold_tasks_pattern, rf"\1{hold_text}", content)

# === Write final file ===
with open(target_file, 'w', encoding='utf-8') as f:
    f.write(content)

# === Launch in Sublime ===
subprocess.Popen([SUBLIME_PATH, target_file])

# Build path to the script
script_name = "pomodoro_timer.pyw"
script_path = os.path.join(os.path.dirname(__file__), script_name)

# Run the script
subprocess.Popen(["pythonw", script_path])