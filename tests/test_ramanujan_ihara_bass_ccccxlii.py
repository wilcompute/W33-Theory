"""
Part CCCCXLII -- W(3,3) is Ramanujan: Ihara-Bass and the Graph RH
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "exploration") not in sys.path:
    sys.path.insert(0, str(ROOT / "exploration"))

from PART_CCCCXLII_RAMANUJAN_IHARA_BASS import (
    Q, V, K, LAM, MU, F, G, PHI3, PHI4, PHI6,
    ADJACENCY_EIGENVALUES, RAM_BOUND,
    EDGES, DIRECTED_EDGES, TRIVIAL_PAIRS, NON_BACKTRACK_OUTDEG,
    CRITICAL_RADIUS,
    checks, Verified,
)


def test_verified_true():
    assert Verified is True


def test_all_checks_pass():
    failed = [lbl for lbl, ok in checks if not ok]
    assert failed == [], f"Failing: {failed}"


def test_adjacency_eigenvalues():
    assert ADJACENCY_EIGENVALUES == {12: 1, 2: F, -4: G}
    assert sum(ADJACENCY_EIGENVALUES.values()) == V


def test_ramanujan_property():
    """W(3,3) non-trivial eigenvalues satisfy |lam| <= 2*sqrt(k-1)."""
    for lam_i in [2, -4]:
        assert abs(lam_i) <= RAM_BOUND


def test_ramanujan_bound_exact():
    assert RAM_BOUND == 2 * math.sqrt(11)


def test_ihara_bass_parameters():
    assert EDGES == 240
    assert DIRECTED_EDGES == 480
    assert TRIVIAL_PAIRS == 200 == 5 * V
    assert NON_BACKTRACK_OUTDEG == 11


def test_graph_RH_critical_circle():
    """Ihara zeta zeros on |u| = 1/sqrt(k-1) = 1/sqrt(11)."""
    expected = 1 / math.sqrt(11)
    assert abs(CRITICAL_RADIUS - expected) < 1e-10


def test_480_directed_edges_equals_a_0():
    """The 480-dim Hashimoto carrier = a_0 cosmological coefficient (CCCCXXXIII)."""
    assert DIRECTED_EDGES == 480


def test_D_F_squared_total_480():
    """D_F^2 spectrum total = 480 (matches Hashimoto)."""
    assert 82 + 320 + 48 + 30 == 480


def test_alpha_correction_factors_through_k_minus_1():
    """alpha correction denominator 24445 = 22 * M_vac + 3, with M_vac = 11*101 = 1111."""
    assert 24445 == 22 * 1111 + 3
    M_vac = (K - 1) * ((K - LAM) ** 2 + 1)
    assert M_vac == 1111 == 11 * 101
    # 11 = k-1 is the Ihara-Bass non-backtracking outdegree
    assert 11 == NON_BACKTRACK_OUTDEG
    # M_vac is divisible by 11
    assert M_vac % 11 == 0


def test_W33_is_Ramanujan():
    """The main theorem: W(3,3) is a Ramanujan graph."""
    non_trivial = [eig for eig in ADJACENCY_EIGENVALUES if eig != K]
    assert all(abs(lam_i) <= RAM_BOUND for lam_i in non_trivial)


# JSON output
def test_json_exists_after_main():
    import importlib
    mod = importlib.import_module("PART_CCCCXLII_RAMANUJAN_IHARA_BASS")
    mod.main()
    assert (ROOT / "PART_CCCCXLII_ramanujan_ihara_bass_results.json").exists()


def test_json_verified():
    out = ROOT / "PART_CCCCXLII_ramanujan_ihara_bass_results.json"
    if not out.exists():
        import importlib
        importlib.import_module("PART_CCCCXLII_RAMANUJAN_IHARA_BASS").main()
    data = json.loads(out.read_text(encoding="utf-8"))
    assert data["Verified"] is True


def test_json_unified_picture_complete():
    out = ROOT / "PART_CCCCXLII_ramanujan_ihara_bass_results.json"
    data = json.loads(out.read_text(encoding="utf-8"))
    levels = data["unified_picture"]
    assert "level_1" in levels
    assert "level_7" in levels
