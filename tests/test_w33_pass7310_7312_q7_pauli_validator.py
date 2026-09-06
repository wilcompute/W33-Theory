"""Focused replay tests for the Pass 7310--7312 q=7 validator packet."""

from __future__ import annotations

import importlib.util
import json
import os
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "analysis" / "w33_pass7310_7312_q7_pauli_validator.py"
SPEC = importlib.util.spec_from_file_location("pass7310_validator", SCRIPT)
assert SPEC and SPEC.loader
M = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(M)


def test_exact_source_hash_packing_and_gauge_firewall() -> None:
    points, result = M.validate_source()
    assert len(points) == 33
    assert result["pairs"] == 528
    assert result["source_points_sha256"] == M.POINTS_SHA256
    assert result["packed_hex"] == M.PACKED_HEX
    assert result["canonical_histogram"] == [0, 88, 90, 94, 90, 90, 76]
    assert result["rescaled_histogram"] == [0, 73, 120, 80, 81, 88, 86]
    assert result["canonical_histogram"] != result["rescaled_histogram"]
    assert result["canonical_histogram"][0] == result["rescaled_histogram"][0] == 0


def test_frozen_certificate_and_physics_boundary() -> None:
    _, exact = M.validate_source()
    M.validate_frozen(exact)
    frozen = json.loads(M.FROZEN.read_text(encoding="utf-8"))
    assert frozen["formal"]["assignments_covered"] == 2**24
    assert frozen["simulation"]["register_serial_cycles_including_load_and_done"] == 33 + 528 + 1
    assert frozen["simulation"]["bram_serial_cycles_including_load_and_done"] == 33 + 3 * 528 + 1
    boundary = frozen["boundary"].lower()
    for exclusion in ("not a maximality proof", "quantum state preparation", "power measurement", "device result"):
        assert exclusion in boundary


def test_namespace_and_synthesizable_surfaces_are_closed() -> None:
    surfaces = [M.RTL, M.TB, M.GAP_REPLAY, M.FORMAL_SCRIPT,
                ROOT / "formal" / "w33_pass7310_q7_pair_equiv_formal.sv"]
    text = "\n".join(path.read_text(encoding="utf-8") for path in surfaces)
    stale_namespace = tuple(str(7200 + offset) for offset in (54, 55, 56))
    assert not any(old in text for old in stale_namespace)
    for module in (
        "w33_pass7310_pauli_pair_q7",
        "w33_pass7311_q7_parallel",
        "w33_pass7311_q7_serial",
        "w33_pass7311_q7_bram",
    ):
        assert module in text


def test_native_gap_replay_when_available() -> None:
    try:
        M.executable("gap")
    except RuntimeError:
        pytest.skip("GAP not installed")
    record = M.replay_gap()
    assert record["all_pass"] is True
    assert record["canonical_histogram"] == M.CANONICAL_HISTOGRAM
    assert record["rescaled_histogram"] == M.RESCALED_HISTOGRAM


def test_exact_snapshot_separates_trivial_psp_from_c2_pcsp() -> None:
    points, _ = M.validate_source()
    result = M.validate_projective_stabilizer(points)
    assert result["projective_psp_stabilizer_order"] == 1
    assert result["projective_pcsp_stabilizer_order"] == 2
    assert result["nontrivial_pcsp_multiplier_is_square"] == [False]
    assert result["nontrivial_pcsp_fixed_selected_points"] == [1]
    assert result["exact_pcsp_orbit_seeds_for_33_points"] == 17


def test_icarus_exact_and_corrupted_replay_when_available() -> None:
    try:
        M.executable("iverilog")
        M.executable("vvp")
    except RuntimeError:
        pytest.skip("Icarus Verilog not installed")
    result = M.simulate()
    assert result["register_cycles"] == 562
    assert result["bram_cycles"] == 1618


@pytest.mark.skipif(os.environ.get("W33_RUN_EDA_SYNTH") != "1",
                    reason="set W33_RUN_EDA_SYNTH=1 for exact iCE40 mapping")
def test_pair_core_ice40_counts_when_yosys_available() -> None:
    try:
        M.executable("yosys")
    except RuntimeError:
        pytest.skip("Yosys not installed")
    tops = ["w33_pass7310_pauli_pair_q7_naive", "w33_pass7310_pauli_pair_q7"]
    result, _, _ = M.synthesize(tops)
    assert result == {top: M.EXPECTED_CELLS[top] for top in tops}
    assert result[tops[1]]["SB_LUT4"] < result[tops[0]]["SB_LUT4"] // 4


@pytest.mark.skipif(os.environ.get("W33_RUN_EDA_FORMAL") != "1",
                    reason="set W33_RUN_EDA_FORMAL=1 for the roughly one-minute SAT replay")
def test_universal_pair_core_formal_proof() -> None:
    result = M.prove_formal()
    assert result == {
        "unconstrained_input_bits": 24,
        "assignments_covered": 2**24,
        "variables": 20319,
        "clauses": 59982,
        "status": "SUCCESS",
    }


@pytest.mark.skipif(os.environ.get("W33_RUN_EDA_PNR") != "1",
                    reason="set W33_RUN_EDA_PNR=1 for the seeded HX8K replay")
def test_serial_place_and_route_proxy() -> None:
    tops = ["w33_pass7311_q7_serial", "w33_pass7311_q7_bram"]
    _, paths, _ = M.synthesize(tops)
    result = M.place_and_route(paths)
    assert result[tops[0]]["logic_cells"] == 2439
    assert result[tops[1]]["logic_cells"] == 230
    assert result[tops[1]]["block_rams"] == 1
