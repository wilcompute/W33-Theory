@echo off
REM Run tests without requiring PowerShell execution policy changes
if not exist .venv\Scripts\python.exe (
  echo Virtualenv python not found: .venv\Scripts\python.exe
  exit /b 2
)
if not exist logs mkdir logs
.venv\Scripts\python.exe -u -m pytest -vv tests/test_summary.py::test_summary_and_numeric_comparisons -s > logs\pytest_local_cmd.log 2>&1


exit /b %ERRORLEVEL%type logs\pytest_local_cmd.logn