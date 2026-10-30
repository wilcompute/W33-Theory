# One-command setup of a fresh clone on Windows (2026-10-30).
#
#   pwsh -File scripts/bootstrap.ps1            # install Python packages + git hooks, then run the doctor
#   pwsh -File scripts/bootstrap.ps1 -Optional  # also try requirements-optional.txt (failures are not fatal)
#
# Idempotent: rerunning only installs what is missing.  External tools that need an installer (tectonic, PARI/GP, Lean,
# WSL with GAP/Sage/orbifolder) are reported by the doctor with where to get them -- see docs/SETUP.md.
param([switch]$Optional)
$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root

if (-not (Get-Command py -ErrorAction SilentlyContinue)) {
    Write-Host "Python launcher 'py' not found: install Python 3.11+ from python.org (tick 'py launcher')." -ForegroundColor Red
    exit 1
}

Write-Host "[1/4] core Python packages (requirements.txt)"
py -3 -m pip install --upgrade --quiet pip
py -3 -m pip install --quiet -r requirements.txt

if ($Optional) {
    Write-Host "[1b] optional packages (requirements-optional.txt), one at a time"
    Get-Content requirements-optional.txt | Where-Object { $_ -and -not $_.StartsWith("#") } | ForEach-Object {
        py -3 -m pip install --quiet $_ 2>$null
        if ($LASTEXITCODE -ne 0) { Write-Host "    skipped $_ (no wheel for this platform)" -ForegroundColor Yellow }
    }
}

Write-Host "[2/4] git hooks (pre-commit: rediscovery guard, 540 tags, pass-namespace guard, black/isort)"
py -3 -m pre_commit install --install-hooks | Out-Null
git config core.autocrlf false
git config pull.ff only

Write-Host "[3/4] remotes"
$remotes = git remote
if ($remotes -notcontains "origin-https") {
    git remote add origin-https https://github.com/wilcompute/W33-Theory.git
}

Write-Host "[4/4] health check"
py -3 scripts/doctor.py
