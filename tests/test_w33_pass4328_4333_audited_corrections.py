"""Focused native-GAP regression for Passes 4328--4333."""

from __future__ import annotations

import json
from pathlib import Path
import shutil
import subprocess


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "analysis" / "w33_pass4328_4333_audited_corrections.g"
FROZEN = ROOT / "data" / "PART_W33_PASS4328_4333_AUDITED_CORRECTIONS.json"
PASS_LINE = "Passes 4328--4333 audited corrections: 28/28 checks; status=PASS"

EXPECTED_CHECKS = {
    "affine_translation_not_projectively_well_defined",
    "corrected_universal_size_census_sums_360",
    "degree_33",
    "degree_33_irreducible_over_Q",
    "differential_comparator_census",
    "falsifier_cycle_is_simple_base_cycle",
    "falsifier_edge_indices",
    "falsifier_signed_voltages",
    "falsifier_unsigned_voltages",
    "falsifier_voltage_zero_mod_2731",
    "geometry_40_40_160",
    "kotani_sunada_square_root_translation",
    "machine_A_stir_counts",
    "machine_B_graph_swap_invariant",
    "machine_B_stir_counts",
    "machine_C_stir_counts",
    "machine_D_graph_swap_invariant",
    "machine_D_stir_counts",
    "machine_opcode_counts",
    "machine_swap_invariance_false_true_false_true",
    "one_rail_comparator_census",
    "shared_control_comparator_boundary",
    "swap_conjugates_cx_pair",
    "swap_conjugates_fp_ff",
    "swap_conjugates_load_pair",
    "unique_growth_root_in_interval",
    "unique_slow_root_in_interval",
    "voltage_tree_cotree_79_81",
}


def _assert_exact_payload(payload: dict[str, object]) -> None:
    assert payload["schema"] == "w33.pass4328_4333.audited_corrections.v1"
    assert payload["status"] == "PASS"
    assert payload["checks"] == {name: True for name in EXPECTED_CHECKS}

    ihara = payload["pass_4328_ihara_correction"]
    assert ihara["shipped_graph_u_annulus"] == "1/sqrt(7) <= |u| <= 1"
    assert ihara["reciprocal_lambda_annulus"].startswith(
        "1 <= |lambda| <= sqrt(7)"
    )
    assert "withdrawn" in ihara

    cover = payload["pass_4329_voltage_cover_retraction"]
    assert cover["base_cycle_zero_based"] == [3, 52, 4, 48, 8, 66, 18, 53]
    assert cover["signed_voltages"] == [0, 0, 0, 0, 1328, -542, 801, -1587]
    assert cover["voltage_sum_mod_2731"] == 0
    assert cover["corrected_cover_girth"] == 8
    assert "does not certify girth >=16" in cover["retraction"]

    symmetry = payload["pass_4330_point_frequency_symmetry"]
    assert symmetry["machine_swap_invariance_A_B_C_D"] == [False, True, False, True]
    assert symmetry["machine_A_stir"] == ["1", "8/9", "2/3", "2/3"]
    assert symmetry["machine_D_stir"] == ["1", "26/27", "1", "26/27"]
    assert "descends to neither" in symmetry["load_port_boundary"]
    assert symmetry["hardware_boundary"].endswith("did not synthesize B or D in Yosys.")

    comparator = payload["pass_4331_incidence_comparator"]
    assert comparator["differential_single_rail_detected"] == 1656
    assert comparator["differential_single_rail_trials"] == 1920
    assert comparator["differential_detection_fraction"] == "69/80"
    assert comparator["shared_control_detected"] == 0
    assert comparator["shared_control_trials"] == 960

    conjugates = payload["pass_4332_degree33_galois_pair"]
    assert conjugates["degree"] == 33
    assert conjugates["irreducible_over_Q"] is True
    assert conjugates["growth_root_isolating_interval"] == ["574/100", "575/100"]
    assert conjugates["slow_root_isolating_interval"] == ["3349/1000", "3350/1000"]
    assert conjugates["roots_in_each_interval"] == [1, 1]

    census = payload["pass_4333_universal_census_correction"]
    assert census["sizes_4_through_10"] == [24, 80, 114, 90, 41, 10, 1]
    assert census["total"] == 360
    assert "positions 7 through 12" in census["shipped_rho_rank"]


def test_native_gap_rebuild_matches_frozen_certificate(tmp_path: Path) -> None:
    gap = shutil.which("gap")
    assert gap is not None, "native GAP is required for Passes 4328--4333"

    completed = subprocess.run(
        [gap, "-q", str(SOURCE)],
        cwd=tmp_path,
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=300,
    )
    assert completed.returncode == 0, completed.stdout[-6000:]
    assert PASS_LINE in completed.stdout.splitlines(), completed.stdout[-6000:]
    assert "Syntax warning" not in completed.stdout

    rebuilt = tmp_path / "data" / "PART_W33_PASS4328_4333_AUDITED_CORRECTIONS.json"
    rebuilt_bytes = rebuilt.read_bytes()
    assert rebuilt_bytes == FROZEN.read_bytes()
    _assert_exact_payload(json.loads(rebuilt_bytes))
