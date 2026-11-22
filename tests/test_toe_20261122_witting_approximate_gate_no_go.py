"""Exact regression tests for the Witting gate-approximation no-go."""
import sys
from pathlib import Path

import sympy as sp

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "analysis"))
import toe_20261122_witting_approximate_gate_no_go as witness


def test_exact_spectrum():
    certificate = witness.verify()
    assert certificate["status"] == "PASS_EXACT_SYMBOLIC"
    assert certificate["operator_Schmidt_rank"] == 8
    assert certificate["squared_Schmidt_spectrum"] == (
        ["17/2", "9/2"] + ["1/2"] * 6
    )


def test_robust_fidelity_ceiling_and_diamond_floor():
    rows = witness.verify()["bounds"]
    assert [r["average_gate_fidelity_ceiling"] for r in rows] == [
        "19/34", "14/17", "15/17", "1"
    ]
    assert rows[2]["process_fidelity_ceiling"] == "7/8"
    assert rows[2]["diamond_distance_floor"] == "sqrt(2)/2"


def test_exact_unitary_realignment_and_local_rank():
    U = witness.canonical_chart_gate()
    R = witness.realign(U)
    assert (U*U.H-sp.eye(16)).applyfunc(sp.simplify) == sp.zeros(16)
    assert sp.simplify(sp.trace(R*R.H)-16) == 0
    A = sp.diag(1,-1,1,-1)
    B = sp.eye(4)
    assert witness.realign(sp.kronecker_product(A,B)).rank() == 1
