param([string]$jobId)
$token = $env:GH_TOKEN
if (-not $token) {
    # Fall back to gh CLI token if available for interactive auth
    try {
        $token = gh auth token 2>$null
    } catch {
        $token = $null
    }
}
if (-not $token) { Write-Error 'GH_TOKEN not set in environment and gh not authenticated; run `gh auth login` or set GH_TOKEN'; exit 2 }
$headers = @{ Authorization = "token $token" }
$uri = "https://api.github.com/repos/wilcompute/W33-Theory/actions/jobs/$jobId/logs"
$out = "artifacts/job_${jobId}_logs.zip"
New-Item -ItemType Directory -Force -Path artifacts | Out-Null
Write-Output "Downloading logs to $out"
try {
    Invoke-WebRequest -Headers $headers -Uri $uri -OutFile $out -UseBasicParsing
} catch {
    Write-Error "Error downloading logs: $_"
    exit 3
}
# Extract
$dest = "artifacts/job_${jobId}_logs"
if (Test-Path $dest) { Remove-Item -Recurse -Force $dest }
Expand-Archive -Path $out -DestinationPath $dest
Write-Output "Extracted logs to $dest"
# Show tail of log files
Get-ChildItem -Path $dest -Filter '*.txt' -Recurse | ForEach-Object {
    Write-Output "--- $_.FullName ---"
    Get-Content -Path $_.FullName -Tail 200 | Select-String -Pattern 'error|failed|FAIL' -SimpleMatch -NotMatch:$false | Select-Object -First 200
}
