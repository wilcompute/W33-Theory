$ErrorActionPreference = "Stop"

$root = Split-Path -Parent $PSScriptRoot
$dir = Join-Path $root "data/_toe/native_w33_projectors_c24_20260110"
$checkpoint = Join-Path $dir "checkpoint_native_C24_projectors_20260110.json"
$winners = Join-Path $dir "native_C24_projector_winners_keypoints.csv"
$stabilities = Join-Path $dir "native_C24_projector_stabilities_flux_vs_noflux_keypoints.csv"
$outMd = Join-Path $root "data/_workbench/04_measurement/native_C24_summary.md"

if (-not (Test-Path $checkpoint)) { throw "Missing $checkpoint" }
if (-not (Test-Path $winners)) { throw "Missing $winners" }

$ck = Get-Content -Path $checkpoint -Raw | ConvertFrom-Json
$wins = Import-Csv -Path $winners

$paramPoints = ""
if ($ck.param_points) {
    $paramPoints = ($ck.param_points | ForEach-Object { "({0}, {1})" -f $_[0], $_[1] }) -join ", "
}

$flipCount = ($wins | Where-Object { $_.flip -eq "True" }).Count
$lines = @(
    "# Native C24 projectors (summary)",
    "",
    "Source:",
    '- `data/_toe/native_w33_projectors_c24_20260110/checkpoint_native_C24_projectors_20260110.json`',
    '- `data/_toe/native_w33_projectors_c24_20260110/native_C24_projector_winners_keypoints.csv`',
    "",
    "## Core definition",
    "- uvec_definition: $($ck.uvec_definition)",
    "- param_points: $paramPoints",
    "",
    "## Winner flips at keypoints",
    "- flip_count: $flipCount / $($wins.Count)"
)

foreach ($row in $wins) {
    $lines += "- lambda=$($row.lambda), mu=$($row.mu), winner_flux=$($row.winner_flux), winner_noflux=$($row.winner_noflux), flip=$($row.flip)"
}

$lines -join "`n" | Set-Content -Path $outMd -Encoding utf8
Write-Output "Wrote $outMd"

