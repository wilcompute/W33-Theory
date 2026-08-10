"""Pytest suite for Pass 92 -- discriminant form of the W(3,3) code-lattice = E8/2E8 = O+_8(2)."""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))


def _data() -> dict:
    import w33_pass92_discriminant_e8 as mod

    mod.main()
    return json.loads(Path("w33_pass92_discriminant_e8.json").read_text(encoding="utf-8"))


def test_status_pass() -> None:
    assert _data()["status"] == "PASS"


def test_glue_group_is_Z2_8() -> None:
    g = _data()["glue_group"]
    assert g["order"] == 256
    assert g["C_dim"] == 16 and g["Cperp_dim"] == 24  # (Z/2)^8


def test_coset_split_120_135() -> None:
    d = _data()
    dist = {int(k): v for k, v in d["coset_minweight_distribution"].items()}
    assert dist == {0: 1, 6: 120, 8: 135}
    assert d["anisotropic_norm1_count"] == 120
    assert d["isotropic_count"] == 135
    assert 120 + 135 == 2**8 - 1


def test_is_O_plus_8_2_form() -> None:
    o = _data()["O_plus_8_2"]
    assert o["isotropic_formula_(2^4-1)(2^3+1)"] == 135  # (2^4-1)(2^3+1)
    assert o["anisotropic_formula_2^7-2^3"] == 120  # 2^7 - 2^3
    assert o["type"].startswith("plus")


def test_120_is_240_E8_roots_mod_pm1() -> None:
    d = _data()
    assert d["anisotropic_norm1_count"] == 240 // 2  # E8 roots mod +-1
    assert "E8/2E8" in d["e8_identification"]
