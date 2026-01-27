@echo off
REM Robust runner: run the full test suite from the repository root and write to logs\pytest_all.log
REM Determine script directory and repository root, then cd there
cd /d "%~dp0\.."
if errorlevel 1 (
  echo Failed to cd to repo root "%~dp0\.."
  exit /b 1
)

REM Prefer virtualenv python at %CD%\.venv\Scripts\python.exe, otherwise fall back to system python
set "VENV_PY=%CD%\.venv\Scripts\python.exe"
if exist "%VENV_PY%" (
  set "PYTHON_EXE=%VENV_PY%"
) else (
  where python >nul 2>&1
  if errorlevel 1 (
    echo No python found (neither .venv nor system python). Exiting.
    exit /b 2
  ) else (
    set "PYTHON_EXE=python"
    echo Using system python
  )
)

if not exist logs mkdir logs
"%PYTHON_EXE%" -u -m pytest -q > "%CD%\logs\pytest_all.log" 2>&1
set RC=%ERRORLEVEL%

if exist "%CD%\logs\pytest_all.log" (
  type "%CD%\logs\pytest_all.log"
) else (
  echo No log produced
)

exit /b %RC%