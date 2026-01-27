$ErrorActionPreference = "Stop"

$root = Split-Path -Parent $PSScriptRoot
$dataDir = Join-Path $root "data"
$metaDir = Join-Path $dataDir "_workbench\00_meta"
$aliasCsv = Join-Path $metaDir "ALIASES.csv"
$aliasMd = Join-Path $metaDir "ALIASES.md"

function To-SnakeCase([string]$name) {
    $lower = $name.ToLowerInvariant()
    $snake = [regex]::Replace($lower, "[^a-z0-9]+", "_")
    $snake = [regex]::Replace($snake, "_+", "_")
    return $snake.Trim('_')
}

function Ensure-Dir([string]$path) {
    New-Item -ItemType Directory -Force -Path $path | Out-Null
}

function To-DataRel([string]$path) {
    $prefix = $dataDir + "\"
    $rel = $path
    if ($rel.StartsWith($prefix, [System.StringComparison]::OrdinalIgnoreCase)) {
        $rel = "data\" + $rel.Substring($prefix.Length)
    }
    return $rel -replace "\\", "/"
}

function Get-UniqueDirPath([string]$dir, [string]$name) {
    $candidate = Join-Path $dir $name
    if (-not (Test-Path -LiteralPath $candidate)) {
        return $candidate
    }
    $i = 2
    do {
        $candidate = Join-Path $dir ("{0}_v{1}" -f $name, $i)
        $i++
    } while (Test-Path -LiteralPath $candidate)
    return $candidate
}

function Get-UniqueFilePath([string]$dir, [string]$name, [string]$ext) {
    $candidate = Join-Path $dir ("{0}{1}" -f $name, $ext)
    if (-not (Test-Path -LiteralPath $candidate)) {
        return $candidate
    }
    $i = 2
    do {
        $candidate = Join-Path $dir ("{0}_v{1}{2}" -f $name, $i, $ext)
        $i++
    } while (Test-Path -LiteralPath $candidate)
    return $candidate
}

$newMappings = @()
$dirMoves = 0
$fileMoves = 0

function Add-Mapping([string]$oldRel, [string]$newRel) {
    if ([string]::IsNullOrWhiteSpace($oldRel) -or [string]::IsNullOrWhiteSpace($newRel)) { return }
    $newMappings += [pscustomobject]@{
        old_path = $oldRel
        new_path = $newRel
        action = "move_rename"
    }
}

function Move-Dir([System.IO.DirectoryInfo]$dir, [string]$destDir, [string]$newBase) {
    Ensure-Dir $destDir
    $base = To-SnakeCase $newBase
    if ([string]::IsNullOrWhiteSpace($base)) { $base = "dir" }
    $destPath = Get-UniqueDirPath $destDir $base
    $oldRel = To-DataRel $dir.FullName
    Move-Item -LiteralPath $dir.FullName -Destination $destPath
    $newRel = To-DataRel $destPath
    Add-Mapping $oldRel $newRel
    $script:dirMoves++
}

function Move-File([System.IO.FileInfo]$file, [string]$destDir, [string]$newBase) {
    Ensure-Dir $destDir
    $base = To-SnakeCase $newBase
    if ([string]::IsNullOrWhiteSpace($base)) { $base = "file" }
    $ext = $file.Extension.ToLowerInvariant()
    $destPath = Get-UniqueFilePath $destDir $base $ext
    $oldRel = To-DataRel $file.FullName
    Move-Item -LiteralPath $file.FullName -Destination $destPath
    $newRel = To-DataRel $destPath
    Add-Mapping $oldRel $newRel
    $script:fileMoves++
}

Ensure-Dir $metaDir

