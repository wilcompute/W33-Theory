$venv = ".venv\Scripts\python.exe"
if (-not (Test-Path $venv)) { Write-Error "Virtual env Python not found: $venv"; exit 2 }
$log = "logs\pytest_local.log"
if (-not (Test-Path "logs")) { New-Item -Path "logs" -ItemType Directory | Out-Null }
# Run Python unbuffered and redirect both stdout and stderr to log via cmd.exe to ensure capture on older PowerShell
$cmd = "$venv -u -m pytest -vv tests/test_summary.py::test_summary_and_numeric_comparisons -s"
Write-Output "Running: $cmd"
Start-Process -FilePath "cmd.exe" -ArgumentList "/c", "$cmd > $log 2>&1" -Wait -NoNewWindow
# Output the log to console for quick inspection
Write-Output "---- pytest log start ----"
Get-Content $log -Raw | Write-Output
Write-Output "---- pytest log end ----"
# Return exit code from pytest by parsing last line of log if present
$rc = 1
try {
    $last = Get-Content $log | Select-Object -Last 5
    foreach ($l in $last) {
        if ($l -match '([0-9]+) passed') { $rc = 0; break }
        if ($l -match 'FAILED') { $rc = 2; break }
    }
} catch {
    $rc = 3
}
Write-Output "pytest exit code (inferred): $rc"
exit $rc
