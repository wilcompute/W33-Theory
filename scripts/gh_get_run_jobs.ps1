param([string]$runId)
$token = $env:GH_TOKEN
if (-not $token) { Write-Error 'GH_TOKEN not set in environment'; exit 2 }
$headers = @{ Authorization = "token $token" }
$uri = "https://api.github.com/repos/wilcompute/W33-Theory/actions/runs/$runId/jobs"
try {
    $resp = Invoke-RestMethod -Headers $headers -Uri $uri
} catch {
    Write-Error "Error calling GitHub API: $_"
    exit 3
}
$resp.jobs | Select-Object id,name,status,conclusion,started_at,completed_at,html_url | ConvertTo-Json -Depth 5
