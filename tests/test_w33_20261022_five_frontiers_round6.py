"""Five exact W33 TOE round-six research regressions, no physical TOE overclaim."""
import itertools
import math
import numpy as np
from analysis.w33_20261022_five_frontiers_round6 import (
    field,make_geometry,primepower_module,extension_research,
    microscopic_chiral_projector,routing_matchings,
    bell_resource_injection,w33_point_q9_spectral,sparse_point_equivalence
)
from analysis.w33_20261022_five_followups_round5 import A,cycles,transvection


def test_three_finite_fields_and_prime_power_css_modules():
    for q in (4,8,9):
        p,add,mul=field(q)
        for a,b in itertools.product(range(q),repeat=2):
            assert add(a,b)==add(b,a)
            assert mul(a,b)==mul(b,a)
            assert mul(a,1)==a
        for a in range(1,q):
            assert any(mul(a,b)==1 for b in range(1,q))
    results=extension_research()["cases"]
    assert [(x["q"],x["n"],x["Cdim"],x["Qdim"]) for x in results]==[
        (4,85,16,53),(8,585,64,457),(9,820,100,620)]
    assert [x["delta_higher_rank"][0] for x in results]==[0,0,4]
    assert results[2]["delta_higher_rank"]==[4,16,0]
    assert results[2]["Jordan_C"]=={"1":13,"2":12,"3":21}
    assert results[2]["Jordan_K"]=={"1":70,"2":16,"3":206}
    assert results[2]["Jordan_Q"]=={"1":49,"2":32,"3":169}


def test_microscopic_clock_parity_selection_and_nonzero_composite():
    x=microscopic_chiral_projector()
    assert x["ground_rank"]==5
    assert x["ground_projection_current_exactly_zero"]
    assert x["composite_ground_projection_nonzero"]
    assert "9/32" in x["composite_projected_minimal_polynomial"]
    eig=np.asarray(x["composite_ground_spectrum"])
    assert np.allclose(eig,
        [-3*np.sqrt(2)/8]*2+[0]*5+[3*np.sqrt(2)/8]*2,atol=1e-9)
    assert x["selection_proved"] is False


def test_four_layer_hub_matching_entropy_and_restricted_optimum():
    x=routing_matchings()
    assert x["one_anchor_matchings"]==8124
    assert x["distinct_available_hubs"]==12
    assert x["restricted_normal_form_min_swaps"]==36
    assert x["restricted_normal_form_min_depth"]==4
    assert x["global_SWAPS_bounds"]==[27,36]
    assert x["global_depth_bounds"]==[3,4]
    # Other projective point anchors have the same 4-way common-neighbor combinatorics.
    for anchor in (1,7,13,27,39):
        c=cycles(transvection(anchor))
        moving={v for triple in c for v in triple}
        assert len(c)==9
        assert all(sum(all(A[h,z]==1 for z in triple) and h not in moving
                       for h in range(40))==4 for triple in c)


def test_all_nine_magic_Bell_branches_are_Clifford_correctable():
    x=bell_resource_injection()
    assert len(x["outcomes"])==9
    assert all(np.isclose(y["outcome_probability"],1/9)
               for y in x["outcomes"])
    assert x["native_magic_preparation_or_distillation"] is False
    assert x["fault_threshold"] is False
    assert "Clifford" in x["correction"]


def test_q9_W33_pointspace_controls_13_23_51():
    x=w33_point_q9_spectral()
    rows=x["cases"]
    assert [(v["q"],v["second_transvection_parameter"]) for v in rows]==[
        (3,1),(9,1),(9,3),(9,4)]
    assert [v["generated_group_order"] for v in rows]==[24,24,120,720]
    assert [v["certified_distinct_pointspace_eigenvalues_lower_bound"]
            for v in rows]==[12,13,23,51]
    assert all(z["saturated"] for z in rows)
    assert all(z["certified_distinct_pointspace_eigenvalues_lower_bound"]<=z["dimension"] for z in rows)
    assert rows[-1]["dimension"]==820


def test_rank_one_dense_to_sparse_W33_point_equivalence():
    cert=sparse_point_equivalence()
    assert cert["status"]=="EXACT_RANK_ONE_DENSE_TO_SPARSE_SPECTRAL_EQUIVALENCE"
    rows=cert["cases"]
    assert [(r["q"],r["shear"]) for r in rows]==[(3,1),(9,1),(9,3),(9,4)]
    assert all(r["nonconstant_spectra_identical"] for r in rows)
    assert all(r["constant_isolated_in_sparse_model"] for r in rows)
    for r in rows:
        assert r["constant_eigenvalue_sparse"]==r["n"]
        assert r["constant_eigenvalue_dense"]==0
        assert r["A_degree"]==r["q"]*(r["q"]+1)
        assert r["sparse_max_nondiagonal_neighbors"]<=r["A_degree"]+4
        assert r["sparse_max_nondiagonal_neighbors"]<r["B_degree"]
