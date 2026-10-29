"""Exact controls for five independent W33/TOE fronts."""
from analysis.w33_20261028_round12_five_frontiers import (
    matter_response,torus_grid,rotor_exact,parity_gluing,
    root_intertwiner_falsifier,one_term_exact_falsifier,
)


def test_E6_species_response_falsifies_unconditional_5_3():
    c=matter_response()
    assert c["equal_kernel_quadratic_trace"]==[[120,0],[0,72]]
    assert c["eta_1_response"]==[[130,10],[10,82]]
    assert c["eta_1_diagonal_ratio"]=="65/41"


def test_exact_ternary_Bloch_grid_and_finite_prime_artifact():
    c=torus_grid()
    assert c["order_three_character_count"]==81
    assert len(c["two_prime_controls"])==2
    for sample in c["two_prime_controls"]:
        assert sample["histogram"]=={"105":1,"107":10,"108":70}
        assert len(sample["exception_exponents"])==10
        assert sample["one_cosine_repairs_every_third_root_defect"] is True
    assert [t["mixed_rank"] for t in c["order_five_bad_prime_control"]]==[107,108,108]
    assert "No continuous Brillouin-torus" in c["critical"]


def test_rigorous_infinite_flux_three_rotor_ground_energy():
    c=rotor_exact()
    assert c["G_minus_7I_leading_minors"]==[787,10041,335]
    assert c["smallest_nonzero_integer_flux_norm_squared"]==22
    assert c["global_integer_minimizers"]==[[0,-1,0],[0,1,0]]
    assert c["potential_weight_sum"]=="7009/28125"
    assert c["coupling_vector_norm_squared"]=="297803260427/44651250000000"
    assert 0.2190<c["lower_bound_numeric_for_exact_algebraic_formula"]<0.2191
    assert c["upper_bound_exact"]=="7009/28125"


def test_parity_integer_lattice_index_two():
    c=parity_gluing()
    assert c["stacked_integer_basis_det"]==-2
    assert c["quotient"]=="Z^4/(Lambda_even+Lambda_odd) = Z/2"
    assert c["odd_norm_squared"]==18
    assert c["even_gram"]==[[10,0,-6],[0,12,-6],[-6,-6,12]]


def test_H4_E6_direct_root_embedding_no_go_and_Smith_trace():
    c=root_intertwiner_falsifier()
    assert c["H4_Weyl_order"]==14400 and c["E6_Weyl_order"]==51840
    assert c["Lagrange_no_full_Weyl_group_embedding"]
    assert c["Lagrange_no_rotation_subgroup_embedding"]
    assert c["charge_trace_determinant"]==8640
    assert c["charge_trace_Smith_invariants"]==[24,360]
    assert c["rebased_trace"]==[[120,120],[120,192]]

def test_exact_unitary_one_term_falsifier_outside_third_root_grid():
    c=one_term_exact_falsifier()
    assert c["Q_equals_zero_exact"]
    assert c["translation_e0_plus_e3_factor_equals_one_exact"]
    assert c["full_unrepaired_magnetic_rank"]==107
    assert c["single_cosine_magnetic_rank"]==107
    assert c["full_six_commutator_rank"]==108