# Move root directories into grouped folders
$rootDirs = Get-ChildItem -Path $dataDir -Directory
foreach ($dir in $rootDirs) {
    if ($dir.Name -eq ".git") { continue }
    if ($dir.Name.StartsWith("_")) { continue }

    if ($dir.Name -match '^(?i)toe_bundle$') {
        Move-Dir $dir (Join-Path $dataDir "_archives\extracted") "toe_bundle"
        continue
    }
    if ($dir.Name -match '^(?i)toe_') {
        $base = $dir.Name -replace '^(?i)toe_', ''
        Move-Dir $dir (Join-Path $dataDir "_toe") $base
        continue
    }
    if ($dir.Name -match '^(?i)is_pg32_') {
        $base = $dir.Name -replace '^(?i)is_pg32_', ''
        Move-Dir $dir (Join-Path $dataDir "_pg32") $base
        continue
    }
    if ($dir.Name -match '^(?i)pg32_') {
        $base = $dir.Name -replace '^(?i)pg32_', ''
        Move-Dir $dir (Join-Path $dataDir "_pg32") $base
        continue
    }
    if ($dir.Name -match '^(?i)is_') {
        $base = $dir.Name -replace '^(?i)is_', ''
        Move-Dir $dir (Join-Path $dataDir "_is") $base
        continue
    }
    if ($dir.Name -match '^(?i)user-') {
        $base = $dir.Name -replace '^(?i)user-', 'user_'
        Move-Dir $dir (Join-Path $dataDir "_user") $base
        continue
    }
}

# Move root files into grouped folders
$rootFiles = Get-ChildItem -Path $dataDir -File
foreach ($file in $rootFiles) {
    if ($file.Name -ieq ".gitignore") { continue }
    if ($file.Name -ieq "README.md") { continue }
    if ($file.Name -ieq "prepare_push.bat") { continue }

    if ($file.Name -match '^(?i)checkpoint_.*\.json$') {
        Move-File $file (Join-Path $dataDir "_checkpoints") $file.BaseName
        continue
    }
    if ($file.Name -match '^(?i)embedding_.*\.csv$') {
        Move-File $file (Join-Path $dataDir "_embeddings") $file.BaseName
        continue
    }
    if ($file.Name -match '^(?i)tomotope_.*\.csv$') {
        Move-File $file (Join-Path $dataDir "_tomotope") $file.BaseName
        continue
    }
    if ($file.Name -match '^(?i)24cell_') {
        Move-File $file (Join-Path $dataDir "_algebra") $file.BaseName
        continue
    }
    if ($file.Name -match '^(?i)a4_') {
        Move-File $file (Join-Path $dataDir "_algebra") $file.BaseName
        continue
    }
    if ($file.Name -match '^(?i)binary_tetrahedral_') {
        Move-File $file (Join-Path $dataDir "_algebra") $file.BaseName
        continue
    }
    if ($file.Name -match '^(?i)toe_.*\.md$') {
        Move-File $file (Join-Path $dataDir "_docs") $file.BaseName
        continue
    }
    if ($file.Name -match '^(?i).*_bundle\.zip$') {
        $lower = $file.BaseName.ToLowerInvariant()
        $bucket = "misc"
        if ($lower -like "toe_*" -or $lower -eq "toe_bundle") { $bucket = "toe" }
        elseif ($lower -like "is_*") { $bucket = "is" }
        elseif ($lower -like "pg32_*") { $bucket = "pg32" }
        $dest = Join-Path $dataDir ("_archives\bundles\{0}" -f $bucket)
        Move-File $file $dest $file.BaseName
        continue
    }
}

# Merge mappings with existing alias file
$existing = @()
if (Test-Path $aliasCsv) {
    $existing = Import-Csv -Path $aliasCsv
}

$combined = @{}
foreach ($m in $existing) {
    $combined[$m.old_path] = $m
}
foreach ($m in $newMappings) {
    $combined[$m.old_path] = $m
}

$final = $combined.Values | Sort-Object old_path
$final | Export-Csv -NoTypeInformation -Path $aliasCsv

$lines = @()
$lines += "# Alias index"
$lines += ""
$lines += "This maps old paths to new paths after grouping + snake_case normalization."
$lines += ""
$lines += "- total mappings: $($final.Count)"
$lines += "- output csv: data/_workbench/00_meta/ALIASES.csv"
$lines += ""
foreach ($map in $final) {
    $lines += "- $($map.old_path) -> $($map.new_path)"
}
$lines | Set-Content -Path $aliasMd -Encoding UTF8

Write-Host "Moved directories: $dirMoves"
Write-Host "Moved files: $fileMoves"
Write-Host "Wrote $aliasCsv"
Write-Host "Wrote $aliasMd"
