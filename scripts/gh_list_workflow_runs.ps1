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
$uri = 'https://api.github.com/repos/wilcompute/W33-Theory/actions/workflows/sage-verification.yml/runs'
try {
    $resp = Invoke-RestMethod -Headers $headers -Uri $uri
} catch {
    Write-Error "Error calling GitHub API: $_"
    exit 3
}
if ($resp.total_count -eq 0) {
    Write-Output "NO_RUNS"
    exit 0
}
$resp.workflow_runs | Select-Object id,status,conclusion,created_at,updated_at,html_url | ConvertTo-Json -Depth 5
