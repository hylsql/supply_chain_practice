# daily analyst refresh workflow

import subprocess
import sys
from pathlib import Path

BASE_DIR = Path(__file__).parent

scripts = [
    "data_cleaning.py",
    "kpi_dashboard.py",
    "operations_automation.py",
    "sql_auto_reporting.py",
    "ai_summary.py"
]

for script in scripts:
    script_path = BASE_DIR / script

    print(f"\nRunning {script}...")

    result = subprocess.run(
        [sys.executable, str(script_path)],
        cwd=BASE_DIR,
        capture_output=True,
        text=True
    )

    print(result.stdout)

    if result.returncode != 0:
        print("ERROR:")
        print(result.stderr)
        raise SystemExit(f"{script} failed.")

print("\nAll automations completed successfully.")