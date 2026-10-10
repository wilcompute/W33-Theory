"""Regression tests for Passes 11831-11833 (the finite AdS4 of two qutrits)."""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))

import w33_pass11831_11833_finite_ads4 as F  # noqa: E402

DATA = ROOT / "data"


def test_clifford_quadric_dictionary():
    c = F.classify()
    assert c["n_points"] == 121 and c["clifford_relation_all_pairs"]
    assert dict(c["counts"]) == {"null": 40, "square": 45, "nonsquare": 36}
    assert (c["lagrangians"], c["factorisations"], c["kramers"]) == (40, 45, 36)


def test_cross_track_readings():
    k = F.kramers_locality()
    assert k["local_iff_orthogonal_and_always_swap"] and k["splits_per_reversal"] == {15: 36}
    o = F.orth_equals_disjoint()
    assert o["orthogonal_iff_octets_disjoint"] and o["all_split_frames"] == 27 and o["frames_partition_40_points"]
    assert F.frames() == {"0_kramers+5_splits": 27, "2_kramers+3_splits": 270, "4_kramers+1_splits": 135}


def test_certificate():
    c = json.load(open(DATA / "w33_pass11831_11833_finite_ads4.json"))
    assert c["group_order"] == 51840
    assert c["stabilisers"]["nonsquare"]["stabiliser"] == 1440 and c["stabilisers"]["square"]["stabiliser"] == 1152
    lz = c["lorentz"]
    assert lz["centraliser_is_SL29_by_order_statistics"] and lz["centre_size"] == 2
    assert lz["celestial_sphere_size"] == 10 and lz["celestial_equals_orthogonal_null_points"]
    assert lz["image_on_sphere"] == 720 and lz["image_of_centraliser"] == 360 and lz["image_is_S6_PSigmaL29"]
    ap = c["apartments"]
    assert ap["component_equals_factorisation"] and ap["equals_J42_box_J42"]
    t = c["tangent"]
    assert [o[0] for o in t["lorentz_SL29_orbits"]] == [1, 20, 30, 30]
    lc = t["light_cone_graph"]
    assert lc["degree"] == [20] and lc["lam"] == [1] and lc["mu"] == [6]
    assert t["spinor_map"]["fibre_sizes"] == [4] and t["spinor_map"]["image_is_null_cone"]
    assert c["pairs"]["kramers_composition"] == {
        "beta!=0: (M-beta)^2=0 (unipotent tick)": 360,
        "orthogonal: M^2=-1 (Fourier type)": 270,
    }
