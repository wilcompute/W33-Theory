from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "PART_W33_PASS4725_4726_INVOLUTION_RESIDUE_DUAL_CODE.json"


def D():
    return json.loads(DATA.read_text(encoding="utf-8"))


def test_4725_residue_kernel_code():
    d = D()["4725_kernel_code"]
    assert d["rank_Astar_F2"] == 10
    assert d["residue_span_dimension"] == 30
    assert d["parameters"] == "[40,30,4]"
    assert d["low_weight_kernel_census"] == {"1": 0, "2": 0, "3": 0, "4": 270}
    assert d["minimum_shell_size"] == 270
    assert "ker_F2(A_*)" in d["identity"]
    assert "im_F2(A_*)^perp" in d["identity"]


def test_4726_H10_is_reconstructed_by_minimum_involution_checks():
    d = D()["4726_H10_dual_reconstruction"]
    assert d["H10_parameters"] == "[40,10,12]"
    assert d["dual_parameters"] == "[40,30,4]"
    assert d["minimum_parity_checks"] == 270
    assert d["H10_weight_enumerator"] == {
        "0": 1, "12": 40, "16": 135, "20": 672,
        "24": 135, "28": 40, "40": 1,
    }
    dual = {int(k): v for k, v in d["dual_weight_enumerator"].items()}
    assert sum(dual.values()) == 2**30
    assert dual[4] == dual[36] == 270
    assert dual[40] == 1
    assert d["all_one_in_dual"] is True
    assert "common orthogonal kernel" in d["reconstruction"]
