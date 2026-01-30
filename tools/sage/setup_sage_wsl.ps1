<#
PowerShell helper: run the WSL Sage + PySymmetry installer from Windows
Usage (PowerShell):
  Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass; .\tools\sage\setup_sage_wsl.ps1
#>

try {
    wsl.exe --help > $null 2>&1
} catch {
    Write-Error "WSL does not seem to be available. Install WSL (Ubuntu recommended) and re-run this script."
    exit 1
}

$repo = (Get-Location).Path
Write-Output "Converting repo path to WSL path and invoking setup script in WSL..."
$wslPath = wsl.exe wslpath -a "$repo" 2>$null
if ($LASTEXITCODE -ne 0 -or -not $wslPath) {
    Write-Error "Failed to convert path to WSL path. Please run the WSL command manually: cd /mnt/your/path && bash scripts/setup_sage_pysymmetry.sh"
    exit 1
}

# Trim trailing newlines
$wslPath = $wslPath.Trim()
Write-Output "Running in WSL: cd '$wslPath' && bash scripts/setup_sage_pysymmetry.sh"

# Run the WSL installer (this may take time while Sage is installed)
& wsl -e bash -lc "cd '$wslPath' && bash scripts/setup_sage_pysymmetry.sh"

if ($LASTEXITCODE -eq 0) {
    Write-Output "Sage + PySymmetry setup completed successfully. Test with: wsl -e bash -lc \"cd '$wslPath' && ./run_sage.sh src/test_sage_pysymmetry.py\""
} else {
    Write-Error "The WSL setup script failed. Inspect the output above and re-run the WSL script manually for debugging."
}
