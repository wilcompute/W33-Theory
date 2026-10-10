"""Regression tests for Passes 11849-11853 (spinorial Lorentz in E8, central Z3, generations, four-point, Lean)."""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))

DATA = ROOT / "data"


def load():
    return json.load(open(DATA / "w33_pass11849_11851_spinor_lorentz_central_z3_generations.json"))


def test_central_z3_gives_standard_model_algebra():
    c = load()["central_Z3"]
    assert all(c["fixes_A5_A2_A1_roots"].values()) and c["commutes_with_A6_lift"]
    sm = c["commutant_of_A6_and_tc"]
    assert (sm["dim"], sm["derived_dim"], sm["centre_dim"], sm["rank"]) == (12, 11, 1, 4)
    assert sm["contains_su3_A2"] and sm["contains_su2_alpha"]


def test_spinorial_lorentz_so11():
    d = load()
    assert d["Di"]["SL29_generated_order"] == 720 and d["Di"]["frobenius_schur_indicator_on_SL29"] == -1.0
    assert max(d["generator_order_errors"]) < 1e-6 and d["Z_fixes_commutant"] < 1e-8
    sp = d["spinor_lorentz"]["commutant"]
    assert (sp["dim"], sp["rank"], sp["centre_dim"]) == (55, 5, 0) and sp["contains_su5_gut"]
    assert d["spinor_matter_blocks_match_so11_x_sp4"]
    r = d["casimir_ratios_to_adjoint"]
    assert abs(r["55_1"] - 10 / 18) < 1e-4 and abs(r["128_2"] - 13.75 / 18) < 1e-4
    assert d["casimir_counts_by_spinor_sign"] == {"1": {"0.0": 10, "0.166667": 55, "0.3": 55}, "-1": {"0.229167": 128}}
    assert d["vector5_versus_Rac"]["overlap"] == 0.0


def test_generations():
    g = load()["generations"]
    assert g["A2_inside_su5gut"] and g["e6_cap_su5gut_dim"] == 4


def test_four_point():
    c = json.load(open(DATA / "w33_pass11852_bulk_four_point.json"))
    assert c["invariant_symmetric_forms_on_boundary_15"] == {"sym2": 1.0, "sym3": 1.0, "sym4": 3.0}
    assert c["rank_of_three_structures"] == 3 and c["hidden_20_detected_at_four_points"]
    assert abs(c["E20_relative_residual_outside_span_C_E15"] - 10 ** -0.5) < 1e-6


def test_lean_module():
    root = (ROOT / "formal" / "W33.lean").read_text(encoding="utf-8")
    assert "import W33.Pass11853HyperchargeSpectrum" in root
    src = (ROOT / "formal" / "W33" / "Pass11853HyperchargeSpectrum.lean").read_text(encoding="utf-8")
    for name in ("spec_length", "spec_counts", "spec_traceless", "w10_is_Q_uc_ec"):
        assert f"theorem {name}" in src
    assert "sorry" not in src
