$root = Split-Path -Parent $PSScriptRoot
$dataDir = Join-Path $root "data"
$aliasCsv = Join-Path $dataDir "_workbench\00_meta\ALIASES.csv"
$reportPath = Join-Path $dataDir "_workbench\00_meta\ALIASES_APPLIED.md"

if (-not (Test-Path $aliasCsv)) { throw "Missing $aliasCsv" }

$maps = Import-Csv -Path $aliasCsv

$extensions = @("*.md","*.ps1","*.py","*.txt","*.json")
$files = @()
foreach ($ext in $extensions) {
    $files += Get-ChildItem -Path $dataDir -Recurse -File -Filter $ext
    $files += Get-ChildItem -Path (Join-Path $root "scripts") -Recurse -File -Filter $ext
}
$files = $files | Sort-Object FullName -Unique

$changed = @()
foreach ($file in $files) {
    if ($file.FullName -like "*\\_workbench\\00_meta\\ALIASES.md") { continue }
    if ($file.FullName -like "*\\retrofit_aliases_for_reorg.ps1") { continue }
    $content = Get-Content -Path $file.FullName -Raw
    $updated = $content
    foreach ($map in $maps) {
        $oldForward = $map.old_path
        $newForward = $map.new_path
        $oldBack = $oldForward -replace '/', '\\'
        $newBack = $newForward -replace '/', '\\'
        $oldMnt = "/mnt/data/" + ($oldForward -replace '^data/', '')
        $newMnt = "/mnt/data/" + ($newForward -replace '^data/', '')
        $updated = $updated -replace [regex]::Escape($oldForward), $newForward
        $updated = $updated -replace [regex]::Escape($oldBack), $newBack
        $updated = $updated -replace [regex]::Escape($oldMnt), $newMnt
    }
    if ($updated -ne $content) {
        Set-Content -Path $file.FullName -Value $updated -Encoding UTF8
        $changed += $file.FullName
    }
}

$lines = @()
$lines += "# Alias application report"
$lines += ""
$lines += "- mappings: $($maps.Count)"
$lines += "- files_updated: $($changed.Count)"
$lines += ""
foreach ($path in $changed) {
    $lines += "- $($path.Replace($root + '\\',''))"
}
$lines | Set-Content -Path $reportPath -Encoding UTF8

Write-Host "Wrote $reportPath"
