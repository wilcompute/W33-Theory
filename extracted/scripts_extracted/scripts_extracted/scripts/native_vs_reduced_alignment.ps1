$ErrorActionPreference = "Stop"

$root = Split-Path -Parent $PSScriptRoot
$nativeCsv = Join-Path $root "data/_toe/native_fullgrid_20260110/nativeC24_line_flux_response_ranking_summary.csv"
$reducedCsv = Join-Path $root "data/_toe/flux_response_rankings_20260110/line_flux_response_summary.csv"
$outMd = Join-Path $root "data/_workbench/04_measurement/native_vs_reduced_alignment.md"

if (-not (Test-Path $nativeCsv)) { throw "Missing $nativeCsv" }
if (-not (Test-Path $reducedCsv)) { throw "Missing $reducedCsv" }

$native = Import-Csv -Path $nativeCsv
$reduced = Import-Csv -Path $reducedCsv

$reducedMap = @{}
foreach ($r in $reduced) {
    $reducedMap[[int]$r.line_id] = [double]$r.mean_abs_delta
}

$pairs = @()
foreach ($n in $native) {
    $id = [int]$n.line_id
    if ($reducedMap.ContainsKey($id)) {
        $pairs += [PSCustomObject]@{
            line_id = $id
            native_mean_abs_delta = [double]$n.mean_abs_delta
            reduced_mean_abs_delta = $reducedMap[$id]
        }
    }
}

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

$xs = $pairs | ForEach-Object { $_.native_mean_abs_delta }
$ys = $pairs | ForEach-Object { $_.reduced_mean_abs_delta }
$pearson = [math]::Round((Pearson $xs $ys), 6)

$nativeTop10 = $native | Sort-Object {[double]$_.mean_abs_delta} -Descending | Select-Object -First 10
$reducedTop10 = $reduced | Sort-Object {[double]$_.mean_abs_delta} -Descending | Select-Object -First 10
$nativeIds = $nativeTop10 | ForEach-Object { [int]$_.line_id }
$reducedIds = $reducedTop10 | ForEach-Object { [int]$_.line_id }
$overlap = $nativeIds | Where-Object { $reducedIds -contains $_ }
$overlapStr = ($overlap | ForEach-Object { $_.ToString().Trim() }) -join ", "

$lines = @(
    "# Native vs reduced alignment",
    "",
    "Sources:",
    '- `data/_toe/native_fullgrid_20260110/nativeC24_line_flux_response_ranking_summary.csv`',
    '- `data/_toe/flux_response_rankings_20260110/line_flux_response_summary.csv`',
    "",
    "## Pearson correlation",
    "- mean_abs_delta correlation (native vs reduced): $pearson",
    "",
    "## Top-10 overlap",
    "- overlap_count: $($overlap.Count)",
    "- overlap_lines: $overlapStr"
)

$lines -join "`n" | Set-Content -Path $outMd -Encoding utf8
Write-Output "Wrote $outMd"

