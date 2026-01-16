$ErrorActionPreference = "Stop"

$root = Split-Path -Parent $PSScriptRoot
$timestamp = (Get-Date).ToUniversalTime().ToString("yyyyMMddTHHmmssZ")

$runs = @(
    @{
        script = "scripts/w33_line_phase_map.ps1"
        outputs = @(
            "data/_workbench/02_geometry/W33_line_phase_map.csv",
            "data/_workbench/02_geometry/W33_line_phase_map.md"
        )
    },
    @{
        script = "scripts/w33_line_phase_flux_join.ps1"
        outputs = @(
            "data/_workbench/02_geometry/W33_line_phase_flux_join.csv",
            "data/_workbench/02_geometry/W33_line_phase_flux_join.md"
        )
    },
    @{
        script = "scripts/line_feature_table.ps1"
        outputs = @(
            "data/_workbench/02_geometry/line_feature_table.csv",
            "data/_workbench/02_geometry/line_feature_table_summary.md"
        )
    },
    @{
        script = "scripts/native_c24_fullgrid_summary.ps1"
        outputs = @(
            "data/_workbench/04_measurement/native_C24_fullgrid_summary.md"
        )
    },
    @{
        script = "scripts/native_vs_reduced_alignment.ps1"
        outputs = @(
            "data/_workbench/04_measurement/native_vs_reduced_alignment.md"
        )
    },
    @{
        script = "scripts/native_c24_winner_signature.ps1"
        outputs = @(
            "data/_workbench/04_measurement/native_C24_winner_signature.md"
        )
    }
)

$results = @()
foreach ($entry in $runs) {
    $scriptPath = Join-Path $root $entry.script
    if (-not (Test-Path $scriptPath)) { throw "Missing $scriptPath" }

    & $scriptPath

    $outputs = @()
    foreach ($out in $entry.outputs) {
        $full = Join-Path $root $out
        $outputs += [pscustomobject]@{
            path = $out
            exists = (Test-Path $full)
        }
    }

    $results += [pscustomobject]@{
        script = $entry.script
        outputs = $outputs
    }
}

$checkpoint = [ordered]@{
    timestamp_utc = $timestamp
    purpose = "Analysis refresh after data reorg"
    scripts_run = ($runs | ForEach-Object { $_.script })
    outputs = $results
    notes = "Generated from reorganized _toe workspace."
}

$checkpointPath = Join-Path $root ("data/_checkpoints/checkpoint_toe_analysis_run_{0}.json" -f $timestamp)
$checkpoint | ConvertTo-Json -Depth 6 | Set-Content -Path $checkpointPath -Encoding utf8
Write-Output "Wrote $checkpointPath"

& (Join-Path $root "scripts/toe_checkpoint_digest.ps1")
