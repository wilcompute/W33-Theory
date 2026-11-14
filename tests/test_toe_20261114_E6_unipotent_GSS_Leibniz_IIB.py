"""Exact E6 unipotent generalized-frame flux, Leibniz ideal and IIB wedge regression."""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"analysis"))
import toe_20261114_E6_unipotent_GSS_local_parallelization as F
import toe_20261114_E6_GSS_nilpotent_flux_monodromy_sections as A

def test_nonzero_constant_27D_generalized_frame_flux():
    r=F.main()
    assert r["status"]=="PASS_NONZERO_LOCAL_E6_GENERALIZED_FRAME_FLUX"
    c=r["candidate"]
    assert c is not None
    assert (c["root_index"],c["coordinate_index"])==(1,3)
    assert c["nonzero_flux_components"]==30
    assert len(c["root_sparse"])==6
    assert c["X_tensor_sha256"]=="0ebafd8592edb79c7045c499197eba8f4b51b7920f856370674c689f4b4a6fc5"
    assert c["complete_integer_leibniz_identity"]
    assert c["all_sampled_polynomial_coefficients_constant"]
    assert all(v==0 for v in c["trace_X_AB_B"])
    assert c["simultaneous_shared_four_M_IIB_single_coordinate"]

def test_exact_27D_Leibniz_ideal_25D_Lie_quotient_and_monodromy():
    r=A.main()
    assert r["status"]=="PASS_E6_GSS_TWO_STEP_LEIBNIZ_FREE5_LIE_QUOTIENT_MONODROMY"
    assert r["constant_generalized_structure_coefficient_nnz"]==30
    assert r["ordinary_antisymmetric_Lie_bracket"] is False
    assert r["exact_Leibniz_residual_zero"]
    assert r["two_step_nilpotent_Leibniz"]
    assert r["symmetric_trivial_ideal_rational_dim"]==2
    assert r["full_product_image_rational_dim"]==12
    assert r["left_annihilator_dim"]==22
    assert r["right_annihilator_dim"]==12
    assert (r["lie_quotient_dim"],r["lie_quotient_derived_dim"],r["lie_quotient_center_dim"])==(25,10,20)
    assert r["lie_quotient_is_free_two_step_on_five_plus_10_central"]
    wedge=r["explicit_wedge2_five_to_derived_ten_dictionary"]
    assert len(wedge)==10 and len({u["derived_coordinate"] for u in wedge})==10
    P=r["candidate_IIB_5_10_10_2_partition"]
    assert [len(P[k]) for k in P]==[5,10,10,2]
    assert P["five_section_generators"]==[0,1,2,3,4]
    assert P["two_symmetric_ideal_coordinates"]==[25,26]
    C=r["fixed_max_coordinate_sections_by_monodromy"]
    assert C["5"]["primal"]==141 and C["6"]["primal"]==51
    assert C["5"]["dual"]==141 and C["6"]["dual"]==51
    assert C["5"]["primal_contain_base_j"]==27
    assert C["6"]["primal_contain_base_j"]==12
    assert r["monodromy_infinite_order"]
    assert r["IIB_intertwiner_to_GL5_times_SL2_not_yet_constructed"]

if __name__=="__main__":
    fns=(test_nonzero_constant_27D_generalized_frame_flux,
         test_exact_27D_Leibniz_ideal_25D_Lie_quotient_and_monodromy)
    for f in fns:
        f()
        print("PASS",f.__name__,flush=True)
    print("PASS",len(fns),"/",len(fns),flush=True)
