param([string]$runId, [int]$intervalSeconds = 8, [int]$timeoutSeconds = 600)
$token = $env:GH_TOKEN
if (-not $token) { Write-Error 'GH_TOKEN not set in environment'; exit 2 }
$headers = @{ Authorization = "token $token" }
$uri = "https://api.github.com/repos/wilcompute/W33-Theory/actions/runs/$runId"
$start = Get-Date
while ($true) {
    try {
        $r = Invoke-RestMethod -Headers $headers -Uri $uri
    } catch {
        Write-Error "Error querying run: $_"
        exit 3
    }
    Write-Output "Status: $($r.status)  Conclusion: $($r.conclusion)  Updated: $($r.updated_at)"
    if ($r.status -eq 'completed') { Write-Output 'RUN_COMPLETED'; break }
    if ((Get-Date) -gt $start.AddSeconds($timeoutSeconds)) { Write-Error 'Timed out waiting for run'; exit 4 }
    Start-Sleep -Seconds $intervalSeconds
}
# Return run JSON
$r | ConvertTo-Json -Depth 5
