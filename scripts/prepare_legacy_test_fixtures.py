from __future__ import annotations

import shutil
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

LEGACY_FIXTURE_MAP = {
    Path("H27_OUTER_TWIST_ACTION_BUNDLE_v01"): Path(
        "archive/dirs/H27_OUTER_TWIST_ACTION_BUNDLE_v01"
    ),
    Path("H27_CE2_FUSION_BRIDGE_BUNDLE_v01"): Path(
        "archive/dirs/H27_CE2_FUSION_BRIDGE_BUNDLE_v01"
    ),
    Path("PG33_OUTER_TWIST_GEOMETRY_BUNDLE_v01"): Path(
        "archive/dirs/PG33_OUTER_TWIST_GEOMETRY_BUNDLE_v01"
    ),
    Path("WE6_EVEN_to_PSp43_CONJUGACY_BUNDLE_v01 (1)"): Path(
        "archive/dirs/WE6_EVEN_to_PSp43_CONJUGACY_BUNDLE_v01 (1)"
    ),
    Path("SP43_TO_WE6_TRUE_FIXED_BUNDLE_v01_2026-02-25"): Path(
        "archive/dirs/SP43_TO_WE6_TRUE_FIXED_BUNDLE_v01_2026-02-25"
    ),
    Path("TOE_E6pair_SRG_triangle_decomp_v01_20260227_bundle"): Path(
        "archive/dirs/TOE_E6pair_SRG_triangle_decomp_v01_20260227_bundle"
    ),
    Path("TOE_holonomy_Z2_flatZ3_v01_20260227_bundle"): Path(
        "archive/dirs/TOE_holonomy_Z2_flatZ3_v01_20260227_bundle"
    ),
    Path("TOE_7pocket_derivations_v01_20260227_bundle"): Path(
        "archive/dirs/TOE_7pocket_derivations_v01_20260227_bundle"
    ),
    Path("TOE_push_triangle_scheme_cohomology_v01_20260227_bundle"): Path(
        "archive/dirs/TOE_push_triangle_scheme_cohomology_v01_20260227_bundle"
    ),
    Path("TOE_pocket_transport_glue_orbit480_v01_20260227_bundle"): Path(
        "archive/dirs/TOE_pocket_transport_glue_orbit480_v01_20260227_bundle"
    ),
    Path("TOE_duad_algebra_v06_20260227_bundle"): Path(
        "archive/dirs/TOE_duad_algebra_v06_20260227_bundle"
    ),
    Path("TOE_duad_algebra_v06_20260227_bundle.zip"): Path(
        "archive/zip/TOE_duad_algebra_v06_20260227_bundle.zip"
    ),
    Path("pillars/TOE_27x10_quotient_v01_20260228_bundle.zip"): Path(
        "archive/zip/TOE_27x10_quotient_v01_20260228_bundle.zip"
    ),
    Path("pillars/TOE_270_TRANSPORT_v01_20260228_bundle.zip"): Path(
        "archive/zip/TOE_270_TRANSPORT_v01_20260228_bundle.zip"
    ),
    Path("pillars/TOE_BoseMesner_Algebra_Solution_bundle_v04_20260227.zip"): Path(
        "archive/zip/TOE_BoseMesner_Algebra_Solution_bundle_v04_20260227.zip"
    ),
    Path("pillars/TOE_S3_SHEET_TRANSPORT_v01_20260228_bundle.zip"): Path(
        "archive/zip/TOE_S3_SHEET_TRANSPORT_v01_20260228_bundle.zip"
    ),
    Path("pillars/TOE_tomotope_true_flag_model_v02_20260228_bundle.zip"): Path(
        "archive/zip/TOE_tomotope_true_flag_model_v02_20260228_bundle.zip"
    ),
    Path("TOE_54sheet_pillar82_bundle.zip"): Path(
        "archive/zip/TOE_54sheet_pillar82_bundle.zip"
    ),
    Path("TOE_E6pair_SRG_triangle_decomp_v01_20260227_bundle.zip"): Path(
        "archive/zip/TOE_E6pair_SRG_triangle_decomp_v01_20260227_bundle.zip"
    ),
    Path("analysis/outer_twist_cocycle"): Path("archive/dirs/analysis/outer_twist_cocycle"),
    Path("analysis/w33_bundle_temp"): Path("archive/dirs/analysis/w33_bundle_temp"),
    Path("action_conjugacy_obstruction.json"): Path(
        "archive/json/action_conjugacy_obstruction.json"
    ),
    Path("270_transport_table.json"): Path("archive/json/270_transport_table.json"),
    Path("block_to_pockets.json"): Path("archive/json/block_to_pockets.json"),
    Path("edges_270_transport.csv"): Path("archive/data/edges_270_transport.csv"),
    Path("edgepair_to_pockets.json"): Path("archive/json/edgepair_to_pockets.json"),
    Path("flag_word_map.json"): Path("archive/json/flag_word_map.json"),
    Path("K54_54sheet_coords.csv"): Path("archive/data/K54_54sheet_coords.csv"),
    Path("K54_54sheet_coords_refined.csv"): Path(
        "archive/data/K54_54sheet_coords_refined.csv"
    ),
    Path("K54_node_labels_L.csv"): Path("archive/data/K54_node_labels_L.csv"),
    Path("K54_edges_L_reconstruct.csv"): Path("archive/data/K54_edges_L_reconstruct.csv"),
    Path("K27_stabilizer_C6.json"): Path("archive/json/K27_stabilizer_C6.json"),
    Path("tomo_t4_cycle_structure.json"): Path("archive/json/tomo_t4_cycle_structure.json"),
    Path("pillars/N_subgroup.json"): Path("archive/json/N_subgroup.json"),
    Path("axis_bundle_content"): Path("archive/dirs/axis_bundle_content"),
    Path("pillar77_data"): Path("archive/dirs/pillar77_data"),
    Path("neighbor_map.json"): Path("archive/json/neighbor_map.json"),
    Path("orbit_480_summary.json"): Path("archive/json/orbit_480_summary.json"),
    Path("orbits_outer.json"): Path("archive/json/orbits_outer.json"),
    Path("orbits_P.json"): Path("archive/json/orbits_P.json"),
    Path("orbits_NP.json"): Path("archive/json/orbits_NP.json"),
    Path("pocket_geometry.json"): Path("archive/json/pocket_geometry.json"),
    Path("pocket_glue_summary.json"): Path("archive/json/pocket_glue_summary.json"),
    Path("pocket_to_flags.json"): Path("archive/json/pocket_to_flags.json"),
    Path("pocket_to_unique_flag.json"): Path("archive/json/pocket_to_unique_flag.json"),
    Path("pg_to_edge_labeling.json"): Path("archive/json/pg_to_edge_labeling.json"),
    Path("pg_to_internal_inf.json"): Path("archive/json/pg_to_internal_inf.json"),
    Path("SUMMARY_54sheet.json"): Path("archive/json/SUMMARY_54sheet.json"),
    Path("SUMMARY_matching.json"): Path("archive/json/SUMMARY_matching.json"),
    Path("W33_adjacency_matrix.txt"): Path("archive/data/W33_adjacency_matrix.txt"),
    Path("PILLAR_89.md"): Path("archive/misc/PILLAR_89.md"),
}


