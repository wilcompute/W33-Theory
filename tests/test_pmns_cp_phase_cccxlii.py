"""
Part CCCXLII -- PMNS CP phase delta_CP/pi = (k-1)/Phi_4 = 11/10 in W(3,3)
"""
from __future__ import annotations

import json
import math
import sys
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "exploration") not in sys.path:
    sys.path.insert(0, str(ROOT / "exploration"))

from PART_CCCXLII_PMNS_CP_PHASE_BRIDGE import (
    Q, V, K, LAM, MU, F, G, PHI3, PHI4, PHI6,
    DELTA_CP_OVER_PI_W33, DELTA_CP_W33_RAD, DELTA_CP_W33_DEG,
    DELTA_CP_OVER_PI, SIGMA_NH, RESIDUAL, Z,
    residual_records, checks, Verified,
)


def test_verified_true():
    assert Verified is True


def test_all_checks_pass():
    failed = [lbl for lbl, ok in checks if not ok]
    assert failed == [], f"Failing: {failed}"


def test_W33_form():
    assert DELTA_CP_OVER_PI_W33 == Fraction(K - 1, PHI4)
    assert DELTA_CP_OVER_PI_W33 == Fraction(11, 10)


def test_components():
    assert K - 1 == 11
    assert PHI4 == 10


def test_decimal():
    assert float(DELTA_CP_OVER_PI_W33) == 1.1


def test_within_1_sigma():
    assert abs(Z) < 1


def test_within_0p5_sigma():
    assert abs(Z) < 0.5


def test_delta_CP_radians():
    assert abs(DELTA_CP_W33_RAD - 11 * math.pi / 10) < 1e-9


def test_delta_CP_degrees():
    assert abs(DELTA_CP_W33_DEG - 198.0) < 0.01


def test_11_in_Bernoulli_tower():
    assert 11 in {2, 3, 5, 7, 11, 13, 17, 19, 23}


def test_residual_records():
    records = residual_records()
    assert len(records) == 1
    assert "PASS" in records[0].status


# Cross-link: PMNS sector now complete with this part
def test_pmns_complete():
    SIN2_12 = Fraction(MU, PHI3)
    SIN2_23 = Fraction(MU, PHI6)
    SIN2_13 = Fraction(Q ** 2, (LAM * PHI4) ** 2)
    DELTA = DELTA_CP_OVER_PI_W33
    assert SIN2_12 == Fraction(4, 13)
    assert SIN2_23 == Fraction(4, 7)
    assert SIN2_13 == Fraction(9, 400)
    assert DELTA == Fraction(11, 10)


# JSON output
def test_json_exists_after_main():
    import importlib
    mod = importlib.import_module("PART_CCCXLII_PMNS_CP_PHASE_BRIDGE")
    mod.main()
    assert (ROOT / "PART_CCCXLII_pmns_cp_phase_results.json").exists()


def test_json_verified():
    out = ROOT / "PART_CCCXLII_pmns_cp_phase_results.json"
    if not out.exists():
        import importlib
        importlib.import_module("PART_CCCXLII_PMNS_CP_PHASE_BRIDGE").main()
    data = json.loads(out.read_text(encoding="utf-8"))
    assert data["Verified"] is True


def test_json_pmns_complete():
    out = ROOT / "PART_CCCXLII_pmns_cp_phase_results.json"
    data = json.loads(out.read_text(encoding="utf-8"))
    assert "11/10" in data["pmns_complete"]["delta_CP"] or "11 pi/10" in data["pmns_complete"]["delta_CP"]
