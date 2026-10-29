"""Regression controls for native F2 Klein-quadric gauge-kernel bridge."""
from analysis.w33_20261028_f2_klein_native_gauge_bridge import analyze,pair_result


def test_63_projective_bivectors_split_35_plus_28():
    c=analyze()
    assert c["full_nonzero_bivectors"]==63
    assert c["Klein_quadric_decomposable"]==35
    assert c["off_quadric_nondecomposable"]==28
    assert c["GL4_F2_order"]==20160
    assert c["Sp4_F2_order"]==720
    assert c["symplectic_form_coset_count"]==28


def test_all_15_pairs_and_mod2_reduction():
    c=analyze()
    assert len(c["two_commutator_pairs"])==15
    assert c["pairs_surviving_full_F2_injectivity"]==12
    assert c["pairs_losing_F2_injectivity"]==3
    assert c["distinct_good_F2_kernels"]==6
    assert c["distinct_bad_F2_kernels"]==1


def test_three_even_pfaffians_have_exact_same_bad_directions():
    c=analyze()
    bad=[p for p in c["two_commutator_pairs"]
         if p["bad_nonzero_momenta_F2"]]
    assert [p["indices"] for p in bad]==[[0,1],[0,3],[1,3]]
    assert all(p["bad_nonzero_momenta_F2"]==["0001","1110","1111"]
               for p in bad)
    assert all(p["rank_A_mod_2"]==5 for p in c["two_commutator_pairs"])


def test_optimized_native_pair_has_primitive_symplectic_kernel():
    c=pair_result(0,5)
    assert c["primitive_kernel"]==[0,1,1,1,0,0]
    assert c["integer_pfaffian"]==1
    assert c["pfaffian_mod_2"]==1
    assert c["bad_nonzero_momenta_F2"]==[]