def _build_edge_orient_bundle(target: Path) -> None:
    source = ROOT / "archive/json/edge_orient_map_real.json"
    if not source.exists():
        return
    target.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(target, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.write(
            source,
            "TOE_edge_orient_map_v01_20260227/edge_orient_map_real.json",
        )


def _build_tomotope_axis_bundle(target: Path) -> None:
    """Create the pillars ZIP bundle from the axis_bundle_content directory if present."""
    source_dir = ROOT / "axis_bundle_content" / "TOE_tomotope_axis_block_twist_v02_20260228"
    if not source_dir.exists():
        return
    target.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(target, "w", zipfile.ZIP_DEFLATED) as zf:
        for p in sorted(source_dir.rglob("*")):
            if p.is_file():
                arcname = Path("TOE_tomotope_axis_block_twist_v02_20260228") / p.relative_to(source_dir)
                zf.write(p, str(arcname))


def _build_line_polarization_bundle(target: Path) -> None:
    """Extract the TOE_line_polarization zip into the expected bundle directory."""
    source_zip = ROOT / "archive" / "zip" / "TOE_line_polarization_A5_v01_20260227_bundle.zip"
    if not source_zip.exists():
        return
    target.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(source_zip, "r") as zf:
        # Extract all files into the target directory. If the zip contains a
        # top-level folder like 'TOE_line_polarization_A5_v01_20260227', this
        # will produce the expected nested structure under target.
        zf.extractall(target)


SPECIAL_BUILDERS = {
    Path("TOE_edge_orient_map_v01_20260227_bundle.zip"): _build_edge_orient_bundle,
    Path("pillars/TOE_tomotope_axis_block_twist_v02_20260228_bundle.zip"): _build_tomotope_axis_bundle,
    Path("TOE_line_polarization_A5_v01_20260227_bundle"): _build_line_polarization_bundle,
}


def _copy_path(source: Path, target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    if source.is_dir():
        shutil.copytree(source, target, dirs_exist_ok=True)
    else:
        shutil.copy2(source, target)


def ensure_legacy_test_fixtures() -> list[Path]:
    materialized: list[Path] = []
    for target_rel, builder in SPECIAL_BUILDERS.items():
        target = ROOT / target_rel
        existed = target.exists()
        builder(target)
        if target.exists() and not existed:
            materialized.append(target)
    for target_rel, source_rel in LEGACY_FIXTURE_MAP.items():
        target = ROOT / target_rel
        source = ROOT / source_rel
        if target.exists():
            continue
        if not source.exists():
            continue
        _copy_path(source, target)
        materialized.append(target)
    return materialized


def main() -> None:
    created = ensure_legacy_test_fixtures()
    if created:
        print("Materialized legacy fixtures:")
        for path in created:
            print(path.relative_to(ROOT))
    else:
        print("Legacy fixtures already present")


if __name__ == "__main__":
    main()
