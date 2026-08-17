"""Exact regression for the GAP-owned Passes 5667-5674 packet."""

from __future__ import annotations

import json
import os
import shutil
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "analysis" / "w33_pass5667_5674_q5_reye_equivariant_orientation.g"
FROZEN = ROOT / "data" / "PART_W33_PASS5667_5674_Q5_REYE_EQUIVARIANT_ORIENTATION.json"


def load_frozen() -> dict:
    return json.loads(FROZEN.read_text(encoding="utf-8"))


def test_frozen_q5_reye_orientation_contract() -> None:
    data = load_frozen()
    assert data["status"] == "PASS"
    assert data["all_pass"] is True
    assert data["check_count"] == data["checks_passed"] == 56
    assert all(data["checks"].values())

    gate = data["pass_5667_action_gate"]
    assert gate["transitive_id"] == 165
    assert gate["stabilizer_id"] == [48, 48]
    assert gate["subdegrees"] == [1, 3, 8]
    assert gate["cover_to_latin_conjugator_one_based"] == [
        1, 9, 4, 8, 12, 7, 10, 2, 5, 3, 6, 11
    ]

    design = data["pass_5668_design"]
    assert design["parameters"] == [13, 6, 60]
    assert design["rows_with_multiplicity"] == 312
    assert design["triple_containment_spectrum_value_count"] == [
        [0, 16], [16, 30], [24, 240]
    ]

    reye = data["pass_5669_reye_zero_shell"]
    assert reye["configuration"] == [12, 4, 16, 3]
    assert reye["levi_edges"] == 48
    assert reye["point_action_transitive_id"] == 165
    assert reye["line_action_transitive_id"] == 1034
    assert reye["line_action_subdegrees"] == [1, 6, 9]

    orientation = data["pass_5670_5671_orientation"]
    assert orientation["twelve_action_even"] is False
    assert orientation["sixteen_action_even"] is True
    assert orientation["twelve_sign_kernel_order"] == 288
    assert orientation["twelve_sign_kernel_id"] == [288, 1025]

    join = data["pass_5672_natural_PSL27_join"]
    assert join["number_of_S12_conjugates"] == 23_760
    assert join["relative_placement_orbit_counts"] == [53, 62, 58]
    assert join["join_order_sets"] == [[239_500_800], [239_500_800], [479_001_600]]
    assert join["all_joins_are_A12"] == [True, True, False]
    assert join["all_joins_are_S12"] == [False, False, True]

    heavy = data["pass_5673_5674_heavy_dual"]
    assert heavy["distinct_rows"] == 132
    assert heavy["row_multiplicity_value_count"] == [[2, 120], [6, 12]]
    assert heavy["heavy_action_transitive_id"] == 165
    assert heavy["stabilizers_conjugate_in_source_group"] is False
    assert heavy["permutation_images_conjugate_in_S12"] is True
    assert heavy["source_automorphism_witness_order"] == 8
    assert heavy["source_outer_coset_order"] == 2
    assert heavy["inner_regaugings_yielding_outer_involutions"] == 48
    assert heavy["outer_involution_order"] == 2
    assert heavy["outer_involution_maps_point_to_heavy_stabilizer_class"] is True

    firewall = data["sign_twist_module_firewall"]
    assert firewall["point_heavy_character_inner_product"] == 2
    assert firewall["point_line_character_inner_product"] == 2
    assert firewall["heavy_line_character_inner_product"] == 2
    assert firewall["sign_twisted_point_heavy_inner_product"] == 0
    assert firewall["sign_twisted_point_line_inner_product"] == 0


def test_native_gap_replay_is_byte_exact(tmp_path: Path) -> None:
    gap = shutil.which("gap")
    if gap is None:
        pytest.skip("GAP is not installed")

    env = os.environ.copy()
    user_bin = str(Path.home() / ".local" / "bin")
    user_lib = str(Path.home() / ".local" / "lib")
    env["PATH"] = user_bin + os.pathsep + env.get("PATH", "")
    env["LD_LIBRARY_PATH"] = user_lib + os.pathsep + env.get("LD_LIBRARY_PATH", "")
    probe = subprocess.run(
        [gap, "-q", "-c", 'if LoadPackage("grape")=fail then QUIT_GAP(1); fi; QUIT;'],
        cwd=ROOT,
        env=env,
        capture_output=True,
        text=True,
        timeout=30,
        check=False,
    )
    if probe.returncode != 0:
        pytest.skip("GAP package GRAPE is not installed")

    (tmp_path / "data").mkdir()
    env["W33_REPO"] = str(tmp_path)
    run = subprocess.run(
        [gap, "-q", str(SOURCE)],
        cwd=ROOT,
        env=env,
        capture_output=True,
        text=True,
        timeout=300,
        check=False,
    )
    assert run.returncode == 0, run.stdout + run.stderr
    assert "PASS5667-5674: 56/56 PASS" in run.stdout
    replay = tmp_path / "data" / FROZEN.name
    assert replay.read_bytes() == FROZEN.read_bytes()
