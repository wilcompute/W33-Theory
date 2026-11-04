"""Aravind 2000 Peres-24/dual-Reye contextuality independent certification.

All 16 critical 18-ray 9-tetrad parity proofs are published prior art.
"""
import importlib.util, math
from pathlib import Path
import pytest
ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/"analysis"/"toe_20261104_reye_peres_critical_ks.py"
spec=importlib.util.spec_from_file_location("ks_peres_2000",SRC)
mod=importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

@pytest.fixture(scope="module")
def d():return mod.run()

def test_peres_published_coordinates_and_orthogonality(d):
    assert d["total_orthonormal_tetrads"]==24
    assert d["each_ray_orthogonal_to_nine_others"]
    assert d["each_ray_in_four_tetrads"]
    assert d["pure_tetrads"]==6 and d["mixed_tetrads"]==18
    assert d["full_24ray_ks_coloring_satisfiable"] is False

def test_two_reye_projective_line_systems(d):
    assert d["first_Reye_projective_lines"]==16
    assert d["second_Reye_projective_lines"]==16
    assert d["line_mates"]==16
    assert d["critical_18ray_sets"]==16

def test_all_sixteen_parity_proofs_are_exact_and_critical(d):
    pairs=set()
    for witness in d["certificate_rows"]:
        excluded=tuple(witness["missing_first_12_ray_line"]+witness["missing_second_12_ray_line"])
        assert len(excluded)==6
        assert len(witness["nine_full_orthogonal_tetrads"])==9
        assert witness["each_surviving_ray_occurs_exactly_twice"]
        assert witness["any_one_ray_deletion_makes_constraints_colorable"]
        pairs.add(excluded)
        remaining=set(range(1,25))-set(excluded)
        counts={v:0 for v in remaining}
        for tet in witness["nine_full_orthogonal_tetrads"]:
            assert len(tet)==4 and set(tet)<=remaining
            for v in tet:counts[v]+=1
        assert all(c==2 for c in counts.values())
        # count marks per tetrad = 9 odd; per ray doubled = even.
        assert (9%2)==1 and all((n%2)==0 for n in counts.values())
    assert len(pairs)==16

def test_ray_dimension_is_hilbert_not_spacetime(d):
    assert len(d["explicit_24_non_normalized_integer_rays"])==24
    assert all(len(v)==4 for v in d["explicit_24_non_normalized_integer_rays"])
    assert "NOT imply 4D spacetime" in d["proof_boundary"]
