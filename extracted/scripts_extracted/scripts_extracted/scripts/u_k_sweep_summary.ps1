$ErrorActionPreference = "Stop"

$root = Split-Path -Parent $PSScriptRoot
$csvPath = Join-Path $root "data/_toe/native_w33_projectors_c24_20260110/u_k_parityminus_k_sweep_keypoints.csv"
$outMd = Join-Path $root "data/_workbench/04_measurement/u_k_sweep_summary.md"

if (-not (Test-Path $csvPath)) { throw "Missing $csvPath" }

$rows = Import-Csv -Path $csvPath
$rows | ForEach-Object {
    $_.k = [int]$_.k
    $_.max_abs_delta = [double]$_.max_abs_delta
}

$byK = $rows | Group-Object k | ForEach-Object {
    $flipCount = @($_.Group | Where-Object { $_.flip -eq "True" }).Count
    $meanMax = ($_.Group | Measure-Object max_abs_delta -Average).Average
    [PSCustomObject]@{
        k = $_.Name
        count = $_.Count
        flip_count = $flipCount
        mean_max_abs_delta = [math]::Round($meanMax, 6)
    }
} | Sort-Object k

$lines = @(
    "# u_k parity-minus sweep summary",
    "",
    "Source:",
    '- `data/_toe/native_w33_projectors_c24_20260110/u_k_parityminus_k_sweep_keypoints.csv`',
    "",
    "## By k",
    ""
)
foreach ($row in $byK) {
    $lines += "- k=$($row.k): count=$($row.count), flip_count=$($row.flip_count), mean_max_abs_delta=$($row.mean_max_abs_delta)"
}

$lines -join "`n" | Set-Content -Path $outMd -Encoding utf8
Write-Output "Wrote $outMd"

