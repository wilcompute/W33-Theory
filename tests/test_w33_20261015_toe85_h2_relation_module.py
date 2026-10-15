"""Regression tests for TOE85's exact H27 face-relation module."""
from functools import lru_cache
import json
from pathlib import Path

from analysis.w33_20261015_toe85_h2_relation_module import certificate

ROOT = Path(__file__).resolve().parents[1]


@lru_cache(maxsize=1)
def fresh():
    return certificate()


def test_chain_and_complete_group_action():
    d = fresh()
    assert d["chain_dimensions"] == {"C2":99,"C1":135,"H2":16}
    assert d["verified_signed_face_automorphisms"] == 27
    for field in ("F2","F3"):
        assert d[field]["boundary_rank"] == 83
        assert d[field]["H27_fixed_dimension"] == 2
        assert d[field]["center_generator_rank"] == 6
        assert len(d[field]["elements"]) == 27
        assert len({tuple(e["h"]) for e in d[field]["elements"]}) == 27


def test_binary_maschke_decomposition_and_irreducibility():
    d=fresh()["F2"]
    assert d["rank_g_minus_identity_distribution"] == {"0":1,"6":2,"10":24}
    s=d["semisimple_decomposition"]
    assert s["trivial_dimension"] == 2
    assert s["center_invariant_dimension"] == 10
    assert s["four_nontrivial_F3xF3_character_pairs"] == {
        "1,0":2,"0,1":2,"1,1":2,"1,2":2}
    assert s["faithful_irreducible_dimension"] == 6
    assert s["faithful_nonzero_cyclic_vectors_verified"] == 63
    assert s["order9_subgroup_fixed_dimensions"] == [4]*4


def test_ternary_radical_and_joint_clock_polarization():
    d=fresh()["F3"]
    assert d["rank_g_minus_identity_distribution"] == {
        "0":1,"6":2,"8":6,"10":18}
    assert d["augmentation_radical_filtration_dimensions"] == [
        16,13,10,6,4,2,1,0]
    assert d["Loewy_layer_dimensions"] == [3,3,4,2,2,1,1]
    assert d["F3_trivial_head_dimension"] == 3
    assert d["same_polarization_as_TOE84_H1"]
    A={(0,b,c) for b in range(3) for c in range(3)}
    assert {tuple(x) for x in d["H2_rank8_polarization"]} == A
    x={tuple(e["h"]) for e in d["elements"]
       if e["rank_g_minus_identity"]==8}
    assert x==A-{(0,0,c) for c in range(3)}


def test_frozen_certificate_reproduced_exactly():
    frozen=json.loads((ROOT/"data/w33_20261015_toe85_h2_relation_module.json").read_text(encoding="utf-8"))
    assert fresh()==frozen
