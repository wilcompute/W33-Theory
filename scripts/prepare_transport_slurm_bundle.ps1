#!/usr/bin/env pwsh
<#
Prepare SLURM CNF bundles for transport CSP seeds 0..127 with strong lex-leader.

Run this locally in the repo (inside the .venv) to export CNFs and produce a
tar.gz bundle ready for submission to a SAT farm. The script calls the
transport_job_generator.py helper which emits CNFs, a SLURM .slurm script,
and a bundle archive when --bundle is passed.

Usage (PowerShell):
  .\scripts\prepare_transport_slurm_bundle.ps1

#>
param(
    [int]$Start = 0,
    [int]$End = 127,
    [int]$TimeLimit = 600,
    [int]$Workers = 8,
    [int]$PrefixLength = 8
)

$repo = Resolve-Path -Path "$PSScriptRoot\.."
$python = Join-Path $repo ".venv\Scripts\python.exe"
if (-not (Test-Path $python)) {
    Write-Warning "Could not find venv python at $python. Activate your venv or adjust the script."
    $python = "python"
}

$script = Join-Path $repo 'scripts\transport_job_generator.py'
$out_dir = Join-Path $repo 'data'

Write-Host "Generating CNF bundle for seeds $Start..$End (lexleader-strong, prefix $PrefixLength)"

& $python $script --seeds "$Start-$End" --time_limit $TimeLimit --workers $Workers --slurm --bundle --lexleader-strong --lexleader-prefix-length $PrefixLength --out_dir $out_dir

Write-Host "Done. Inspect the data/ directory for transport_cnfs_bundle.tar.gz and the manifest."
