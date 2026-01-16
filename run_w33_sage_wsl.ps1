# PSScriptAnalyzerSettings = @{
#   Rules = @{
#     PSAvoidAssignmentToAutomaticVariable = @{ Enable = $false }
#   }
# }

param(
  [switch]$PySymmetry,
  [ValidateSet('QQ','GF')] [string]$Field = 'QQ',
  [int]$Prime = 1000003
)

$ErrorActionPreference = 'Stop'

$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path

if (-not (Get-Command wsl.exe -ErrorAction SilentlyContinue)) {
  throw "wsl.exe not found on PATH. Ensure WSL is enabled and available in this terminal session."
}

# Convert Windows path -> WSL path via wslpath inside WSL.
$wslRepo = & wsl.exe -d Ubuntu wslpath -a "$repoRoot" 2>$null
if (-not $wslRepo) {
  throw "Could not convert repo path using 'wsl.exe wslpath'. Is WSL installed and a distro initialized?"
}

# Preflight: ensure Sage is available inside WSL.
# Use single quotes so PowerShell does not expand bash's `$?`.
$sageOk = & wsl.exe -d Ubuntu -e bash -lc 'command -v sage >/dev/null 2>&1; echo $?' 2>$null
if ($sageOk -ne '0') {
  throw "Sage is not available inside WSL (command 'sage' not found). Install in WSL, e.g.: sudo apt install -y sagemath  OR micromamba create -n sage -c conda-forge sagemath"
}

$sageArgs = "claude_workspace/w33_sage_incidence_and_h1.py"
if ($PySymmetry) { $sageArgs += " --pysymmetry" }
if ($Field -eq 'GF') { $sageArgs += " --field=GF --prime=$Prime" }

$cmd = "cd '$wslRepo'; bash ./claude_workspace/run_sage.sh $sageArgs"

Write-Host "Running in WSL:" $cmd
& wsl.exe -d Ubuntu -e bash -lc $cmd
