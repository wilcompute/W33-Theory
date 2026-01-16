$ErrorActionPreference = "Stop"

$root = Split-Path -Parent $PSScriptRoot
$canonCsv = Join-Path $root "data/_toe/domainwall_to_w33_sensors_20260110/W33_lines_flux_sensitivity_with_Q12_variance.csv"
$phaseCsv = Join-Path $root "data/_workbench/02_geometry/W33_line_phase_map.csv"
$nativeCsv = Join-Path $root "data/_toe/native_fullgrid_20260110/nativeC24_line_flux_response_ranking_summary.csv"
$winsCsv = Join-Path $root "data/_toe/native_fullgrid_20260110/nativeC24_fullgrid_winners_flux_vs_noflux.csv"
$outCsv = Join-Path $root "data/_workbench/02_geometry/line_feature_table.csv"
$outMd = Join-Path $root "data/_workbench/02_geometry/line_feature_table_summary.md"

if (-not (Test-Path $canonCsv)) { throw "Missing $canonCsv" }
if (-not (Test-Path $phaseCsv)) { throw "Missing $phaseCsv" }
if (-not (Test-Path $nativeCsv)) { throw "Missing $nativeCsv" }
if (-not (Test-Path $winsCsv)) { throw "Missing $winsCsv" }

$canon = Import-Csv -Path $canonCsv
$phase = Import-Csv -Path $phaseCsv
$native = Import-Csv -Path $nativeCsv
$wins = Import-Csv -Path $winsCsv

$phaseMap = @{}
foreach ($p in $phase) { $phaseMap[[int]$p.line_id] = $p }

$nativeMap = @{}
foreach ($n in $native) { $nativeMap[[int]$n.line_id] = $n }

$fluxWinCounts = @{}
$nofluxWinCounts = @{}
foreach ($w in $wins) {
    $f = [int]$w.winner_flux_line_id
    $n = [int]$w.winner_noflux_line_id
    if ($fluxWinCounts.ContainsKey($f)) { $fluxWinCounts[$f] += 1 } else { $fluxWinCounts[$f] = 1 }
    if ($nofluxWinCounts.ContainsKey($n)) { $nofluxWinCounts[$n] += 1 } else { $nofluxWinCounts[$n] = 1 }
}

# Ranking positions
$canonRanks = @{}
$canonSorted = $canon | Sort-Object {[double]$_.mean_abs_delta} -Descending
$idx = 1
foreach ($row in $canonSorted) {
    $canonRanks[[int]$row.line_id] = $idx
    $idx++
}

$nativeRanks = @{}
$nativeSorted = $native | Sort-Object {[double]$_.mean_abs_delta} -Descending
$idx = 1
foreach ($row in $nativeSorted) {
    $nativeRanks[[int]$row.line_id] = $idx
    $idx++
}

$rows = @()
foreach ($c in $canon) {
    $id = [int]$c.line_id
    $p = $phaseMap[$id]
    $n = $nativeMap[$id]
    $rows += [PSCustomObject]@{
        line_id = $id
        card_basis = $c.card_basis
        line_type = $c.line_type
        type = $c.type
        proj_quartet_str = $c.proj_quartet_str
        rainbow_m_tuple_SHDC = $c.rainbow_m_tuple_SHDC
        var_q_class = $c.var_q_class
        var_q_r = $c.var_q_r
        canon_mean_abs_delta = [double]$c.mean_abs_delta
        canon_mean_delta = [double]$c.mean_delta
        native_mean_abs_delta = if ($n) { [double]$n.mean_abs_delta } else { $null }
        native_mean_delta = if ($n) { [double]$n.mean_delta } else { $null }
        canon_rank = $canonRanks[$id]
        native_rank = if ($nativeRanks.ContainsKey($id)) { $nativeRanks[$id] } else { $null }
        rank_delta = if ($nativeRanks.ContainsKey($id)) { $nativeRanks[$id] - $canonRanks[$id] } else { $null }
        flux_winner_count = if ($fluxWinCounts.ContainsKey($id)) { $fluxWinCounts[$id] } else { 0 }
        noflux_winner_count = if ($nofluxWinCounts.ContainsKey($id)) { $nofluxWinCounts[$id] } else { 0 }
        unique_k_mod6 = if ($p) { [int]$p.unique_k_mod6 } else { $null }
        unique_k_mod3 = if ($p) { [int]$p.unique_k_mod3 } else { $null }
        coord0_unique_k_mod6 = if ($p) { [int]$p.coord0_unique_k_mod6 } else { $null }
        coord1_unique_k_mod6 = if ($p) { [int]$p.coord1_unique_k_mod6 } else { $null }
        coord2_unique_k_mod6 = if ($p) { [int]$p.coord2_unique_k_mod6 } else { $null }
        coord3_unique_k_mod6 = if ($p) { [int]$p.coord3_unique_k_mod6 } else { $null }
        k_mod6_counts = if ($p) { $p.k_mod6_counts } else { "" }
        k_mod3_counts = if ($p) { $p.k_mod3_counts } else { "" }
    }
}

