$root = Split-Path -Parent $PSScriptRoot
$dataDir = Join-Path $root "data"
$outDir = Join-Path $dataDir "_workbench\\00_meta"

New-Item -ItemType Directory -Force -Path $outDir | Out-Null

function To-SnakeCase([string]$name) {
    $lower = $name.ToLowerInvariant()
    $snake = [regex]::Replace($lower, "[^a-z0-9]+", "_")
    $snake = [regex]::Replace($snake, "_+", "_")
    return $snake.Trim('_')
}

function Resolve-ExtractedDir([string]$stem) {
    $lower = $stem.ToLowerInvariant()
    if ($lower -eq "toe_bundle") {
        return Join-Path $dataDir "_archives\\extracted\\toe_bundle"
    }
    if ($lower -like "toe_*") {
        $name = $lower.Substring(4)
        return Join-Path $dataDir ("_toe\\{0}" -f $name)
    }
    if ($lower -like "is_pg32_*") {
        $name = $lower.Substring(8)
        return Join-Path $dataDir ("_pg32\\{0}" -f $name)
    }
    if ($lower -like "pg32_*") {
        $name = $lower.Substring(5)
        return Join-Path $dataDir ("_pg32\\{0}" -f $name)
    }
    if ($lower -like "is_*") {
        $name = $lower.Substring(3)
        return Join-Path $dataDir ("_is\\{0}" -f $name)
    }
    return Join-Path $dataDir $lower
}

$bundleFiles = Get-ChildItem -Path $dataDir -Recurse -File |
    Where-Object { $_.Name -like "*_bundle*.zip" }

$rows = @()
foreach ($file in $bundleFiles) {
    $base = $file.BaseName -replace "\s*\\(\\d+\\)$", ""
    $stemRaw = $base -replace "_bundle$", ""
    $stem = To-SnakeCase $stemRaw
    $candidateDir = Resolve-ExtractedDir $stem
    $rows += [pscustomobject]@{
        bundle_path = $file.FullName
        bundle_name = $file.Name
        bundle_dir = $file.DirectoryName
        size_kb = [math]::Round($file.Length / 1KB, 1)
        stem_name = $stem
        extracted_dir = $candidateDir
        extracted_exists = (Test-Path -Path $candidateDir)
    }
}

$csvPath = Join-Path $outDir "BUNDLE_INDEX.csv"
$rows | Sort-Object bundle_path | Export-Csv -NoTypeInformation -Path $csvPath

$total = $rows.Count
$extracted = ($rows | Where-Object { $_.extracted_exists }).Count
$missing = $total - $extracted
$uniqueStems = ($rows.stem_name | Select-Object -Unique).Count

$mdPath = Join-Path $outDir "BUNDLE_INDEX.md"
$lines = @()
$lines += "# Bundle index"
$lines += ""
$lines += "Summary:"
$lines += "- total bundles: $total"
$lines += "- unique stems: $uniqueStems"
$lines += "- extracted targets present: $extracted"
$lines += "- extracted targets missing: $missing"
$lines += ""
$lines += "Notes:"
$lines += '- stems are `*_bundle.zip` with `_bundle` and trailing ` (n)` removed.'
$lines += '- extracted targets are resolved to `_toe`, `_is`, `_pg32`, or `_archives/extracted`.'
$lines += ""
$lines += "Outputs:"
$lines += '- `data/_workbench/00_meta/BUNDLE_INDEX.csv`'

$lines | Set-Content -Path $mdPath -Encoding UTF8

Write-Host "Wrote $mdPath"
