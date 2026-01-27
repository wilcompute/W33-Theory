$ErrorActionPreference = "Stop"

$root = Split-Path -Parent $PSScriptRoot
$dir = Join-Path $root "data/_toe/native_fullgrid_20260110"
$winnersCsv = Join-Path $dir "nativeC24_fullgrid_winners_flux_vs_noflux.csv"
$rankingCsv = Join-Path $dir "nativeC24_line_flux_response_ranking_summary.csv"
$canonicalTopCsv = Join-Path $root "data/_toe/flux_response_rankings_20260110/top15_flux_sensitive_lines.csv"
$phaseMapCsv = Join-Path $root "data/_workbench/02_geometry/W33_line_phase_map.csv"
$q12Csv = Join-Path $root "data/_toe/domainwall_to_w33_sensors_20260110/W33_lines_flux_sensitivity_with_Q12_variance.csv"
$outMd = Join-Path $root "data/_workbench/04_measurement/native_C24_fullgrid_summary.md"

if (-not (Test-Path $winnersCsv)) { throw "Missing $winnersCsv" }
if (-not (Test-Path $rankingCsv)) { throw "Missing $rankingCsv" }
if (-not (Test-Path $canonicalTopCsv)) { throw "Missing $canonicalTopCsv" }
if (-not (Test-Path $phaseMapCsv)) { throw "Missing $phaseMapCsv" }
if (-not (Test-Path $q12Csv)) { throw "Missing $q12Csv" }

$wins = Import-Csv -Path $winnersCsv
$rank = Import-Csv -Path $rankingCsv
$canon = Import-Csv -Path $canonicalTopCsv
$phase = Import-Csv -Path $phaseMapCsv
$q12 = Import-Csv -Path $q12Csv

$winnerChanged = ($wins | Where-Object { $_.winner_changed -eq "1" -or $_.winner_changed -eq "True" }).Count

function Group-Winners($rows, $idField) {
    return ($rows | Group-Object -Property mu, $idField | ForEach-Object {
        [PSCustomObject]@{
            mu = $_.Group[0].mu
            line_id = $_.Group[0].$idField
            count = $_.Count
        }
    }) | Sort-Object mu, @{Expression="count";Descending=$true}
}

$fluxCounts = Group-Winners $wins "winner_flux_line_id"
$nofluxCounts = Group-Winners $wins "winner_noflux_line_id"

$top10 = $rank | Sort-Object {[double]$_.mean_abs_delta} -Descending | Select-Object -First 10
$top10Ids = $top10 | ForEach-Object { [int]$_.line_id }

$canonTop10 = $canon | Select-Object -First 10
$canonTop10Ids = $canonTop10 | ForEach-Object { [int]$_.line_id }
$overlap = $top10Ids | Where-Object { $canonTop10Ids -contains $_ }

$phaseMap = @{}
foreach ($p in $phase) { $phaseMap[[int]$p.line_id] = $p }

$q12Map = @{}
foreach ($q in $q12) { $q12Map[[int]$q.line_id] = $q }

$top10Details = @()
foreach ($id in $top10Ids) {
    $p = $phaseMap[$id]
    $q = $q12Map[$id]
    $top10Details += [PSCustomObject]@{
        line_id = $id
        mean_abs_delta = ($top10 | Where-Object { [int]$_.line_id -eq $id }).mean_abs_delta
        unique_k_mod6 = if ($p) { $p.unique_k_mod6 } else { "" }
        var_q_class = if ($q) { $q.var_q_class } else { "" }
    }
}

$joinedAll = @()
foreach ($row in $rank) {
    $id = [int]$row.line_id
    $p = $phaseMap[$id]
    $q = $q12Map[$id]
    $joinedAll += [PSCustomObject]@{
        line_id = $id
        mean_abs_delta = [double]$row.mean_abs_delta
        unique_k_mod6 = if ($p) { [int]$p.unique_k_mod6 } else { $null }
        var_q_class = if ($q) { $q.var_q_class } else { "" }
    }
}

$k6Means = $joinedAll | Where-Object { $_.unique_k_mod6 } | Group-Object unique_k_mod6 | ForEach-Object {
    [PSCustomObject]@{
        unique_k_mod6 = $_.Name
        mean_abs_delta = [math]::Round(($_.Group | Measure-Object mean_abs_delta -Average).Average, 6)
        count = $_.Count
    }
} | Sort-Object unique_k_mod6

$varQMeans = $joinedAll | Where-Object { $_.var_q_class } | Group-Object var_q_class | ForEach-Object {
    [PSCustomObject]@{
        var_q_class = $_.Name
        mean_abs_delta = [math]::Round(($_.Group | Measure-Object mean_abs_delta -Average).Average, 6)
        count = $_.Count
    }
} | Sort-Object var_q_class

$md = @(
    "# Native C24 full-grid summary",
    "",
    "Sources:",
    '- `data/_toe/native_fullgrid_20260110/nativeC24_fullgrid_winners_flux_vs_noflux.csv`',
    '- `data/_toe/native_fullgrid_20260110/nativeC24_line_flux_response_ranking_summary.csv`',
    "",
    "## Winner flips",
    "- winner_changed_count: $winnerChanged / $($wins.Count)",
    "",
    "## Flux winners by mu (line_id: count)",
    ""
)

foreach ($g in $fluxCounts) {
    $md += "- mu=$($g.mu) line=$($g.line_id): $($g.count)"
}

$md += @("", "## No-flux winners by mu (line_id: count)", "")
foreach ($g in $nofluxCounts) {
    $md += "- mu=$($g.mu) line=$($g.line_id): $($g.count)"
}

$md += @("", "## Top 10 lines by mean_abs_delta (native)", "")
foreach ($row in $top10Details) {
    $md += "- line $($row.line_id): mean_abs_delta=$($row.mean_abs_delta), unique_k_mod6=$($row.unique_k_mod6), var_q_class=$($row.var_q_class)"
}

$md += @("", "## Mean mean_abs_delta by unique k mod 6 (native)", "")
foreach ($row in $k6Means) {
    $md += "- k_mod6_unique=$($row.unique_k_mod6): mean_abs_delta=$($row.mean_abs_delta) (n=$($row.count))"
}

$md += @("", "## Mean mean_abs_delta by Q12 variance class (native)", "")
foreach ($row in $varQMeans) {
    $md += "- var_q_class=$($row.var_q_class): mean_abs_delta=$($row.mean_abs_delta) (n=$($row.count))"
}

$md += @("", "## Overlap with canonical top10 (sector-reduced)", "")
$md += "- overlap_count: $($overlap.Count)"
$md += "- overlap_lines: " + ($overlap -join ", ")

$md -join "`n" | Set-Content -Path $outMd -Encoding utf8
Write-Output "Wrote $outMd"

