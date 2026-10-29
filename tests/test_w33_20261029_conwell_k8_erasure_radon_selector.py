"""W33 native Conwell graph, finite Radon and Grassmann corrections."""
from analysis.w33_20261029_conwell_k8_erasure_radon_selector import (
    graph, exact_erasure, syndrome_controls, finite_radon,
    a8_selector, sub_six_counterexample, exact_F3_lagrangian_code,
)

def test_conwell_eight_heptads_have_an_additive_K8_edge_model():
    points, owners, edges=graph()
    assert len(points)==28 and len(owners)==28 and len(edges)==28
    v=[0]+[edges[0,j] for j in range(1,8)]
    assert all(edges[i,j]==v[i]^v[j] for i,j in edges)

def test_exact_heralded_loss_enumerator_and_graph_circuits():
    c=exact_erasure()
    assert c['correctable_counts_size_0_through_6']==[1,28,378,3220,18760,73248,155456]
    assert c['uncorrectable_counts_size_0_through_6']==[0,0,0,56,1715,25032,221284]
    assert c['all_size_7_or_more_erasures_uncorrectable']
    assert c['weight3_logical_supports_graph_triangles']==56
    assert c['weight4_zero_syndrome_four_cycles']==210
    assert c['weight4_zero_syndrome_perfect_matchings']==105
    assert abs(c['independent_heralded_loss_success_probabilities']['0.05']-0.9910413781331214)<1e-12

def test_exact_single_pauli_syndrome_and_two_bit_error_collisions():
    c=syndrome_controls()
    assert c['single_X_Pauli_syndrome_equals_six_bit_Plucker_vector']
    assert c['two_X_errors_alias_single_X']==168
    assert c['two_X_errors_detectably_outside_single_lookup']==210
    assert c['minimal_stabilizer_rows']==[7,6]

def test_finite_Radon_incidence_kernel_cokernel():
    c=finite_radon()
    assert c['GF2_incidence_Radon_rank']==11
    assert c['kernel_dimension']==4 and c['cokernel_dimension']==24
    assert c['kernel_equals_four_linear_functions_on_F2_4']
    assert c['GL4_F2_generator_equivariance_count']==12

def test_A8_invariant_matter_selector_has_sectors_1_7_20():
    c=a8_selector()
    assert c['A8_invariant_quadratic_response_commutant_dim']==3
    assert c['mode_eigenvalues_and_multiplicities']=={
      'a+12*b+28*c':1,'a+4*b':7,'a-2*b':20
    }

def test_non_torsion_bloch_character_disproves_three_term_candidate():
    c=sub_six_counterexample()
    assert c['Q_zero_exact'] and c['all_three_added_harmonics_inactive']
    assert c['rejected_global_repair']
    assert c['restricted_torus_resultant']=='180*(Y-1)^6*(5*Y^2+4*Y+5)'

def test_ternary_W33_Lagrangian_Grassmann_distance_is_24_not_28():
    c=exact_F3_lagrangian_code()
    assert c['all_planes']==130 and c['totally_isotropic_planes']==40
    assert c['parameters']==[40,5,24]
    assert c['weight_enumerator']=={0:1,24:90,27:80,30:72}
    assert c['incorrect_legacy_distance_claim']==28
