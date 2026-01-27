# claude_workspace

Helper scripts and utilities for running verification and collection.

## Running tests locally 🧪

- Create the virtual environment (Windows PowerShell):

  ```powershell
  python -m venv .venv
  .\.venv\Scripts\python.exe -m pip install --upgrade pip
  .\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
  ```

- Run tests without changing PowerShell execution policy (Windows):

  ```cmd
  cd claude_workspace
  scripts\run_local_tests.bat
  # or, to run all tests:
  scripts\run_all_tests.bat
  ```

- Or on PowerShell you can run for the session only:

  ```powershell
  Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
  . .\.venv\Scripts\Activate.ps1
  pytest -q
  ```

## Notes

- CI runs `sage-verification` workflow which produces `SUMMARY_RESULTS.json` and `NUMERIC_COMPARISONS.json` as artifacts. These files are validated by tests using JSON Schemas in `schemas/`.
