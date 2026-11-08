"""Exact odd-prime Gaussian compiler, generalized Clifford and routing-limit checks."""
import importlib.util,math
from pathlib import Path
import pytest
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("odd_prime_clifford",
        ROOT/"analysis/w33_20261108_odd_prime_clifford_compiler.py")
M=importlib.util.module_from_spec(spec);spec.loader.exec_module(M)

@pytest.fixture(scope="module")
def cert():return M.produce()

@pytest.mark.parametrize("p",[3,5,7,11,13,17])
def test_three_qupit_quadratic_factorization_all_displacement_types(cert,p):
    d=next(x for x in cert["cases"] if x["prime"]==p)
    assert d["rails"]==p**3
    assert d["full_kernel_difference_type_count"]==p**3
    assert d["full_kernel_from_factorization_max_residual"]<1e-12
    assert d["sample_pair_max_residual"]<1e-12

@pytest.mark.parametrize("p",[3,5,7,11,13,17])
def test_gaussian_ports_are_unitary_and_clifford(cert,p):
    d=next(x for x in cert["cases"] if x["prime"]==p)
    for port in d["quadratic_port_gates"]:
        assert port["gaussian_port_unitarity_error"]<1e-12
        assert port["quadratic_phase_Fourier_factorization_error"]<1e-12
    for gates in d["local_port_Pauli_normalizer_certificates"].values():
        assert [g["generator"] for g in gates]==["X","Z"]
        assert all(g["max_matrix_residual"]<1e-11 for g in gates)

@pytest.mark.parametrize("p",[3,5,7,11,13,17])
def test_gate_counts_and_rail_complexities(cert,p):
    d=next(x for x in cert["cases"] if x["prime"]==p)
    assert d["logical_SUM_count"]==4
    assert d["local_one_qupit_Gauss_gate_count"]==3
    assert d["if_expanded_local_quadratic_phase_gates"]==6
    assert d["if_expanded_local_Fourier_gates"]==3
    assert d["independent_rail_p_port_Gauss_units"]==3*p*p
    assert d["internal_generic_two_mode_upper_bound_without_routing"]==3*p*p*(p*(p-1)//2)
    assert d["generic_n_rail_mesh_two_mode_bound"]==p**3*(p**3-1)//2

def test_only_p3_drops_local_scaling_and_recovers_prior_compiler(cert):
    assert [(x["prime"],x["nontrivial_local_multipliers"]) for x in cert["cases"]]==[
         (3,0),(5,2),(7,2),(11,2),(13,2),(17,2)]
    assert cert["cases"][0]["independent_rail_p_port_Gauss_units"]==27
    assert cert["cases"][0]["internal_generic_two_mode_upper_bound_without_routing"]==81

def test_p5_125_mode_savings_are_logic_not_chip(cert):
    p5=cert["cases"][1]
    assert p5["rails"]==125 and p5["independent_rail_p_port_Gauss_units"]==75
    assert p5["internal_generic_two_mode_upper_bound_without_routing"]==750
    assert p5["generic_n_rail_mesh_two_mode_bound"]==7750
    assert p5["internal_upper_to_generic_mesh_ratio"]==pytest.approx(750/7750)

def test_finite_field_coordinate_map_inverse_explicitly():
    for p in [3,5,7]:
        for a in range(p):
            assert M.coordinates(p,(a,0,0))[0]==(a*pow(2,-1,p))%p

def test_stabilizer_gate_is_not_a_universal_toe(cert):
    assert "not universal quantum computation by itself" in cert["physics_limit"]
    assert "previously-owned" in cert["p3_special"]
    assert "finite-field arithmetic" in cert["fixed_prime_test_scope"]
