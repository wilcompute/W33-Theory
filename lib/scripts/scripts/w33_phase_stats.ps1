$ErrorActionPreference = "Stop"

$root = Split-Path -Parent $PSScriptRoot
$csvPath = Join-Path $root "data/_toe/w33_orthonormal_phase_solution_20260110/W33_point_rays_C4_12throot_phases.csv"
$outPath = Join-Path $root "data/_workbench/02_geometry/W33_phase_stats.md"

if (-not (Test-Path $csvPath)) {
    throw "Missing $csvPath"
}

$rows = Import-Csv -Path $csvPath

$records = @()
foreach ($row in $rows) {
    $kindValue = ""
    if (-not [string]::IsNullOrWhiteSpace($row.kind)) {
        $kindValue = $row.kind.Trim()
    }
    for ($j = 0; $j -lt 4; $j++) {
        $magKey = "c${j}_mag"
        $kKey = "c${j}_phase_k"
        $mag = 0.0
        if (-not [string]::IsNullOrWhiteSpace($row.$magKey)) {
            $mag = [double]$row.$magKey
        }
        $kRaw = $row.$kKey
        if ($mag -gt 0 -and -not [string]::IsNullOrWhiteSpace($kRaw)) {
            $k = [int][double]$kRaw
            $records += [PSCustomObject]@{
                kind = $kindValue
                coord = $j
                k = $k
                k_mod6 = $k % 6
                k_mod3 = $k % 3
            }
        }
    }
}

function Format-Group($groups, $label) {
    $lines = @("### $label")
    foreach ($g in $groups | Sort-Object Name) {
        $lines += "- $($g.Name): $($g.Count)"
    }
    $lines += ""
    return $lines
}

$totalRays = $rows.Count
$totalEntries = $records.Count
$kindCounts = $rows | ForEach-Object {
    if (-not [string]::IsNullOrWhiteSpace($_.kind)) { $_.kind.Trim() } else { "" }
} | Group-Object | Sort-Object Name

$kindsSummary = ($kindCounts | ForEach-Object { "$($_.Name)=$($_.Count)" }) -join ", "

$lines = @(
    "# W33 phase statistics (12th-root exponents)",
    "",
    'Source: `data/_toe/w33_orthonormal_phase_solution_20260110/W33_point_rays_C4_12throot_phases.csv`',
    "",
    "## Summary",
    "- rays: $totalRays",
    "- nonzero phase entries: $totalEntries",
    "- kinds: $kindsSummary",
    ""
)

$lines += Format-Group ($records | Group-Object k) "Counts by k (0..11)"
$lines += Format-Group ($records | Group-Object k_mod6) "Counts by k mod 6"
$lines += Format-Group ($records | Group-Object k_mod3) "Counts by k mod 3"

# Per-kind breakdown (k mod 6)
foreach ($kind in ($kindCounts | ForEach-Object { $_.Name })) {
    $subset = $records | Where-Object { $_.kind -eq $kind }
    $lines += "### k mod 6 by kind: $kind"
    foreach ($g in $subset | Group-Object k_mod6 | Sort-Object Name) {
        $lines += "- $($g.Name): $($g.Count)"
    }
    $lines += ""
}

$lines -join "`n" | Set-Content -Path $outPath -Encoding utf8
Write-Output "Wrote $outPath"
