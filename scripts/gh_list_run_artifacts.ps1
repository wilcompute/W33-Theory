param([string]$runId)
$token = $env:GH_TOKEN
if (-not $token) { Write-Error 'GH_TOKEN not set in environment'; exit 2 }
$headers = @{ Authorization = "token $token" }
$uri = "https://api.github.com/repos/wilcompute/W33-Theory/actions/runs/$runId/artifacts"
try {
    $resp = Invoke-RestMethod -Headers $headers -Uri $uri
} catch {
    Write-Error "Error calling GitHub API: $_"
    exit 3
}
if ($resp.total_count -eq 0) { Write-Output 'NO_ARTIFACTS'; exit 0 }
$resp.artifacts | Select-Object id,name,size_in_bytes,expired,archive_download_url | ConvertTo-Json -Depth 5
