$ErrorActionPreference = "Stop"

$root = Split-Path -Parent $PSScriptRoot
$winnersCsv = Join-Path $root "data/_toe/native_fullgrid_20260110/nativeC24_fullgrid_winners_flux_vs_noflux.csv"
$phaseMapCsv = Join-Path $root "data/_workbench/02_geometry/W33_line_phase_map.csv"
$q12Csv = Join-Path $root "data/_toe/domainwall_to_w33_sensors_20260110/W33_lines_flux_sensitivity_with_Q12_variance.csv"
$outMd = Join-Path $root "data/_workbench/04_measurement/native_C24_winner_signature.md"

if (-not (Test-Path $winnersCsv)) { throw "Missing $winnersCsv" }
if (-not (Test-Path $phaseMapCsv)) { throw "Missing $phaseMapCsv" }
if (-not (Test-Path $q12Csv)) { throw "Missing $q12Csv" }

$wins = Import-Csv -Path $winnersCsv
$phase = Import-Csv -Path $phaseMapCsv
$q12 = Import-Csv -Path $q12Csv

$phaseMap = @{}
foreach ($p in $phase) { $phaseMap[[int]$p.line_id] = $p }
$q12Map = @{}
foreach ($q in $q12) { $q12Map[[int]$q.line_id] = $q }

function WinnerStats($rows, $field) {
    $items = @()
    foreach ($r in $rows) {
        $id = [int]$r.$field
        $p = $phaseMap[$id]
        $q = $q12Map[$id]
        $items += [PSCustomObject]@{
            line_id = $id
            unique_k_mod6 = if ($p) { [int]$p.unique_k_mod6 } else { $null }
            var_q_class = if ($q) { $q.var_q_class } else { "" }
        }
    }
    return $items
}

$fluxItems = WinnerStats $wins "winner_flux_line_id"
$nofluxItems = WinnerStats $wins "winner_noflux_line_id"

function GroupCounts($items, $property) {
    return ($items | Group-Object $property | ForEach-Object {
        [PSCustomObject]@{
            key = $_.Name
            count = $_.Count
        }
    }) | Sort-Object count -Descending
}

$fluxK6 = GroupCounts $fluxItems "unique_k_mod6"
$nofluxK6 = GroupCounts $nofluxItems "unique_k_mod6"
$fluxQ12 = GroupCounts $fluxItems "var_q_class"
$nofluxQ12 = GroupCounts $nofluxItems "var_q_class"

$lines = @(
    "# Native C24 winner signature",
    "",
    "Sources:",
    '- `data/_toe/native_fullgrid_20260110/nativeC24_fullgrid_winners_flux_vs_noflux.csv`',
    '- `data/_workbench/02_geometry/W33_line_phase_map.csv`',
    '- `data/_toe/domainwall_to_w33_sensors_20260110/W33_lines_flux_sensitivity_with_Q12_variance.csv`',
    "",
    "## Flux winners: unique k mod 6 counts",
    ""
)
foreach ($row in $fluxK6) {
    $lines += "- k_mod6_unique=$($row.key): $($row.count)"
}

$lines += @("", "## No-flux winners: unique k mod 6 counts", "")
foreach ($row in $nofluxK6) {
    $lines += "- k_mod6_unique=$($row.key): $($row.count)"
}

$lines += @("", "## Flux winners: Q12 variance class counts", "")
foreach ($row in $fluxQ12) {
    $lines += "- var_q_class=$($row.key): $($row.count)"
}

$lines += @("", "## No-flux winners: Q12 variance class counts", "")
foreach ($row in $nofluxQ12) {
    $lines += "- var_q_class=$($row.key): $($row.count)"
}

$lines -join "`n" | Set-Content -Path $outMd -Encoding utf8
Write-Output "Wrote $outMd"
