@echo off
REM Parent-safe label-based runner with debug output (no nested parentheses)
setlocal
for %%I in ("%~f0") do set "SCRIPT_DIR=%%~dpI"
set "REPO_ROOT=%SCRIPT_DIR%.."


set "VENV_PY=%CD%\.venv\Scripts\python.exe"
if exist "%VENV_PY%" goto have_venv
where python >nul 2>&1
if errorlevel 1 goto no_python
set "PYTHON_EXE=python"
goto run_tests
:have_venv
set "PYTHON_EXE=%VENV_PY%"
goto run_tests
:no_python
echo No python found (neither .venv nor system python). Exiting.
exit /b 2
:run_tests
if not exist logs mkdir logs
"%PYTHON_EXE%" -u -m pytest -q > "%CD%\logs\pytest_all.log" 2>&1
set RC=%ERRORLEVEL%
if exist "%CD%\logs\pytest_all.log" (
  type "%CD%\logs\pytest_all.log"
) else (
  echo No log produced
)
endlocal
exit /b %RC%
:fail_cd
echo Failed to change directory to repo root "%REPO_ROOT%"
exit /b 1















exit /b 1
