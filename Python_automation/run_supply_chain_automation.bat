@echo off
cd /d "YOUR_PROJECT_PATH"

"..\.venv\Scripts\python.exe" "run_all_automations.py" >> logs\automation_log.txt 2>&1