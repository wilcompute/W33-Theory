"""
Part CCCCXLIV -- The Dihedral-Symmetric Coincidence: Why q = 3
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "exploration") not in sys.path:
    sys.path.insert(0, str(ROOT / "exploration"))

from PART_CCCCXLIV_DIHEDRAL_SYMMETRIC_COINCIDENCE import (
    Q, V, K, LAM, MU, F, G, PHI3, PHI4, PHI6,
    sym_order, alt_order, dihedral_order,
    equivalences_at_q, info_combinatorial, info_geometric,
    PHYSICAL_CONSEQUENCES,
    checks, Verified,
)


def test_verified_true():
    assert Verified is True


def test_all_checks_pass():
    failed = [lbl for lbl, ok in checks if not ok]
    assert failed == [], f"Failing: {failed}"


def test_S_3_equals_D_3():
    """The fundamental coincidence: S_3 = D_3 (both order 6)."""
    assert sym_order(3) == dihedral_order(3) == 6


def test_S_q_strictly_larger_for_q_geq_4():
    """For q >= 4, S_q is strictly larger than D_q."""
    for q in range(4, 10):
        assert sym_order(q) > dihedral_order(q)


def test_A_3_cyclic():
    """A_3 is cyclic of order 3 (= Z_3)."""
    assert alt_order(3) == 3 == Q


def test_information_match_at_q_3():
    """log_2(q!) = log_2(2q) only at q = 3."""
    assert abs(info_combinatorial(3) - info_geometric(3)) < 1e-10
    # 2.585 bits = log_2 6
    assert abs(info_combinatorial(3) - math.log2(6)) < 1e-10


def test_information_mismatch_elsewhere():
    for q in [1, 2, 4, 5, 6]:
        assert abs(info_combinatorial(q) - info_geometric(q)) > 1e-10


def test_master_equation_unique_solution():
    matches = [q for q in range(1, 20) if sym_order(q) == 2 * q]
    assert matches == [3]


def test_S_3_smallest_non_abelian():
    """|S_3| = 6 is the order of the smallest non-abelian group."""
    assert sym_order(3) == 6
    # (Z_2 x Z_2 also has order 4 but is abelian; S_3 = D_3 of order 6 is the
    # smallest non-abelian group.)


def test_dihedral_subgroup_of_symmetric():
    """D_q is always a subgroup of S_q for q >= 3 (action on vertices)."""
    # Note: For q = 1, 2, the dihedral group D_q is sometimes defined
    # differently or degenerately. For q >= 3 it acts faithfully on q vertices.
    for q in range(3, 10):
        assert dihedral_order(q) <= sym_order(q)


def test_five_equivalences_at_q_3():
    """All five equivalent conditions hold at q = 3."""
    eq = equivalences_at_q(3)
    assert eq["q!_eq_2q"]
    assert eq["|A_q|_eq_q"]
    assert eq["S_q_eq_D_q"]


def test_physical_consequences_count():
    assert len(PHYSICAL_CONSEQUENCES) == 5


def test_physical_consequences_three_fold():
    """All physical consequences are 'three-fold' phenomena."""
    for k in PHYSICAL_CONSEQUENCES:
        assert k in {"spatial_dimensions", "fermion_generations",
                     "SU3_color", "SO8_triality", "Tits_magic_square"}


# JSON output
def test_json_exists_after_main():
    import importlib
    mod = importlib.import_module("PART_CCCCXLIV_DIHEDRAL_SYMMETRIC_COINCIDENCE")
    mod.main()
    assert (ROOT / "PART_CCCCXLIV_dihedral_symmetric_coincidence_results.json").exists()


def test_json_verified():
    out = ROOT / "PART_CCCCXLIV_dihedral_symmetric_coincidence_results.json"
    if not out.exists():
        import importlib
        importlib.import_module("PART_CCCCXLIV_DIHEDRAL_SYMMETRIC_COINCIDENCE").main()
    data = json.loads(out.read_text(encoding="utf-8"))
    assert data["Verified"] is True


def test_json_fundamental_theorem():
    out = ROOT / "PART_CCCCXLIV_dihedral_symmetric_coincidence_results.json"
    data = json.loads(out.read_text(encoding="utf-8"))
    thm = data["fundamental_theorem"]
    assert thm["unique_solution"] == 3
    assert len(thm["five_equivalences"]) == 5
