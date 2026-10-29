"""Exact five-channel Pfaffian theorem and six-cosine native Bloch controls."""
from analysis.w33_20261028_six_term_native_bloch_repair import (
    projective_bivector_theorem,native_character_census,make_certificate,
)


def test_five_flux_channels_have_primitive_nondecomposable_kernel():
    theorem=projective_bivector_theorem()
    assert theorem["kernel_generator"]==[0,1,1,1,0,0]
    assert theorem["kernel_pfaffian"]==1
    assert theorem["nondecomposable_kernel"]
    assert theorem["total_channels_after_repair"]==5
    assert theorem["two_added_original_commutator_indices"]==[0,5]


def test_all_15_two_commutator_choices_are_projectively_complete():
    theorem=projective_bivector_theorem()
    assert theorem["all_15_commutator_pairs_are_non_decomposable"]
    choices=theorem["all_pair_pfaffians"]
    assert len(choices)==15
    assert {(tuple(z["indices"])) for z in choices}=={
        (i,j) for i in range(6) for j in range(i+1,6)
    }
    assert all(z["primitive_pfaffian"] in (1,25,30) for z in choices)


def test_inactive_momentum_line_is_exactly_nonexceptional():
    theorem=projective_bivector_theorem()
    assert theorem["inactive_momentum_line"]=="z0=z1=z2=1"
    assert theorem["inactive_line_exceptional_Q"]=="6*(z3^-1-1)^2"
    assert theorem["magnetic_kernel_equality_all_unitary_characters"]
    assert theorem["number_of_positive_cosine_terms"]==6


def test_native_all_third_fourth_fifth_root_characters():
    cases=native_character_census()
    assert len(cases)==3
    for c,order in zip(cases,(3,4,5)):
        assert c["torsion_order"]==order
        assert c["characters"]==order**4
        assert c["repaired_rank_histogram"]=={
            "105":1,"108":order**4-1
        }
        assert c["same_ranks_as_full_six_loop"]


def test_certificate_uses_literal_repo_voltages_not_generic_geometry():
    c=make_certificate()
    assert c["schema"]=="w33.native.four_period.six_term_repair.v1"
    assert len(c["native_laurent_specializations"])==3
    assert "Lorentzian" in c["physics_boundary"]
