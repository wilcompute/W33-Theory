param([string]$jobId)
$token = $env:GH_TOKEN
if (-not $token) { Write-Error 'GH_TOKEN not set in environment'; exit 2 }
$headers = @{ Authorization = "token $token" }
$uri = "https://api.github.com/repos/wilcompute/W33-Theory/actions/jobs/$jobId"
try {
    $resp = Invoke-RestMethod -Headers $headers -Uri $uri
} catch {
    Write-Error "Error calling GitHub API: $_"
    exit 3
}
$resp | ConvertTo-Json -Depth 10
