# Run E8 Sage test inside Sage Docker image and save logs
param(
  [string]$Image = 'sagemath/sagemath:10.7'
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$root = (Get-Location).Path
$logdir = Join-Path $root 'logs'
if (-not (Test-Path $logdir)) { New-Item -ItemType Directory -Path $logdir | Out-Null }
$out = Join-Path $logdir 'E8_test.log'

Write-Host "Running E8 Sage test in Docker image: $Image"
Write-Host "Log file: $out"

$cmd = "docker run --rm -v "${PWD}:/work" -w /work $Image bash -lc "sage -preparse THEORY_PART_CVII_SAGE_E8_TEST.sage && python3 THEORY_PART_CVII_SAGE_E8_TEST.sage.py 2>&1 | tee /work/logs/E8_test.log""
Write-Host "Executing: $cmd"

try {
    iex $cmd
    Write-Host "Done. Logs written to $out"
} catch {
    Write-Error "Failed to run Docker command. Ensure Docker Desktop is installed and running. Error: $_"
    exit 1
}
