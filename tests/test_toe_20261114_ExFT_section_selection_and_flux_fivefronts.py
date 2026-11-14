"""Exact ExFT scalar-potential, M/IIB interface, flux and systematic regressions."""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"analysis"))
import toe_20261114_E6_ExFT_scalar_potential_isotropy_nogo as V
import toe_20261114_E6_M_IIB_9D_common4_incidence_noselector as B
import toe_20261114_E6_9D_flux_doublet_moduli_stabilizer as F
import toe_20261114_HP3_witness_calibration_and_axis_systematic as N

def test_published_ExFT_potential_exact_scalar_isotropy_nogo():
    a=V.main()
    assert a["status"]=="PASS_EXACT_E6_EXFT_SCALAR_POTENTIAL_ISOTROPIC_BRANCH_NO_GO"
    assert a["full_coset_square_resolution"]=="14/9 I27"
    assert a["isotropic_unit_Hilbert_Schmidt_coset_average_per_unit_derivative"]=="5/216"
    assert a["common_four_anisotropic_scalar_potential_equal_cases"]==168
    assert a["anisotropic_V5_minus_V6_sign_hist"]["positive"]>0
    assert a["anisotropic_V5_minus_V6_sign_hist"]["negative"]>0

def test_1080_M_IIB_four_space_correspondence_exact_spectrum():
    a=B.main()
    assert a["status"].startswith("PASS_E6_1080_")
    assert a["shared_coordinate_four_spaces"]==1080
    assert a["incidence_edges"]==1080
    assert a["M_branch_interface_degree"]==15 and a["IIB_branch_interface_degree"]==5
    assert a["M_M_incidence_Gram_exact_eigen_census"]=={"3":15,"9":30,"21":20,"45":6,"75":1}
    assert a["incidence_matrix_nullity_on_IIB_functions"]==144
    assert a["naive_equal_section_prior"]!=a["incidence_random_walk_stationary_branch_masses"]

def test_genuine_SL2Z_flux_kinetic_conditional_shape_stabilization():
    a=F.main()
    assert a["status"]=="PASS_EXACT_9D_M_IIB_FLUX_SHAPE_MINIMUM_SL2Z_DUALITY"
    assert a["exact_SL2Z_duality_invariance_checks"]==450
    assert a["isolated_interior_shape_minimum_iff_flux_doublet_rank_two"]
    assert a["zero_flux_has_flat_moduli_no_isolated_minimum"]
    assert a["square_hex_and_runaway_examples"]["hexagonal"]["D"]==3
    assert a["square_hex_and_runaway_examples"]["rank_one_runaway"]["D"]==0

def test_orthogonal_four_copy_and_correlated_readout_falsifiers():
    a=N.main()
    assert a["status"].startswith("PASS_HP3_FOURCOPY_")
    assert .128<a["critical_absolute_visibility_uncertainty_at_eta08"]<.129
    assert a["all_single_axis_sign_inversion_cases"]==72*21
    assert a["exact_axis_inversion_alias_count_histogram"]=={"8":1080,"20":432}
    assert a["MUB_CaDiCaL_exclusion_status"]=="UNDECIDED_BOUNDED_CONFLICTS"

if __name__=="__main__":
    tests=[globals()[n] for n in sorted(globals()) if n.startswith("test_")]
    for fn in tests:
        fn()
        print("PASS",fn.__name__,flush=True)
    print("PASS",len(tests),"/",len(tests),flush=True)
