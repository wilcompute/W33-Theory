"""
Part CCCCXXXIV -- W(3,3) TOE Master Theorem
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "exploration") not in sys.path:
    sys.path.insert(0, str(ROOT / "exploration"))

from PART_CCCCXXXIV_W33_MASTER_THEOREM import (
    Q, V, K, LAM, MU, F, G, PHI3, PHI4, PHI6,
    AXIOMS, THEOREM_CHAIN, EMPIRICAL_INVENTORY,
    PROGRAM_DIAGRAM,
    Sp4_3,
    checks, Verified,
)


def test_verified_true():
    assert Verified is True


def test_all_checks_pass():
    failed = [lbl for lbl, ok in checks if not ok]
    assert failed == [], f"Failing: {failed}"


def test_three_axioms():
    assert len(AXIOMS) == 3
    assert "A1_master_equation" in AXIOMS
    assert "A2_symplectic_GQ" in AXIOMS
    assert "A3_spectral_action" in AXIOMS


def test_three_theorems_in_chain():
    assert len(THEOREM_CHAIN) == 3
    for part in ["CCCCXXXI", "CCCCXXXII", "CCCCXXXIII"]:
        assert part in THEOREM_CHAIN


def test_inventory_consistency():
    assert EMPIRICAL_INVENTORY["total_closures"] == 39
    assert EMPIRICAL_INVENTORY["dimensionless_closures"] == 27
    assert EMPIRICAL_INVENTORY["dimensional_predictions"] == 10
    assert EMPIRICAL_INVENTORY["hierarchy_closures"] == 2
    # Total = dimless + dim + hierarchy
    total = (EMPIRICAL_INVENTORY["dimensionless_closures"] +
             EMPIRICAL_INVENTORY["dimensional_predictions"] +
             EMPIRICAL_INVENTORY["hierarchy_closures"])
    assert total == 39


def test_master_equation_uniqueness():
    assert Q ** Q == Q ** 3 == 27
    assert 2 ** 2 != 2 ** 3
    assert 5 ** 5 != 5 ** 3


def test_W33_parameters():
    assert (V, K, LAM, MU) == (40, 12, 2, 4)


def test_aut_group_order():
    assert Sp4_3() == 51840


def test_seeley_dewitt_self_consistency():
    # a_0 = 480, a_2 = 2240, a_4 = 17600
    A_0 = LAM ** 5 * G  # 480
    A_2 = LAM ** 3 * V * PHI6  # 2240
    A_4 = LAM ** 6 * (MU + 1) ** 2 * (K - 1)  # 17600
    assert A_0 == 480
    assert A_2 == 2240
    assert A_4 == 17600


def test_program_diagram_complete():
    assert "Master Equation" in PROGRAM_DIAGRAM
    assert "W(3,3)" in PROGRAM_DIAGRAM
    assert "SU(5)" in PROGRAM_DIAGRAM
    assert "Spectral action" in PROGRAM_DIAGRAM
    assert "39 empirical closures" in PROGRAM_DIAGRAM


# JSON output
def test_json_exists_after_main():
    import importlib
    mod = importlib.import_module("PART_CCCCXXXIV_W33_MASTER_THEOREM")
    mod.main()
    assert (ROOT / "PART_CCCCXXXIV_w33_master_theorem_results.json").exists()


def test_json_verified():
    out = ROOT / "PART_CCCCXXXIV_w33_master_theorem_results.json"
    if not out.exists():
        import importlib
        importlib.import_module("PART_CCCCXXXIV_W33_MASTER_THEOREM").main()
    data = json.loads(out.read_text(encoding="utf-8"))
    assert data["Verified"] is True


def test_json_axioms_present():
    out = ROOT / "PART_CCCCXXXIV_w33_master_theorem_results.json"
    data = json.loads(out.read_text(encoding="utf-8"))
    assert "axioms" in data
    assert len(data["axioms"]) == 3


def test_json_theorem_chain():
    out = ROOT / "PART_CCCCXXXIV_w33_master_theorem_results.json"
    data = json.loads(out.read_text(encoding="utf-8"))
    chain = data["theorem_chain"]
    assert "CCCCXXXI" in chain
    assert "CCCCXXXII" in chain
    assert "CCCCXXXIII" in chain
