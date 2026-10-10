"""Regression tests for Passes 11854-11858 (family no-go, chirality firewall, bootstrap channels, combined group, Lean)."""

import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))

import w33_pass11854_11857_family_nogo_chirality_firewall_combined as X  # noqa: E402

DATA = ROOT / "data"


def load():
    return json.load(open(DATA / "w33_pass11854_11857_family_nogo_chirality_firewall_combined.json"))


def test_family_nogo_centralisers():
    d = load()
    g = d["centraliser_gut_plus_family"]
    assert (g["dim"], g["derived_dim"], g["centre_dim"], g["rank"]) == (4, 3, 1, 2)
    s = d["centraliser_sm_plus_family"]
    assert (s["dim"], s["derived_dim"], s["centre_dim"]) == (5, 3, 2)


def test_chirality_firewall_clifford_model():
    f = X.chirality_firewall(np.random.default_rng(7), trials=30)
    assert f["quaternionic_structure"] and f["J_commutes_with_spin11"] and f["all_kept_spaces_J_invariant"]
    v = f["spin10_volume_projection"]
    assert v["lorentz_commuting_+1"]["net_16_minus_16bar"] == 0.0 and v["lorentz_commuting_-1"]["kept_dim_in_32"] == 0
    assert abs(v["lorentz_breaking_i"]["net_16_minus_16bar"]) == 16.0


def test_combined_group():
    c = load()["combined"]
    assert max(c["tc_commutes_with_spinor_lift"]) < 1e-9
    cm = c["commutant"]
    assert (cm["dim"], cm["rank"], cm["centre_dim"]) == (19, 5, 1) and cm["structure_su3_u1_so5"]
    assert cm["contains_su3_A2"] and cm["contains_su2_alpha"]


def test_bootstrap_channels():
    b = json.load(open(DATA / "w33_pass11856_boundary_bootstrap_channels.json"))
    assert b["all_structures_scalar_on_channels"]
    dims = sorted(r["dim"] for r in b["channels"])
    assert dims == [1, 15, 20, 24, 60, 105]
    ch = {r["dim"]: r for r in b["channels"]}
    assert ch[60]["C"] == 0 and ch[60]["E20"] == 0 and ch[60]["E15"] != 0
    assert ch[24]["C"] == 0 and ch[24]["E20"] != 0
    assert b["characters"]["Sym2_15"]["known_constituents"] == {"1": 1.0, "15_S": 1.0, "20_b": 1.0, "24": 1.0}


def test_lean_module():
    root = (ROOT / "formal" / "W33.lean").read_text(encoding="utf-8")
    assert "import W33.Pass11858A5LatticeMod3" in root
    src = (ROOT / "formal" / "W33" / "Pass11858A5LatticeMod3.lean").read_text(encoding="utf-8")
    for name in ("one_in_S", "one_fixed", "radical", "counts", "no_invariant_functional"):
        assert f"theorem {name}" in src
    assert "sorry" not in src
