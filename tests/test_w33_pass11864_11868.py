"""Regression tests for Passes 11864-11868 (chirality, B-L condensate, charged sectors, one loop, Lean)."""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))

import w33_pass11864_11866_weyl_chirality_bl_quark_sectors as W  # noqa: E402

DATA = ROOT / "data"


def load():
    return json.load(open(DATA / "w33_pass11864_11866_weyl_chirality_bl_quark_sectors.json"))


def test_lorentz_ambivalent_and_no_helicity():
    c = load()["chirality"]
    assert c["SL29_ambivalent"] and c["elements_with_g2_eq_1"] == 2 and c["elements_with_g2_eq_minus1"] == 90
    assert c["null_little_group_order"] == 36 and c["Di_in_2dim_little_group_reps"] == 4.0
    assert all(abs(v) < 1e-9 for v in c["Di_helicity_multiplicities"].values())


def test_bl_condensate_breaks_to_sm():
    b = load()["bl_breaking"]
    assert b["BL_charged_sm_singlets_all_in_spinor_block"] and b["BL_plus_singlet_dim"] == 4
    assert b["lorentz_invariant_bilinears"] == 1 and b["antisymmetric"] == 1
    s = b["stabiliser_of_generic_condensate"]
    assert s["levi_is_SM_algebra"] and s["nilradical_dim"] == 3 and s["rank"] == 4


def test_charged_sector_little_groups():
    g = W.charged_sector_little_groups()
    assert [r["structure"] for r in g["0"]] == ["A6", "3^2:2", "A4", "A4"]
    for k in ("1", "2"):
        assert [(r["orbit"], r["structure"]) for r in g[k]] == [(6, "A5"), (15, "S4"), (60, "S3")]


def test_one_loop_channels_positive():
    c = json.load(open(DATA / "w33_pass11867_one_loop_positivity.json"))
    ch = {r["dim"]: r for r in c["channels"]}
    assert (ch[60]["Bub"], ch[60]["Tri"], ch[60]["Box"]) == (144.0, 3840.0, 15360.0)
    assert all(r["Bub"] >= 0 and r["Box"] >= 0 for r in c["channels"])
    # 60-channel at one loop: 2 - 96 x + 15360 x^2 has negative discriminant -> positive for all g3
    assert 96**2 - 4 * 2 * 15360 < 0
    assert c["regions_g_prime_zero"]["one_loop"]["allowed_fraction_of_grid"] > c["regions_g_prime_zero"]["tree"]["allowed_fraction_of_grid"]


def test_lean_module():
    root = (ROOT / "formal" / "W33.lean").read_text(encoding="utf-8")
    assert "import W33.Pass11868A6NotInGL2RealFixed" in root
    src = (ROOT / "formal" / "W33" / "Pass11868A6NotInGL2RealFixed.lean").read_text(encoding="utf-8")
    for name in ("no_injective_hom_GL2", "real_structure_fixed", "s1_commutator", "comm_kills"):
        assert f"theorem {name}" in src
    assert "sorry" not in src
