"""Regression boundaries for corrected Pass 201--208 live artifacts.

Mathematical arithmetic/withdrawal checks run in GAP.  Python only launches
GAP, parses JSON, and checks that public artifacts cannot resurrect withdrawn
interpretations.
"""

from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def _run_gap(script: str) -> None:
    gap = shutil.which("gap")
    assert gap is not None, "GAP is required"
    completed = subprocess.run(
        [gap, "-q", str(ROOT / "analysis" / script)],
        cwd=ROOT,
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=30,
    )
    assert "PASS" in completed.stdout


def _json(name: str) -> dict:
    return json.loads((ROOT / "data" / name).read_text(encoding="utf-8"))


def test_pass201_and_204_are_label_space_claims_only() -> None:
    pass201 = _json("w33_pass201_sentinel_css_logical_shadow.json")
    pass204 = _json("w33_pass204_transversal_clifford.json")
    assert pass201["css_code"]["full_logical_pauli_dimension"] == 20
    assert pass201["coordinate_automorphisms"]["group"].startswith("PSp(4,3)")
    assert "does not claim a built-in fault-tolerant gate set" in (
        pass201["coordinate_automorphisms"]["reading"]
    )
    assert "logical_action" not in pass204
    assert pass204["label_action"]["corrected_clifford_lift"] == (
        "diag(M,M^(-T)) in Sp(20,2) (Pass 211)"
    )
    assert pass204["image_order_census"]["involutions_not_CZ_gates"] == 315


def test_pass202_gap_arithmetic_never_overwrites_or_overclaims_lean() -> None:
    _run_gap("w33_pass202_shadow_dichotomy_arithmetic.g")
    cert = _json("w33_pass202_shadow_dichotomy_arithmetic.json")
    assert cert["certified_scope"] == {
        "arithmetic_only": True,
        "constructs_W3q": False,
        "proves_quadratic_shadow_nondegenerate": False,
        "higher_q_module_structure": "prediction only",
    }
    assert cert["lean_source_written"] is False
    launcher = (ROOT / "analysis" / "w33_pass202_shadow_dichotomy_arithmetic.py").read_text(encoding="utf-8")
    assert '"gap", "-q"' in launcher
    assert "LEAN.write_text" not in launcher


def test_pass206_is_a_gap_owned_withdrawal_not_a_subsystem_certificate() -> None:
    _run_gap("w33_pass206_subsystem_claim_withdrawal.g")
    cert = _json("w33_pass206_subsystem_distance_boost.json")
    assert cert["status"] == "WITHDRAWN"
    assert cert["checks"]["unsupported_subsystem_claim_present"] is False
    assert "not established" in cert["withdrawn_claims"]["subsystem_parameters"]
    launcher = (ROOT / "analysis" / "w33_pass206_subsystem_distance_boost.py").read_text(encoding="utf-8")
    assert '"gap", "-q"' in launcher
    assert "numpy" not in launcher


def test_pass207_gap_scope_and_pass208_nonparabolic_route_boundary() -> None:
    _run_gap("w33_pass207_lean_shadow_certificate.g")
    pass207 = _json("w33_pass207_lean_shadow_certificate.json")
    pass208 = _json("w33_pass208_route_clock_s6.json")
    assert pass207["verification"]["lean_parser"] is False
    assert pass207["verification"]["lean_kernel_run"] is False
    assert pass207["verification"]["typecheck_guaranteed"] is False
    assert "non-parabolic spread/double-six stabilizer" in (
        pass208["two_platonic_clocks"]["reading"]
    )
    assert "both are quotients of the substrate's maximal parabolics" not in (
        pass208["two_platonic_clocks"]["reading"]
    )


def test_superseded_pass209_210_draft_certificates_are_absent() -> None:
    assert not (ROOT / "data" / "w33_pass209_two_clock_structure.json").exists()
    assert not (ROOT / "data" / "w33_pass210_doily_in_crown.json").exists()
