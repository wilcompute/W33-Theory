param([string]$runId)
$token = $env:GH_TOKEN
if (-not $token) { Write-Error 'GH_TOKEN not set in environment'; exit 2 }
$headers = @{ Authorization = "token $token" }
$uri = "https://api.github.com/repos/wilcompute/W33-Theory/actions/runs/$runId/logs"
$out = "artifacts/run_${runId}_logs.zip"
New-Item -ItemType Directory -Force -Path artifacts | Out-Null
Write-Output "Downloading run logs to $out"
try {
    Invoke-WebRequest -Headers $headers -Uri $uri -OutFile $out -UseBasicParsing
} catch {
    Write-Error "Error downloading logs: $_"
    exit 3
}
Write-Output "Download completed: $out (size: $(Get-Item $out).Length)"
# Try to list content of zip
try{
    Add-Type -AssemblyName System.IO.Compression.FileSystem
    $zip = [System.IO.Compression.ZipFile]::OpenRead($out)
    $zip.Entries | ForEach-Object { Write-Output "ENTRY: $($_.FullName) $($_.Length)" }
    $zip.Dispose()
} catch {
    Write-Error "Failed to read zip: $_"
}
