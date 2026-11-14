"""E6 M/IIB branch-selection critical four-front regressions (2026-11-14)."""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"analysis"))
import toe_20261114_E6_ExFT_scalar_potential_isotropy_nogo as P
import toe_20261114_E6_M_IIB_9D_common4_incidence_noselector as B
import toe_20261114_E6_9D_flux_doublet_moduli_stabilizer as F
import toe_20261114_E6_flux_shape_volume_runaway_nogo as R

def test_exact_scalar_no_intrinsic_branch_preference():
    d=P.main()
    assert d["noncompact_coset_dimension"]==42
    assert d["full_coset_square_resolution"]=="14/9 I27"
    assert d["isotropic_unit_Hilbert_Schmidt_coset_average_per_unit_derivative"]=="5/216"
    assert d["anisotropic_V5_minus_V6_sign_hist"]["positive"]>0
    assert d["anisotropic_V5_minus_V6_sign_hist"]["negative"]>0
    assert d["common_four_anisotropic_scalar_potential_equal_cases"]==168

def test_1080_common_four_and_exact_gram_spectrum():
    d=B.main()
    assert d["incidence_edges"]==1080
    assert d["M_branch_interface_degree"]==15
    assert d["IIB_branch_interface_degree"]==5
    assert d["incidence_matrix_row_rank"]==72
    assert d["incidence_matrix_nullity_on_IIB_functions"]==144
    assert d["M_M_incidence_Gram_exact_eigen_census"]=={"3":15,"9":30,"21":20,"45":6,"75":1}
    assert d["incidence_random_walk_stationary_branch_masses"]=={"M6":"1/2","IIB5":"1/2"}

def test_duality_covariant_flux_shape():
    d=F.main()
    assert d["exact_SL2Z_duality_invariance_checks"]==450
    assert d["isolated_interior_shape_minimum_iff_flux_doublet_rank_two"]
    assert d["square_hex_and_runaway_examples"]["square"]["tau_star"]=="I"
    assert d["square_hex_and_runaway_examples"]["hexagonal"]["D"]==3
    assert d["square_hex_and_runaway_examples"]["rank_one_runaway"]["has_finite_minimum"]==False

def test_finite_shape_but_unstabilized_Einstein_volume():
    d=R.main()
    assert d["external_dimension"]==5
    assert d["Einstein_frame_total_radius_power"]=="-26/3"
    assert d["no_simultaneous_finite_volume_and_shape_critical_point"]
    assert d["original_E6_section_selector_status"]=="NOT OBTAINED"

if __name__=="__main__":
    fs=[test_exact_scalar_no_intrinsic_branch_preference,
        test_1080_common_four_and_exact_gram_spectrum,
        test_duality_covariant_flux_shape,
        test_finite_shape_but_unstabilized_Einstein_volume]
    for f in fs:
        f()
        print("PASS",f.__name__,flush=True)
    print("PASS",len(fs),"/",len(fs),flush=True)
