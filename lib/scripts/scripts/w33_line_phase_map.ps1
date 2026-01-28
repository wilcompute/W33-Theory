$ErrorActionPreference = "Stop"

$root = Split-Path -Parent $PSScriptRoot
$pointsCsv = Join-Path $root "data/_toe/w33_orthonormal_phase_solution_20260110/W33_point_rays_C4_12throot_phases.csv"
$linesCsv = Join-Path $root "data/_sources/w33/W33_lines_tetrads_from_checkpoint_20260109.csv"
$outCsv = Join-Path $root "data/_workbench/02_geometry/W33_line_phase_map.csv"
$outMd = Join-Path $root "data/_workbench/02_geometry/W33_line_phase_map.md"

if (-not (Test-Path $pointsCsv)) { throw "Missing $pointsCsv" }
if (-not (Test-Path $linesCsv)) { throw "Missing $linesCsv" }

$points = Import-Csv -Path $pointsCsv
$pointMap = @{}

foreach ($p in $points) {
    $id = [int]$p.point_id
    $entries = @()
    for ($j = 0; $j -lt 4; $j++) {
        $magKey = "c${j}_mag"
        $kKey = "c${j}_phase_k"
        $mag = 0.0
        if (-not [string]::IsNullOrWhiteSpace($p.$magKey)) {
            $mag = [double]$p.$magKey
        }
        $kRaw = $p.$kKey
        if ($mag -gt 0 -and -not [string]::IsNullOrWhiteSpace($kRaw)) {
            $k = [int][double]$kRaw
            $entries += [PSCustomObject]@{
                coord = $j
                k = $k
                k_mod6 = $k % 6
                k_mod3 = $k % 3
            }
        }
    }
    $pointMap[$id] = $entries
}

$lines = Import-Csv -Path $linesCsv
$outRows = @()

function To-JsonMap($map) {
    $ordered = [ordered]@{}
    foreach ($key in ($map.Keys | Sort-Object)) {
        $ordered["$key"] = $map[$key]
    }
    return ($ordered | ConvertTo-Json -Compress)
}

foreach ($line in $lines) {
    $lineId = [int]$line.line_id
    $ids = @()
    foreach ($token in ($line.point_ids -split " ")) {
        if (-not [string]::IsNullOrWhiteSpace($token)) {
            $ids += [int]$token
        }
    }

    $entries = @()
    foreach ($id in $ids) {
        if ($pointMap.ContainsKey($id)) {
            $entries += $pointMap[$id]
        }
    }

    $k6Counts = @{}
    $k3Counts = @{}
    $coordSets = @{
        0 = New-Object System.Collections.Generic.HashSet[int]
        1 = New-Object System.Collections.Generic.HashSet[int]
        2 = New-Object System.Collections.Generic.HashSet[int]
        3 = New-Object System.Collections.Generic.HashSet[int]
    }

    foreach ($e in $entries) {
        $k6 = $e.k_mod6
        $k3 = $e.k_mod3
        if ($k6Counts.ContainsKey($k6)) {
            $k6Counts[$k6] += 1
        } else {
            $k6Counts[$k6] = 1
        }
        if ($k3Counts.ContainsKey($k3)) {
            $k3Counts[$k3] += 1
        } else {
            $k3Counts[$k3] = 1
        }
        $coordSets[[int]$e.coord].Add([int]$k6) | Out-Null
    }

    $uniqueK6 = $k6Counts.Keys.Count
    $uniqueK3 = $k3Counts.Keys.Count

    $outRows += [PSCustomObject]@{
        line_id = $lineId
        point_ids = ($ids -join " ")
        total_entries = $entries.Count
        unique_k_mod6 = $uniqueK6
        unique_k_mod3 = $uniqueK3
        coord0_unique_k_mod6 = $coordSets[0].Count
        coord1_unique_k_mod6 = $coordSets[1].Count
        coord2_unique_k_mod6 = $coordSets[2].Count
        coord3_unique_k_mod6 = $coordSets[3].Count
        k_mod6_counts = (To-JsonMap $k6Counts)
        k_mod3_counts = (To-JsonMap $k3Counts)
    }
}

$outRows | Sort-Object line_id | Export-Csv -Path $outCsv -NoTypeInformation -Encoding utf8

# Summary markdown
$k6Groups = $outRows | Group-Object unique_k_mod6 | Sort-Object Name
$k3Groups = $outRows | Group-Object unique_k_mod3 | Sort-Object Name
$lowestK6 = $outRows | Sort-Object unique_k_mod6, line_id | Select-Object -First 10

$md = @(
    "# W33 line phase map (k mod 6 / k mod 3)",
    "",
    "Sources:",
    '- `data/_toe/w33_orthonormal_phase_solution_20260110/W33_point_rays_C4_12throot_phases.csv`',
    '- `data/_sources/w33/W33_lines_tetrads_from_checkpoint_20260109.csv`',
    "",
    "Outputs:",
    '- `data/_workbench/02_geometry/W33_line_phase_map.csv`',
    "",
    "## Unique k mod 6 counts",
    ""
)
foreach ($g in $k6Groups) {
    $md += "- $($g.Name): $($g.Count)"
}

$md += @("", "## Unique k mod 3 counts", "")
foreach ($g in $k3Groups) {
    $md += "- $($g.Name): $($g.Count)"
}

$md += @("", "## Lowest unique k mod 6 (first 10 lines)", "")
foreach ($row in $lowestK6) {
    $md += "- line $($row.line_id): unique_k_mod6=$($row.unique_k_mod6), unique_k_mod3=$($row.unique_k_mod3), point_ids=$($row.point_ids)"
}

$md -join "`n" | Set-Content -Path $outMd -Encoding utf8
Write-Output "Wrote $outCsv"
Write-Output "Wrote $outMd"
