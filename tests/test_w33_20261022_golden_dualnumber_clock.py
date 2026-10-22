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
