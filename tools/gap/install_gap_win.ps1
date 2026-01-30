# Download and install GAP 4.15.1 (Windows 64-bit)
# Usage (PowerShell):
#   Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass; .\install_gap_win.ps1

$url = 'https://ftp.gap-system.org/pub/gap/gap-4.15/gap-4.15.1/gap-4.15.1-win64.zip'
$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$zip = Join-Path $root 'gap-4.15.1-win64.zip'
$dest = Join-Path $root 'gap-4.15.1-win64'

$urls = @(
    'https://ftp.gap-system.org/pub/gap/gap-4.15/gap-4.15.1/gap-4.15.1-win64.zip',
    'https://github.com/gap-system/gap/releases/download/v4.15.1/gap-4.15.1-win64.zip'
)
$downloaded = Test-Path $zip
if (-not $downloaded) {
    foreach ($u in $urls) {
        try {
            Write-Output "Attempting download from $u ..."
            Invoke-WebRequest -Uri $u -OutFile $zip -UseBasicParsing -ErrorAction Stop
            Write-Output "Downloaded to $zip"
            $downloaded = $true
            break
        } catch {
            Write-Output "Failed to download from $u: $($_.Exception.Message)"
        }
    }
    if (-not $downloaded) {
        Write-Error "Automatic download failed (possible DNS/network issue). Please download the ZIP manually from one of these URLs and place it at `'$zip'` then re-run the script:`n - https://ftp.gap-system.org/pub/gap/gap-4.15/gap-4.15.1/gap-4.15.1-win64.zip`n - https://github.com/gap-system/gap/releases/download/v4.15.1/gap-4.15.1-win64.zip"
    }
} else {
    Write-Output "ZIP already present: $zip"
}

if ($downloaded) {
    if (-Not (Test-Path $dest)) {
        Write-Output "Extracting $zip to $dest..."
        Expand-Archive -Path $zip -DestinationPath $dest -Force
    } else {
        Write-Output "Destination already exists: $dest"
    }
} else {
    Write-Output "Skipping extraction because the ZIP is missing. Please download the ZIP and re-run the script."
}

$gapBat = Join-Path $dest 'bin\gap.bat'
if (Test-Path $gapBat) {
    $shim = Join-Path $root 'gap.cmd'
    Write-Output "Creating wrapper: $shim"
    Set-Content -Path $shim -Value "@echo off`n\"%~dp0\gap-4.15.1-win64\bin\gap.bat\" %*"
    Write-Output "GAP installed. Run: .\tools\gap\gap.cmd --version"
} else {
    Write-Error "Could not find gap.bat in $dest\bin; please inspect extraction." 
}

Write-Output "Done."