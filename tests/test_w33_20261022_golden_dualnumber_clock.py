"""Exact golden/supergolden-F3 and native W(3,9) dual-number clock regression."""
from analysis.w33_20261022_golden_dualnumber_clock import (
    matrix_conjugacy,field_change,native_golden_clock,
    w33_hybrid_and_complex_nogo,certificate)

def test_supergolden_golden_explicit_conjugator():
    r=matrix_conjugacy()
    assert r["determinant_Q_mod3"]==2
    assert r["supergolden_order_mod3"]==8
    assert r["golden_order_mod3"]==8

def test_golden_gaussian_GF9_isomorphism():
    r=field_change()
    assert r["phi_square_is_i"]
    assert r["phi_order"]==8
    assert r["exact_addition_multiplication_checks"]==162

def test_native_symplectic_W3_9_phi_clock():
    r=native_golden_clock()
    assert r["vertices"]==820 and r["nilpotent_rank"]==100
    assert r["free_rank"]==100
    assert r["simple_F9_modules"]==620
    assert r["field_model_graph_isomorphism"] is True
    assert r["clock_order"]==24

def test_W33_tensor_24clock_not_complex_unitary():
    r=w33_hybrid_and_complex_nogo()
    assert r["B_rank_over_F3"]==10
    assert r["order_mod3"]==24
    assert r["complex_lift_spectral_radius"]>45
    assert r["complex_lift_unitary"] is False

def test_research_scope_boundary():
    r=certificate()
    assert r["classical_RH_proved"] is False
    assert r["physical_photon_clock_constructed"] is False
    assert all(v["status"]=="PASS_EXACT" for v in r.values() if isinstance(v,dict))


def test_exceptional_prime5_gold_ramification_jordan_depth_three():
    from analysis.w33_20261022_gold_prime5_ramification import certificate as prime5
    r=prime5()
    assert r["status"]=="PASS_EXACT_MODULAR"
    assert r["Jordan_unipotent_blocks"]=={"J3":35,"J2":86,"J1":35}
    assert r["order_unscaled_U_mod5"]==20
    assert r["rank_M_squared"]==35
    assert r["tensor_nilpotency_index"]==3
    assert r["classical_RH_proved"] is False

def test_supergolden_discriminant_prime31_jordan_depth_three():
    from analysis.w33_20261022_supergolden_prime31 import certificate as prime31
    a=prime31()
    assert a["beta_discriminants"]=={"golden":5,"supergolden":-31}
    assert a["scalar_orders"]=={"root_10":15,"root_11":30}
    assert a["faithful_six_dimensional_tensor_order"]==930
    assert a["predicted_full_W3_31_dimension"]==92352
    assert a["predicted_full_Jordan_blocks"]["root_11_repeated_Jordan"]=={
        "J3":5456,"J2":19872,"J1":5456}
    assert a["classical_RH_proved"] is False


def test_generalized_pascal_beta_discriminant_family_and_null_prime():
    from analysis.w33_20261022_pascal_beta_discriminants import certificate as discriminants
    r=discriminants()
    assert r["status"]=="PASS_EXACT_SYMBOLIC"
    assert [v["discriminant"] for v in r["candidate_exceptional_characteristics"][:4]]==[5,-31,-283,3381]
    assert r["m5_sample_overlap"]["divisors"]==[3,7,23]
    assert r["m5_sample_overlap"]["Levi_family_nondivisor_control"]==43
    assert r["classical_RH_proved"] is False
