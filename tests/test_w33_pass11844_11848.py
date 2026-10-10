"""Regression tests for Passes 11844-11848 (E8 Lorentz lifts and hypercharge, translations, matter, bulk path integral, Lean)."""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))

import w33_pass11847_finite_bulk_path_integral as BP  # noqa: E402

DATA = ROOT / "data"


def test_lifts_and_hypercharge():
    c = json.load(open(DATA / "w33_pass11844_11846_e8_poincare_lifts_matter.json"))
    assert c["lifts"]["adjacent_tits_order"] == 360 and c["lifts"]["permutation_order"] == 360
    cm = c["commutants"]
    assert (cm["A6_adjacent"]["dim"], cm["A6_adjacent"]["rank"], cm["A6_adjacent"]["centre_dim"]) == (24, 4, 0)
    assert cm["A6_permutation"]["dim"] == 24 and cm["extension_11843"]["dim"] == 11 and cm["ext_inside_A6_adjacent"]
    h = c["hypercharge"]
    assert h["centraliser_dim"] == 1 and h["equals_georgi_glashow_pattern"]
    sm = c["A6_plus_hypercharge_rotation_commutant"]
    assert (sm["dim"], sm["derived_dim"], sm["centre_dim"], sm["rank"]) == (12, 11, 1, 4)
    assert sm["contains_su3_A2"] and sm["contains_su2_alpha"]


def test_matter_lorentz_content():
    c = json.load(open(DATA / "w33_pass11844_11846_e8_poincare_lifts_matter.json"))
    rows = {(r["Y"], r["dim"]): r for r in c["matter"]}
    # GUT 10 pieces (Q, u^c, e^c) in an irreducible Lorentz 5; GUT 5bar pieces (d^c, L) in an irreducible Lorentz 10
    assert rows[("1/6", 30)]["lorentz_char_norm"] == 36.0 and rows[("2/3", 15)]["lorentz_char_norm"] == 9.0
    assert rows[("1", 5)]["lorentz_char_norm"] == 1.0
    assert rows[("1/3", 30)]["lorentz_char_norm"] == 9.0 and rows[("1/2", 20)]["lorentz_char_norm"] == 4.0
    assert rows[("5/6", 6)]["lorentz_invariants"] == 6.0  # X, Y gauge bosons are Lorentz-trivial


def test_translations_central_extension():
    t = json.load(open(DATA / "w33_pass11844_11846_e8_poincare_lifts_matter.json"))["translations"]
    assert t["four_dim_submodules"] == 0
    f = t["five_dim"]
    assert f["equals_A5_lattice_mod3"] and f["form_rank_mod3"] == 4 and f["quotient_orbits_nonzero"] == [20, 30, 30]
    for v in t["poincare_with_central_Z3_commutants"].values():
        assert (v["dim"], v["rank"]) == (11, 3) and v["contains_su3_A2"] and v["contains_su2_alpha"]


def test_bulk_path_integral():
    c = json.load(open(DATA / "w33_pass11847_finite_bulk_path_integral.json"))
    assert c["G_equals_12_projector_15"] and c["two_point_is_multiple_of_boundary_15_projector"] and c["hidden_20_invisible"]
    assert c["boundary_two_point"] == {"meet:-27.0": 480, "opposite:9.0": 1080, "same:81.0": 40}
    assert c["tree_three_point_equals_c_times_boundary_cubic"] and c["hidden_20_circulates_in_bubble"]
    K, X, A, G, N, Cx = BP.setup()
    assert abs((G @ G - 12 * G)).max() < 1e-9


def test_lean_module():
    root = (ROOT / "formal" / "W33.lean").read_text(encoding="utf-8")
    assert "import W33.Pass11848CrosscapProjector" in root
    src = (ROOT / "formal" / "W33" / "Pass11848CrosscapProjector.lean").read_text(encoding="utf-8")
    for name in ("crosscap_symm", "crosscap_symmetric", "crosscap_antisymmetric", "bulk_projector"):
        assert f"theorem {name}" in src
    assert "sorry" not in src
