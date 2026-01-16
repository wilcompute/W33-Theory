$ErrorActionPreference = "Stop"

$root = Split-Path -Parent $PSScriptRoot

$indexPath = Join-Path $root "data/_n12/n12_extended_analysis_json/n12_index.json"
$missingPath = Join-Path $root "data/_n12/n12_extended_analysis_json/n12_global_missing_triangle_orbit_summary.json"
$cupPath = Join-Path $root "data/_n12/n12_extended_analysis_json/n12_58_orbit_cup_analysis.json"
$packetPath = Join-Path $root "data/_n12/n12_58_packet_matching_phase_analysis.json"
$a4Path = Join-Path $root "data/_n12/n12_58_a4_sp12_representation.json"
$orientPath = Join-Path $root "data/_n12/n12_orientable_1_29_symplectic.json"
$clockPath = Join-Path $root "data/_n12/n12_58_a4_clock_phase_bundle.json"
$outMd = Join-Path $root "data/_workbench/05_symmetry/N12_extended_summary.md"

foreach ($p in @($indexPath,$missingPath,$cupPath,$packetPath,$a4Path,$orientPath,$clockPath)) {
    if (-not (Test-Path $p)) { throw "Missing $p" }
}

$index = Get-Content -Path $indexPath -Raw | ConvertFrom-Json
$missing = Get-Content -Path $missingPath -Raw | ConvertFrom-Json
$cup = Get-Content -Path $cupPath -Raw | ConvertFrom-Json
$packet = Get-Content -Path $packetPath -Raw | ConvertFrom-Json
$a4 = Get-Content -Path $a4Path -Raw | ConvertFrom-Json
$orient = Get-Content -Path $orientPath -Raw | ConvertFrom-Json
$clock = Get-Content -Path $clockPath -Raw | ConvertFrom-Json

# Index stats
$autOrders = $index | ForEach-Object { [int]$_.aut_order }
$autDist = $autOrders | Group-Object | Sort-Object Count -Descending | ForEach-Object { "$($_.Name):$($_.Count)" }
$dualGirth = $index | ForEach-Object { [int]$_.dual_girth }
$dualDiam = $index | ForEach-Object { [int]$_.dual_diameter }

# N12_58 missing orbit summary
$n12_58 = $missing | Where-Object { $_.id -eq 58 } | Select-Object -First 1

# Orbit cup analysis
$orbitSizes = $cup.missing_triangle_orbits | Group-Object size | Sort-Object Name | ForEach-Object { "$($_.Name):$($_.Count)" }
$h1Span = $cup.missing_triangle_orbits | Group-Object h1_span_dim | Sort-Object Name | ForEach-Object { "$($_.Name):$($_.Count)" }
$h1Unique = $cup.missing_triangle_orbits | Group-Object h1_unique_count | Sort-Object Name | ForEach-Object { "$($_.Name):$($_.Count)" }

# Packet matching analysis
$packetSummary = $packet.summary
$orbit0 = $packet.orbit0
$orbit13 = $packet.orbit13

function OrbitPacketSummary($orbit) {
    $hist = $orbit.phase_signature_histogram_mod8
    $histPairs = $hist.PSObject.Properties | ForEach-Object { "$($_.Name):$($_.Value)" }
    $matchPairs = $orbit.matchings_orbit_size_histogram_under_A4.PSObject.Properties | ForEach-Object { "$($_.Name):$($_.Value)" }
    $matchPairsStr = $matchPairs -join ", "
    $histPairsStr = $histPairs -join ", "
    return @(
        "- orbit_index: $($orbit.orbit_index)",
        "- orbit_size: $($orbit.orbit_size)",
        "- perfect_matchings: $($orbit.perfect_matchings.Count)",
        "- perfect_matchings_count_commute_mod2: $($orbit.perfect_matchings_count_commute_mod2)",
        "- matchings_orbit_size_histogram_under_A4: $matchPairsStr",
        "- phase_signature_histogram_mod8: $histPairsStr"
    )
}

# A4 symplectic summary
$a4Summary = $a4.representation_summary

# Clock bundle summary
$tau = $clock.clock_element_tau

$missingSizeCounts = ($n12_58.missing_triangle_orbit_size_counts.PSObject.Properties | ForEach-Object { "$($_.Name):$($_.Value)" }) -join ", "
$orderDist = ($a4Summary.order_distribution.PSObject.Properties | ForEach-Object { "$($_.Name):$($_.Value)" }) -join ", "
$orbit0Lines = OrbitPacketSummary $orbit0
$orbit13Lines = OrbitPacketSummary $orbit13

$lines = @(
    "# N12 extended summary (new imports)",
    "",
    "## N12 index (59 manifolds)",
    "- aut_order_dist: $($autDist -join ', ')",
    "- dual_girth_min: $([int]($dualGirth | Measure-Object -Minimum).Minimum)",
    "- dual_girth_max: $([int]($dualGirth | Measure-Object -Maximum).Maximum)",
    "- dual_diameter_min: $([int]($dualDiam | Measure-Object -Minimum).Minimum)",
    "- dual_diameter_max: $([int]($dualDiam | Measure-Object -Maximum).Maximum)",
    "",
    "## N12_58 missing triangle orbits",
    "- automorphism_group_order: $($n12_58.automorphism_group_order)",
    "- missing_triangles_count: $($n12_58.missing_triangles_count)",
    "- missing_triangle_orbit_count: $($n12_58.missing_triangle_orbit_count)",
    "- missing_triangle_orbit_size_counts: $missingSizeCounts",
    "",
    "## N12_58 orbit cup analysis",
    "- H1_dim_mod2: $($cup.cohomology.H1_dim_mod2)",
    "- missing_triangle_orbits_count: $($cup.missing_triangle_orbits.Count)",
    "- orbit_size_histogram: $($orbitSizes -join ', ')",
    "- h1_span_dim_histogram: $($h1Span -join ', ')",
    "- h1_unique_count_histogram: $($h1Unique -join ', ')",
    "",
    "## Packet matching phase analysis (orbits 0 and 13)",
    "- summary: $($packetSummary.note)",
    ""
)

$lines += "### Orbit 0"
$lines += $orbit0Lines
$lines += ""
$lines += "### Orbit 13"
$lines += $orbit13Lines
$lines += @(
    "",
    "## A4 Sp12 representation",
    "- group_isomorphic_to: $($a4Summary.group_isomorphic_to)",
    "- order_distribution: $orderDist",
    "- irrep_decomposition_over_C: $($a4Summary.irrep_decomposition_over_C)",
    "- involution_eigenvalue_counts: $($a4Summary.involution_eigenvalue_counts)",
    "",
    "## A4 clock phase bundle (N12_58)",
    "- tau_definition: $($tau.definition)",
    "- tau_order_verified: $($tau.order_verified)",
    "- Sp12_representation_elements: $($clock.Sp12_representation_elements.Count)",
    "- missing_triangle_orbits_size4: $($clock.missing_triangle_orbits_size4.Count)",
    "- intersection_rank6_graph_isolated_orbits: $($clock.intersection_rank6_graph_isolated_orbits.Count)",
    "",
    "## Orientable symplectic meta",
    "- $($orient.meta.description)"
)

$lines -join "`n" | Set-Content -Path $outMd -Encoding utf8
Write-Output "Wrote $outMd"
