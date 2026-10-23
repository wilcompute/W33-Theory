"""Research firewall regression for five independent W33 TOE frontiers."""
import math
from analysis.w33_20261022_five_toe_frontiers import (
    stabilizer_jordan, anchored_clock_selection, physical_routes,
    nine_root_phase_nogo, continuum_fixed_characteristic
)


def test_all_prime_stabilizer_jordan_module():
    cert=stabilizer_jordan()
    assert cert["status"]=="THEOREM_C_MODULE_LOGICAL_Q_OPEN"
    for x in cert["finite_regressions"]:
        p=x["p"]
        assert x["C_dimension"]==math.comb(p+2,3)
        assert len(x["rank_powers"])==p+1
        assert x["rank_powers"][-1]==0
        assert x["jordan_blocks"]=={str(j):p-j+1 for j in range(1,p+1)}


def test_clock_spontaneous_versus_ensemble_firewall():
    x=anchored_clock_selection()
    assert x["projective_minima"]==40
    assert "4a+2gamma" in x["tangent_Hessian"]
    assert x["minimizers"].startswith("{+e_i,-e_i")
    assert "1/40" in x["finite_temperature_exact"]
    assert x["numerical_nonviolations"]==1000


def test_clifford_routing_on_actual_B_couplers():
    x=physical_routes()
    assert x["transvections_certified"]==40
    assert x["each_transvection"]["triangles"]==9
    assert x["each_transvection"]["parallel_layers"]==2
    assert x["each_transvection"]["swap_gates"]==18
    assert x["A_coupler_pair_within_any_moving_cycle"] is False
    assert x["physical_device_assumed"] is False
    assert x["distinct_B_edges_exercised"]==540
    assert x["edge_anchor_multiplicities"]=={2:540}


def test_exhaustive_ninth_root_logical_coset_leakage():
    x=nine_root_phase_nogo()
    assert x["all_stabilizer_codewords"]==3**10
    assert x["zero_logical_phase_distribution_mod9"]=={"0":59049}
    assert x["logical_coset_u_support"]==[0,1,2,3]
    assert x["relative_phase_distribution_mod9"]=={"0":19683,"3":13122,"6":26244}
    assert x["code_projector_survival_probability"]=="1/27"
    assert x["encoded_non_clifford_unitary_obtained"] is False


def test_fixed_prime_continuum_no_go_scope():
    r=continuum_fixed_characteristic()
    assert len(r["cases"])==12
    for case in r["cases"]:
        p,q=case["p"],case["q"]
        assert case["anchor_perturbation_distinct_eigenvalue_upper_bound"]==p+2
        assert sum(case["multiplicities"])+1==case["n"]
        assert case["normalized_laplacian_nonzero_eigenvalues"][0] < 1
        assert case["normalized_laplacian_nonzero_eigenvalues"][1] > 1
    assert "not a proof against" in r["no_go"].lower()
