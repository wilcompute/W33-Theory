@echo off
cd /d "%~dp0\.."
if not exist .venv\Scripts\python.exe (
  echo venv python not found
  exit /b 2
)
.venv\Scripts\python.exe -c "import jsonschema, sys; print('JSONSCHEMA_OK', jsonschema.__version__)" > logs\jsonschema_check.log 2>&1
type logs\jsonschema_check.log
