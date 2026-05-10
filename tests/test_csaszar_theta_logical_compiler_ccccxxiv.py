"""Regression tests for PART CCCCXXIV Csaszar theta logical compiler."""

from __future__ import annotations

import importlib.util
import json
import sys
from functools import lru_cache
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "exploration" / "PART_CCCCXXIV_CSASZAR_THETA_LOGICAL_COMPILER.py"
RESULTS_PATH = ROOT / "PART_CCCCXXIV_csaszar_theta_logical_compiler_results.json"


@lru_cache(maxsize=1)
def load_module():
    spec = importlib.util.spec_from_file_location("csaszar_theta_logical_compiler_ccccxxiv", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


@lru_cache(maxsize=1)
def build_results():
    return load_module().build_results()


def test_all_csaszar_theta_compiler_checks_pass():
    results = build_results()
    assert results["verified"] is True
    assert results["checks_passed"] == results["checks_total"] == 25
    assert all(check["passed"] for check in results["checks"])


def test_local_code_is_csaszar_k7_toric_packet():
    local = build_results()["local_code"]
    assert local["notation"] == "[[21,2,>=3]]"
    assert local["n"] == 21
    assert local["k"] == 2
    assert local["d_lower"] == 3
    assert local["gsd"] == 4
    assert local["rank_hz"] == 6
    assert local["rank_hx"] == 13


def test_five_block_packet_is_lovasz_theta_register():
    packet = build_results()["five_block_packet"]
    assert packet["blocks"] == 5
    assert packet["notation"] == "[[105,10,>=3]]"
    assert packet["n"] == 105
    assert packet["k"] == 10
    assert packet["d_lower"] == 3
    assert packet["check_rank"] == 95
    assert packet["gsd"] == 1024
    assert packet["logical_equals_lovasz_theta"] is True
    assert packet["theta_times_local_gsd"] == 40


def test_szilassi_g2_ancilla_and_rank_120_handoff():
    closure = build_results()["ancilla_and_rank_closure"]
    assert closure["szilassi_ancilla_modes"] == 2
    assert closure["ancilla_g2_modes"] == 14
    assert closure["theta_plus_g2"] == 24
    assert closure["rank_120_closure"] == 120
    assert "105 local Csaszar edge qubits + 14 G2 ancilla modes + 1 scalar" in closure["rank_120_read"]


def test_compiler_layers_are_ordered_and_honest():
    results = build_results()
    assert [layer["name"] for layer in results["compiler_layers"]] == [
        "five_csaszar_input_blocks",
        "lovasz_theta_logical_register",
        "szilassi_g2_ancilla_rail",
        "rank_120_bookkeeping_closure",
    ]
    assert "[[105,10,>=3]]" in results["theorem"]
    assert "theta(W33)=10" in results["theorem"]
    assert "105+14+1=120" in results["theorem"]
    assert "without claiming a canonical isomorphism" in results["theorem"]
    assert "does not replace the Steane/Phi6" in results["honesty_boundary"]


def test_result_artifact_is_present_and_current():
    artifact = json.loads(RESULTS_PATH.read_text(encoding="utf-8"))
    live = build_results()
    assert artifact["part"] == "CCCCXXIV"
    assert artifact["verified"] is True
    assert artifact["checks_passed"] == artifact["checks_total"] == live["checks_total"]
    assert artifact["five_block_packet"] == live["five_block_packet"]
    assert artifact["ancilla_and_rank_closure"] == live["ancilla_and_rank_closure"]


def test_docs_index_exposes_csaszar_theta_compiler():
    text = (ROOT / "docs" / "index.html").read_text(encoding="utf-8")
    assert "Cs" in text and "Theta Logical Compiler" in text
    assert "PART_CCCCXXIV_CSASZAR_THETA_LOGICAL_COMPILER.md" in text
    assert "[[105,10,&ge;3]]" in text
    assert "theta(W33)=10" in text
    assert "theta(complement)=4" in text
    assert "105+14+1=120" in text
