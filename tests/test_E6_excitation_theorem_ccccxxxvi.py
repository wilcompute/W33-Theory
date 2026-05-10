"""
Part CCCCXXXVI -- The E_6 Excitation Theorem
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "exploration") not in sys.path:
    sys.path.insert(0, str(ROOT / "exploration"))

from PART_CCCCXXXVI_E6_EXCITATION_THEOREM import (
    Q, V, K, LAM, MU, F, G, PHI3, PHI4, PHI6,
    D_F_SQ_SPECTRUM,
    DIM_SU5, DIM_SO10, DIM_E6, DIM_E7, DIM_E8,
    GROUND_82, GAUGE_KINETIC, E_6_GENERATORS, TOTAL_H_F,
    checks, Verified,
)


def test_verified_true():
    assert Verified is True


def test_all_checks_pass():
    failed = [lbl for lbl, ok in checks if not ok]
    assert failed == [], f"Failing: {failed}"


def test_excited_eigenstates_equal_dim_E6():
    """The KEY identification: 48 + 30 = 78 = dim E_6."""
    assert D_F_SQ_SPECTRUM[10] + D_F_SQ_SPECTRUM[16] == 78
    assert DIM_E6 == 78


def test_E_6_dim_78():
    assert DIM_E6 == 78


def test_total_decomposition():
    assert GROUND_82 + GAUGE_KINETIC + E_6_GENERATORS == 480
    assert TOTAL_H_F == 480


def test_ground_82():
    assert GROUND_82 == Q ** 4 + 1
    assert GROUND_82 == 3 * 27 + 1


def test_gauge_kinetic_320():
    """320 = c_EH = lam^3 * v"""
    assert GAUGE_KINETIC == LAM ** 3 * V == 320


def test_E_6_generators_78():
    assert E_6_GENERATORS == 48 + 30 == 78


def test_D_F_squared_spectrum_total():
    assert sum(D_F_SQ_SPECTRUM.values()) == 480


def test_lie_algebra_dimensions_correct():
    assert DIM_SU5 == 24 == F  # = f from W(3,3)
    assert DIM_SO10 == 45
    assert DIM_E6 == 78
    assert DIM_E7 == 133
    assert DIM_E8 == 248


def test_three_generations_of_E6_fundamental():
    """81 = 3 * 27 (3 generations of E_6 fundamental)"""
    assert 3 * 27 == 81 == Q ** 4


def test_a_0_equals_480():
    """The cosmological a_0 equals total H_F dim."""
    assert TOTAL_H_F == 480
    a_0 = LAM ** 5 * G  # 32 * 15 = 480
    assert TOTAL_H_F == a_0


# JSON output
def test_json_exists_after_main():
    import importlib
    mod = importlib.import_module("PART_CCCCXXXVI_E6_EXCITATION_THEOREM")
    mod.main()
    assert (ROOT / "PART_CCCCXXXVI_E6_excitation_theorem_results.json").exists()


def test_json_verified():
    out = ROOT / "PART_CCCCXXXVI_E6_excitation_theorem_results.json"
    if not out.exists():
        import importlib
        importlib.import_module("PART_CCCCXXXVI_E6_EXCITATION_THEOREM").main()
    data = json.loads(out.read_text(encoding="utf-8"))
    assert data["Verified"] is True


def test_json_decomposition_exact():
    out = ROOT / "PART_CCCCXXXVI_E6_excitation_theorem_results.json"
    data = json.loads(out.read_text(encoding="utf-8"))
    decomp = data["Hilbert_space_decomposition"]
    assert decomp["ground_matter"] == 82
    assert decomp["gauge_kinetic_EH"] == 320
    assert decomp["E_6_generators"] == 78
    assert decomp["total"] == 480


def test_json_lie_algebra_dims():
    out = ROOT / "PART_CCCCXXXVI_E6_excitation_theorem_results.json"
    data = json.loads(out.read_text(encoding="utf-8"))
    assert data["Lie_algebra_dimensions"]["E_6"] == 78
    assert data["Lie_algebra_dimensions"]["SU(5)"] == 24
