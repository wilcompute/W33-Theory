"""Regression tests for Passes 11826-11830 (Z6-II candidate ranking; qutrit flavour in 4D SU(9))."""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))

import w33_pass11826_11830_z6ii_candidate_and_qutrit_flavour as Z  # noqa: E402

DATA = ROOT / "data"


def test_pauli_invariants():
    inv = Z.invariant_dims()
    assert inv == {"fundamental_9": 0, "adjoint_80": 0, "wedge3_84": 4}


def test_z3z3_at_most_one_entry_per_row():
    t = Z.z3z3_textures()
    assert t["max_entries_per_row"] == 1
    assert "rank-1 (one heavy family)" in t["kinds"] and "permutation (degenerate)" in t["kinds"]


def test_certificate():
    c = json.load(open(DATA / "w33_pass11826_11830_z6ii_candidate_and_qutrit_flavour.json"))
    assert len(c["order"]) >= 1 and c["best"] is not None
    # the best-scoring model has NO cubic top; the single-cubic-top models all allow renormalisable QLd (udd at degree <= 1)
    assert c["best"]["n_up_cubic"] == 0
    single = [r for r in c["ranking"].values() if r.get("n_up_cubic") == 1]
    assert len(single) >= 3 and all(r["qLd_min"] == 0 and r["udd_min"] <= 1 for r in single)
    assert c["qutrit_flavour"]["pauli_invariants"]["wedge3_84"] == 4
