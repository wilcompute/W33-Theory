@echo off
REM Alternative robust runner: use pushd to change to repo root and run pytest, writing logs\pytest_all.log
rem Determine the script directory robustly and change to repo root (one directory up)
set "SCRIPT_PATH=%~f0"
for %%I in ("%SCRIPT_PATH%") do set "SCRIPT_DIR=%%~dpI"
set "REPO_ROOT=%SCRIPT_DIR%.."
pushd "%REPO_ROOT%" >nul 2>&1
if errorlevel 1 (
  echo Failed to change directory to repo root "%REPO_ROOT%"
  exit /b 1
)
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
popd
exit /b %RC%
