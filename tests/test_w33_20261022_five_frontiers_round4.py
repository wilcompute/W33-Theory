"""Five independent TOE frontiers: exact mathematical controls and scope."""
import math
import pytest
from analysis.w33_20261022_five_frontiers_round4 import (
    orthogonal_all_prime_theorem,
    native_incidence_clock,
    routing_lower_bound,
    magic_feedforward_nogo,
    pair_group_spectral_bound,
    k_rank_formula,
)


def test_k_module_uniform_prime_formula_and_independent_census():
    x=orthogonal_all_prime_theorem()
    assert x["status"]=="PROVED_ALL_PRIMES_BY_AFFINE_SHORTENING"
    assert len(x["prime_controls"])==11
    for row in x["prime_controls"]:
        p=row["p"]
        ranks=[k_rank_formula(p,k) for k in range(p+1)]
        assert ranks[-1]==0
        assert ranks[0]==row["dimK"]
        expected={1:(p*p+p+4)//2}
        expected.update({j:j for j in range(2,p)})
        expected[p]=p*(p+1)//2
        assert {int(k):v for k,v in row["blocks"].items()}==expected


def test_W33_native_clock_symmetry_and_metastable_uniform():
    x=native_incidence_clock()
    assert x["not_invariant_under_all_S40"] is True
    assert x["invariant_under_PSp43"] is True
    assert x["uniform_free_energy"]>x["concentrated_trial_free_energy"]
    assert min(x["uniform_stability_hessian_eigenvalues"])>0
    assert x["uniform_spinodal_temperature"]==pytest.approx(.04)
    assert x["strict_convexity_sufficient_T_greater_than"]==pytest.approx(1.6)


def test_A_graph_SWAPS_lower_and_upper_bounds_all_40():
    x=routing_lower_bound()
    assert x["parallel_depth_lower_bound"]==3
    assert x["parallel_depth_verified_upper_bound"]==6
    assert x["min_swaps_lower_bound"]==27
    assert x["max_verified_swaps"]==54
    assert len(x["all_anchors"])==40
    for row in x["all_anchors"]:
        assert row["transport_distance_sum"]==54
        assert row["compiled_depth"]==6


def test_ninth_root_no_deterministic_syndrome_feedforward():
    x=magic_feedforward_nogo()
    assert x["zero_input"]["trivial_syndrome_probability"]==1
    assert x["weight4_input"]["trivial_syndrome_probability"]==pytest.approx(1/27)
    assert x["measurement_outcome_total_variation_distance"]==pytest.approx(26/27)
    assert "Does not rule out" in x["limit"]


def test_two_F3_rational_anchors_finite_group_no_go_all_extensions():
    x=pair_group_spectral_bound()
    assert "24" in x["generated_anchor_group"]
    assert x["distinct_defect_levels_upper_bound"]==6
    assert x["distinct_H_levels_bound_all_q_3_power"]==13
    assert x["regular_representation_annihilator_verified"] is True
    assert x["defect_annihilator"]=="z(z-2)(z-4)(z-6)(z^2-6z+6)"