$rows | Sort-Object line_id | Export-Csv -Path $outCsv -NoTypeInformation -Encoding utf8

function Pearson($xs, $ys) {
    $n = $xs.Count
    if ($n -eq 0) { return 0.0 }
    $meanX = ($xs | Measure-Object -Average).Average
    $meanY = ($ys | Measure-Object -Average).Average
    $num = 0.0
    $denX = 0.0
    $denY = 0.0
    for ($i = 0; $i -lt $n; $i++) {
        $dx = $xs[$i] - $meanX
        $dy = $ys[$i] - $meanY
        $num += $dx * $dy
        $denX += $dx * $dx
        $denY += $dy * $dy
    }
    if ($denX -eq 0 -or $denY -eq 0) { return 0.0 }
    return $num / [math]::Sqrt($denX * $denY)
}

$valid = $rows | Where-Object { $_.native_mean_abs_delta -ne $null }
$xs = $valid | ForEach-Object { $_.native_mean_abs_delta }
$ys = $valid | ForEach-Object { $_.canon_mean_abs_delta }
$pearson = [math]::Round((Pearson $xs $ys), 6)

$topNative = $rows | Sort-Object native_mean_abs_delta -Descending | Select-Object -First 10
$topCanon = $rows | Sort-Object canon_mean_abs_delta -Descending | Select-Object -First 10
$nativeIds = $topNative | ForEach-Object { $_.line_id }
$canonIds = $topCanon | ForEach-Object { $_.line_id }
$overlap = $nativeIds | Where-Object { $canonIds -contains $_ }
$overlapStr = ($overlap | ForEach-Object { $_.ToString() }) -join ", "

$rankDelta = $rows | Where-Object { $_.rank_delta -ne $null } | Sort-Object { [math]::Abs([int]$_.rank_delta) } -Descending | Select-Object -First 10

$lines = @(
    "# Line feature table summary",
    "",
    "Sources:",
    '- `data/_toe/domainwall_to_w33_sensors_20260110/W33_lines_flux_sensitivity_with_Q12_variance.csv`',
    '- `data/_workbench/02_geometry/W33_line_phase_map.csv`',
    '- `data/_toe/native_fullgrid_20260110/nativeC24_line_flux_response_ranking_summary.csv`',
    '- `data/_toe/native_fullgrid_20260110/nativeC24_fullgrid_winners_flux_vs_noflux.csv`',
    "",
    "Outputs:",
    '- `data/_workbench/02_geometry/line_feature_table.csv`',
    "",
    "## Correlation",
    "- Pearson (native vs canonical mean_abs_delta): $pearson",
    "",
    "## Top-10 overlap (native vs canonical)",
    "- overlap_count: $($overlap.Count)",
    "- overlap_lines: $overlapStr",
    "",
    "## Largest rank deltas (|native_rank - canon_rank|)",
    ""
)

foreach ($row in $rankDelta) {
    $lines += "- line $($row.line_id): canon_rank=$($row.canon_rank), native_rank=$($row.native_rank), delta=$($row.rank_delta)"
}

$lines -join "`n" | Set-Content -Path $outMd -Encoding utf8
Write-Output "Wrote $outCsv"
Write-Output "Wrote $outMd"

