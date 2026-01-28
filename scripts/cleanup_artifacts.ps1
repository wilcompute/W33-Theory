param([switch]$delete)

$archive = "artifacts_archive"
if (-not (Test-Path $archive)) { New-Item -Path $archive -ItemType Directory | Out-Null }

$items = @('artifacts', 'sage-part-jsons*', 'SUMMARY_RESULTS.json', 'NUMERIC_COMPARISONS.json')
foreach ($it in $items) {
    $matches = Get-ChildItem -Path . -Include $it -Recurse -Force -ErrorAction SilentlyContinue
    foreach ($m in $matches) {
        $dest = Join-Path $archive $m.Name
        if ($delete.IsPresent) { Remove-Item -Path $m.FullName -Recurse -Force -ErrorAction SilentlyContinue; Write-Output "Deleted: $($m.FullName)" }
        else { Move-Item -Path $m.FullName -Destination $archive -Force -ErrorAction SilentlyContinue; Write-Output "Moved: $($m.FullName) -> $archive" }
    }
}
Write-Output "Cleanup complete."