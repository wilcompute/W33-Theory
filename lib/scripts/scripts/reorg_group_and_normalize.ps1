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

New-Item -ItemType Directory -Force -Path $metaDir | Out-Null

$targets = @(
    @{ pattern = '^(?i)n12'; folder = '_n12' },
    @{ pattern = '^(?i)w33'; folder = '_w33' },
    @{ pattern = '^(?i)witting'; folder = '_witting' }
)

$mappings = @()

$rootFiles = Get-ChildItem -Path $dataDir -File
foreach ($file in $rootFiles) {
    $target = $null
    foreach ($entry in $targets) {
        if ($file.Name -match $entry.pattern) {
            $target = $entry
            break
        }
    }
    if ($null -eq $target) { continue }

    $destDir = Join-Path $dataDir $target.folder
    New-Item -ItemType Directory -Force -Path $destDir | Out-Null

    $base = $file.BaseName
    $ext = $file.Extension.ToLowerInvariant()
    $newBase = To-SnakeCase $base
    if ([string]::IsNullOrWhiteSpace($newBase)) {
        $newBase = "file"
    }
    $newName = "$newBase$ext"
    $destPath = Join-Path $destDir $newName

    if (Test-Path -LiteralPath $destPath) {
        $i = 2
        do {
            $candidate = Join-Path $destDir ("{0}_v{1}{2}" -f $newBase, $i, $ext)
            $i++
        } while (Test-Path -LiteralPath $candidate)
        $destPath = $candidate
        $newName = Split-Path -Leaf $destPath
    }

    Move-Item -LiteralPath $file.FullName -Destination $destPath

    $mappings += [pscustomobject]@{
        old_path = ("data/{0}" -f $file.Name)
        new_path = ("data/{0}/{1}" -f $target.folder, $newName)
        action = "move_rename"
    }
}

$mappings | Sort-Object old_path | Export-Csv -NoTypeInformation -Path $aliasCsv

$lines = @()
$lines += "# Alias index"
$lines += ""
$lines += "This maps old paths to new paths after grouping + snake_case normalization."
$lines += ""
$lines += "- total mappings: $($mappings.Count)"
$lines += "- output csv: data/_workbench/00_meta/ALIASES.csv"
$lines += ""
foreach ($map in ($mappings | Sort-Object old_path)) {
    $lines += "- $($map.old_path) -> $($map.new_path)"
}
$lines | Set-Content -Path $aliasMd -Encoding UTF8

Write-Host "Wrote $aliasCsv"
Write-Host "Wrote $aliasMd"
