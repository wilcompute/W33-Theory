$root = Split-Path -Parent $PSScriptRoot
$dataDir = Join-Path $root "data"
$variantDir = Join-Path $dataDir "_variants"
$metaDir = Join-Path $dataDir "_workbench\\00_meta"

New-Item -ItemType Directory -Force -Path $variantDir | Out-Null
New-Item -ItemType Directory -Force -Path $metaDir | Out-Null

$pattern = ' \((\d+)\)(\.[^\.]+)$'
$items = Get-ChildItem -Path $dataDir -File | Where-Object { $_.Name -match $pattern }

$removed = @()
$renamed = @()
$moved = @()

foreach ($file in $items) {
    if ($file.Name -notmatch $pattern) {
        continue
    }
    $suffixNum = $matches[1]
    $ext = $matches[2]
    $baseStem = $file.BaseName -replace ' \(\d+\)$', ''
    $baseName = "$baseStem$ext"
    $basePath = Join-Path $dataDir $baseName

    if (Test-Path -LiteralPath $basePath) {
        $hashA = (Get-FileHash -LiteralPath $file.FullName).Hash
        $hashB = (Get-FileHash -LiteralPath $basePath).Hash
        if ($hashA -eq $hashB) {
            Remove-Item -LiteralPath $file.FullName -Force
            $removed += $file.Name
        } else {
            $variantName = "${baseStem}__variant${suffixNum}${ext}"
            $targetPath = Join-Path $variantDir $variantName
            Move-Item -LiteralPath $file.FullName -Destination $targetPath
            $moved += "$($file.Name) -> _variants\\$variantName"
        }
    } else {
        $targetPath = Join-Path $dataDir $baseName
        if (Test-Path -LiteralPath $targetPath) {
            $variantName = "${baseStem}__variant${suffixNum}${ext}"
            $targetPath = Join-Path $variantDir $variantName
            Move-Item -LiteralPath $file.FullName -Destination $targetPath
            $moved += "$($file.Name) -> _variants\\$variantName"
        } else {
            Rename-Item -LiteralPath $file.FullName -NewName $baseName
            $renamed += "$($file.Name) -> $baseName"
        }
    }
}

$reportPath = Join-Path $metaDir "DEDUP_REPORT.md"
$lines = @()
$lines += "# Deduplication report"
$lines += ""
$lines += "Removed identical suffix copies: $($removed.Count)"
foreach ($item in $removed) { $lines += "- $item" }
$lines += ""
$lines += "Renamed (no base found): $($renamed.Count)"
foreach ($item in $renamed) { $lines += "- $item" }
$lines += ""
$lines += "Moved non-identical variants: $($moved.Count)"
foreach ($item in $moved) { $lines += "- $item" }

$lines | Set-Content -Path $reportPath -Encoding UTF8

Write-Host "Wrote $reportPath"
