"""Exact E6 IIB Levi intertwiner, 351 gauging and parabolic stabilizer."""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"analysis"))
import toe_20261114_E6_exact_IIB_Levi_signed_tensor_intertwiner as I
import toe_20261114_E6_GSS_351_embedding_tensor as E
import toe_20261114_E6_GSS_351_flux_parabolic_stabilizer as P
import toe_20261114_E6_unipotent_GSS_local_parallelization as L
import toe_20261114_E6_GSS_nilpotent_flux_monodromy_sections as Q

def test_native_signed_cubic_full_IIB_Levi():
    z=I.main()
    assert z["status"]=="PASS_EXACT_NATIVE_SIGNED_E6_CUBIC_IIB_28D_LEVI_INTERTWINER"
    assert z["native_signed_terms_verified"]==45
    assert z["native_cubic_type_count"]=={"VZZ":15,"WWZ":20,"VWS":10}
    assert z["roots_by_GL1_grade"]=={"-6":5,"-3":20,"0":22,"3":20,"6":5}
    assert z["exact_sl5_block_action_on_V_W_W_Z_S"]
    assert z["exact_sl5_bracket_reconstruction_checks"]==576
    assert z["Levi_sl5_sl2_gl1_dimension"]==28

def test_exact_rank_two_351_embedding_linear_and_quadratic():
    z=E.main()
    assert z["status"]=="PASS_EXACT_E6_SPLIT_351_LINEAR_QUADRATIC_RANK2_Z_GAUGING"
    assert z["antisymmetric_Zraw_nonzero"]==[[25,26,10],[26,25,-10]]
    assert z["antisymmetric_Zraw_rank"]==2
    assert z["linear_constraint_residual_nnz"]==0
    assert z["quadratic_gauge_closure_residual_nnz"]==0
    assert z["active_gauge_generator_count"]==5
    assert z["Z_invariant_under_gauge"] and z["trace_trombone_zero"]

def test_52D_exact_351_stabilizer_parabolic_relative_invariant():
    z=P.main()
    assert z["status"]=="PASS_EXACT_E6_351_GSS_FLUX_52D_OPPOSITE_PARABOLIC_STABILIZER"
    assert z["rank_of_linear_E6_action_on_embedding_tensor"]==26
    assert z["exact_stabilizer_dimension"]==52
    assert z["full_IIB_dual_five_section_opposite_parabolic_dim"]==53
    assert z["GL1_flux_relative_weight"]==-10
    assert z["radical_190_minus3_pair_commutators_checked"]==190
    assert z["radical_derived_algebra_exact_rank"]==5

def test_prior_local_GSS_flux_and_Leibniz_are_preserved():
    frame=L.main()
    quotient=Q.main()
    assert frame["status"]=="PASS_NONZERO_LOCAL_E6_GENERALIZED_FRAME_FLUX"
    assert quotient["status"]=="PASS_E6_GSS_TWO_STEP_LEIBNIZ_FREE5_LIE_QUOTIENT_MONODROMY"
    assert quotient["full_product_image_rational_dim"]==12

if __name__=="__main__":
    seq=[test_native_signed_cubic_full_IIB_Levi,
         test_exact_rank_two_351_embedding_linear_and_quadratic,
         test_52D_exact_351_stabilizer_parabolic_relative_invariant,
         test_prior_local_GSS_flux_and_Leibniz_are_preserved]
    for fn in seq:
        fn()
        print("PASS",fn.__name__,flush=True)
    print("PASS",len(seq),"/",len(seq),flush=True)
