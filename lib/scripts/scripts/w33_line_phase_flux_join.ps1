$ErrorActionPreference = "Stop"

$root = Split-Path -Parent $PSScriptRoot
$phaseCsv = Join-Path $root "data/_workbench/02_geometry/W33_line_phase_map.csv"
$fluxCsv = Join-Path $root "data/_toe/domainwall_to_w33_sensors_20260110/W33_lines_flux_sensitivity_with_Q12_variance.csv"
$outCsv = Join-Path $root "data/_workbench/02_geometry/W33_line_phase_flux_join.csv"
$outMd = Join-Path $root "data/_workbench/02_geometry/W33_line_phase_flux_join.md"

if (-not (Test-Path $phaseCsv)) { throw "Missing $phaseCsv" }
if (-not (Test-Path $fluxCsv)) { throw "Missing $fluxCsv" }

$phase = Import-Csv -Path $phaseCsv
$phaseMap = @{}
foreach ($p in $phase) {
    $phaseMap[[int]$p.line_id] = $p
}

$flux = Import-Csv -Path $fluxCsv
$joined = @()

foreach ($f in $flux) {
    $id = [int]$f.line_id
    if ($phaseMap.ContainsKey($id)) {
        $p = $phaseMap[$id]
        $joined += [PSCustomObject]@{
            line_id = $id
            mean_abs_delta = [double]$f.mean_abs_delta
            var_q_class = $f.var_q_class
            var_q_r = $f.var_q_r
            card_basis = $f.card_basis
            unique_k_mod6 = [int]$p.unique_k_mod6
            unique_k_mod3 = [int]$p.unique_k_mod3
            coord0_unique_k_mod6 = [int]$p.coord0_unique_k_mod6
            coord1_unique_k_mod6 = [int]$p.coord1_unique_k_mod6
            coord2_unique_k_mod6 = [int]$p.coord2_unique_k_mod6
            coord3_unique_k_mod6 = [int]$p.coord3_unique_k_mod6
            k_mod6_counts = $p.k_mod6_counts
            k_mod3_counts = $p.k_mod3_counts
        }
    }
}

$joined | Sort-Object line_id | Export-Csv -Path $outCsv -NoTypeInformation -Encoding utf8

# Summary markdown
$top10 = $joined | Sort-Object mean_abs_delta -Descending | Select-Object -First 10
$k6Groups = $joined | Group-Object unique_k_mod6 | Sort-Object Name
$k6TopGroups = $top10 | Group-Object unique_k_mod6 | Sort-Object Name
$varQGroups = $joined | Group-Object var_q_class | Sort-Object Name

$md = @(
    "# W33 phase + flux sensitivity join",
    "",
    "Sources:",
    '- `data/_workbench/02_geometry/W33_line_phase_map.csv`',
    '- `data/_toe/domainwall_to_w33_sensors_20260110/W33_lines_flux_sensitivity_with_Q12_variance.csv`',
    "",
    "Outputs:",
    '- `data/_workbench/02_geometry/W33_line_phase_flux_join.csv`',
    "",
    "## Distribution: unique k mod 6 (all lines)",
    ""
)
foreach ($g in $k6Groups) {
    $md += "- $($g.Name): $($g.Count)"
}

$md += @("", "## Distribution: unique k mod 6 (top 10 by mean_abs_delta)", "")
foreach ($g in $k6TopGroups) {
    $md += "- $($g.Name): $($g.Count)"
}

$md += @("", "## Distribution: Q12 variance class (all lines)", "")
foreach ($g in $varQGroups) {
    $md += "- $($g.Name): $($g.Count)"
}

$md += @("", "## Top 10 lines by mean_abs_delta", "")
foreach ($row in $top10) {
    $md += "- line $($row.line_id): mean_abs_delta=$([math]::Round($row.mean_abs_delta,6)), unique_k_mod6=$($row.unique_k_mod6), var_q_class=$($row.var_q_class), cards=$($row.card_basis)"
}

$md -join "`n" | Set-Content -Path $outMd -Encoding utf8
Write-Output "Wrote $outCsv"
Write-Output "Wrote $outMd"

