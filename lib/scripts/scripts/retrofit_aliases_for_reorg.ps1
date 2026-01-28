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

function Normalize-PathToken([string]$token) {
    $t = $token.Trim()
    $t = $t.TrimEnd(')', ',', '.', ':', ';', '"')
    return $t
}

function Map-DirPath([string]$norm, [string]$prefixPattern, [string]$newParent) {
    $rel = $norm.Substring(5) # after data/
    $parts = $rel -split '/', 2
    if ($parts.Count -eq 0) { return $null }
    $first = $parts[0]
    if ($first -notmatch $prefixPattern) { return $null }
    $base = $first -replace $prefixPattern, ''
    $newFirst = To-SnakeCase $base
    if ([string]::IsNullOrWhiteSpace($newFirst)) { return $null }
    $newPath = "data/{0}/{1}" -f $newParent, $newFirst
    if ($parts.Count -gt 1) {
        $newPath = $newPath + "/" + $parts[1]
    }
    return $newPath
}

function Map-RootFile([string]$norm, [string]$prefix, [string]$newParent) {
    $rel = $norm.Substring(5)
    if ($rel -notmatch "^[^/]+$") { return $null }
    if ($rel -notmatch $prefix) { return $null }
    $base = [System.IO.Path]::GetFileNameWithoutExtension($rel)
    $ext = [System.IO.Path]::GetExtension($rel).ToLowerInvariant()
    $newBase = To-SnakeCase $base
    if ([string]::IsNullOrWhiteSpace($newBase)) { return $null }
    return "data/{0}/{1}{2}" -f $newParent, $newBase, $ext
}

New-Item -ItemType Directory -Force -Path $metaDir | Out-Null

$extensions = @("*.md","*.ps1","*.py","*.txt","*.json")
$files = @()
foreach ($ext in $extensions) {
    $files += Get-ChildItem -Path $dataDir -Recurse -File -Filter $ext
    $files += Get-ChildItem -Path (Join-Path $root "scripts") -Recurse -File -Filter $ext
}
$files = $files | Sort-Object FullName -Unique | Where-Object {
    $_.FullName -notlike "*\\_workbench\\00_meta\\ALIASES*" -and
    $_.FullName -notlike "*\\retrofit_aliases_for_reorg.ps1"
}

# collect path-like tokens from files
$paths = New-Object System.Collections.Generic.HashSet[string]
foreach ($file in $files) {
    $content = Get-Content -Path $file.FullName -Raw
    foreach ($m in [regex]::Matches($content, 'data[\\/][A-Za-z0-9_\-\.\\/]+')) {
        $raw = Normalize-PathToken $m.Value
        if ([string]::IsNullOrWhiteSpace($raw)) { continue }
        $paths.Add($raw) | Out-Null
    }
}

$mapped = @{}
foreach ($raw in $paths) {
    $norm = $raw -replace '\\', '/'
    if (-not $norm.StartsWith("data/", [System.StringComparison]::OrdinalIgnoreCase)) { continue }
    if ($norm -like "data/_*") { continue }

    $newPath = $null

    if ($norm -match '^(?i)data/TOE_bundle\.zip$') {
        $newPath = "data/_archives/bundles/toe/toe_bundle.zip"
    } elseif ($norm -match '^(?i)data/TOE_bundle($|/)') {
        $suffix = $norm.Substring(15) # length of data/TOE_bundle
        $suffix = $suffix.TrimStart('/')
        $newPath = "data/_archives/extracted/toe_bundle"
        if ($suffix) { $newPath = $newPath + "/" + $suffix }
    } elseif ($norm -match '^(?i)data/TOE_[^/]+\.md$') {
        $newPath = Map-RootFile $norm '^TOE_' '_docs'
    } elseif ($norm -match '^(?i)data/.*_bundle\.zip$') {
        $base = [System.IO.Path]::GetFileNameWithoutExtension($norm)
        $base = ($base -split '/')[ -1 ]
        $stem = $base -replace '_bundle$', ''
        $stemNorm = To-SnakeCase $stem
        $bucket = "misc"
        if ($stemNorm -like "toe_*") { $bucket = "toe" }
        elseif ($stemNorm -like "is_*") { $bucket = "is" }
        elseif ($stemNorm -like "pg32_*") { $bucket = "pg32" }
        $newPath = "data/_archives/bundles/{0}/{1}_bundle.zip" -f $bucket, $stemNorm
    } elseif ($norm -match '^(?i)data/toe_') {
        $newPath = Map-DirPath $norm '^(?i)toe_' '_toe'
    } elseif ($norm -match '^(?i)data/is_pg32_') {
        $newPath = Map-DirPath $norm '^(?i)is_pg32_' '_pg32'
    } elseif ($norm -match '^(?i)data/pg32_') {
        $newPath = Map-DirPath $norm '^(?i)pg32_' '_pg32'
    } elseif ($norm -match '^(?i)data/is_') {
        $newPath = Map-DirPath $norm '^(?i)is_' '_is'
    } elseif ($norm -match '^(?i)data/checkpoint_.*\.json$') {
        $newPath = Map-RootFile $norm '^checkpoint_' '_checkpoints'
    } elseif ($norm -match '^(?i)data/embedding_.*\.csv$') {
        $newPath = Map-RootFile $norm '^embedding_' '_embeddings'
    } elseif ($norm -match '^(?i)data/tomotope_.*\.csv$') {
        $newPath = Map-RootFile $norm '^tomotope_' '_tomotope'
    } elseif ($norm -match '^(?i)data/_algebra/24cell.*') {
        $newPath = Map-RootFile $norm '^24cell_' '_algebra'
    } elseif ($norm -match '^(?i)data/_algebra/a4.*') {
        $newPath = Map-RootFile $norm '^A4_' '_algebra'
    } elseif ($norm -match '^(?i)data/_algebra/binary_tetrahedral.*') {
        $newPath = Map-RootFile $norm '^binary_tetrahedral_' '_algebra'
    }

    if ($null -eq $newPath) { continue }
    if ($newPath -eq $norm) { continue }

    $mapped[$norm] = $newPath
}

$existing = @()
if (Test-Path $aliasCsv) {
    $existing = Import-Csv -Path $aliasCsv | Where-Object {
        $_.old_path -notmatch '^(?i)data/TOE_bundle'
    }
}

$combined = @{}
foreach ($m in $existing) {
    $combined[$m.old_path] = $m
}
foreach ($kv in $mapped.GetEnumerator()) {
    $combined[$kv.Key] = [pscustomobject]@{
        old_path = $kv.Key
        new_path = $kv.Value
        action = "auto_map"
    }
}

$final = $combined.Values | Where-Object {
    $_.old_path -notmatch '^(?i)data/TOE_bundle'
} | Sort-Object old_path
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

Write-Host "Mapped paths: $($mapped.Count)"
Write-Host "Wrote $aliasCsv"
Write-Host "Wrote $aliasMd"
