# Run transport CNF export and OR-Tools runner for a range of seeds
# Usage: .\run_transport_all_seeds.ps1 -Start 0 -End 7 -TimeLimit 300 -Workers 8 -UseLexLeader

param(
    [int]$Start = 0,
    [int]$End = 7,
    [int]$TimeLimit = 300,
    [int]$Workers = 8,
    [switch]$UseLexLeader,
    [switch]$UseLexLeaderStrong,
    [int]$LexLeaderPrefixLength = 8
)

$repoRoot = Resolve-Path -Path "$PSScriptRoot\.."
$venvActivate = Join-Path $repoRoot ".venv\Scripts\Activate.ps1"
if (Test-Path $venvActivate) {
    Write-Host "Activating venv: $venvActivate"
    & $venvActivate
}
else {
    Write-Warning "Could not find venv Activate.ps1 at $venvActivate. Please activate your venv manually."
}

$python = Get-Command python -ErrorAction SilentlyContinue | Select-Object -First 1 -ExpandProperty Source
if (-not $python) {
    # fallback to expected venv python
    $python = Join-Path $repoRoot ".venv\Scripts\python.exe"
}

for ($s = $Start; $s -le $End; $s++) {
    Write-Host "Exporting CNF for seed $s"
    $args = @('scripts/transport_csp_cnf_export.py', '--out', "data/transport_seed$s.cnf", '--seeds', "$s")
    if ($UseLexLeader) { $args += '--lexleader' }
    if ($UseLexLeaderStrong) { $args += '--lexleader-strong'; $args += '--lexleader-prefix-length'; $args += $LexLeaderPrefixLength }
    & $python @args
    if ($LASTEXITCODE -ne 0) {
        Write-Warning "Export failed for seed $s (exit code $LASTEXITCODE)"
        continue
    }

    Write-Host "Running OR-Tools runner for seed $s"
    & $python 'scripts/transport_csp_or_tools_larger.py' --seed $s --time_limit $TimeLimit --workers $Workers
}

Write-Host "Done. Generated CNFs saved in data/ and OR-Tools outputs (if OR-Tools available)."
