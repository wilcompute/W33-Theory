"""Five independent research fronts + strict scope-limited regressions."""
from __future__ import annotations
import sys
from pathlib import Path
import pytest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
@pytest.fixture(scope="module")
def vacuum():
    from w33_20261019_round8_clifford_vacuum_orbit import orbit
    return orbit()
@pytest.fixture(scope="module")
def phase():
    from w33_20261019_round8_exact_local_instability import run
    return run()
def test_full_1440_clifford_real_structure_vacuum_orbit(vacuum):
    assert vacuum["all_checks_pass"]
    assert vacuum["orbit_size"]==1440
    assert vacuum["stabilizer_order"]==2916
    assert vacuum["stabilizer_pauli_translation_order"]==9
def test_exact_one_sided_T_positive_global_noncommutation_phase_exclusion(phase):
    assert phase["all_checks_pass"]
    assert abs(phase["T_point5_refined_noncommuting_exclusion_kappa_below"]+.3402395316212)<1e-11
    assert all(abs(r["directional_total_prime_at_kappa_critical"])<1e-11 for r in phase["temperature_rows"])
def test_fixed_rational_seven_rate_competitor(phase):
    a=phase["rational_seven_mass_witness"]
    assert a["seven_rational_weights"].count("1/60")==6
    assert a["seven_rational_weights"].count("9/10")==1
    assert a["gap_below_single_at_minus_035"]<-.0005
def test_five_heptad_numerical_stationarity_and_feasible_optimized_candidates():
    from w33_20261019_round8_phase_stationarity import run
    d=run()
    assert d["all_checks_pass"]
    assert all(not x["equal_weights_stationary_inside_seven_simplex"] for x in d["five_family_stationarity"])
def test_all_trinification_cartan_anomaly_coefficients():
    from w33_20261019_round8_matter_anomaly_cartan import run
    d=run()
    assert d["all_checks_pass"]
    assert d["SU2_L_Weyl_doublet_multiplicity"]==d["SU2_R_Weyl_doublet_multiplicity"]==6
    assert all(v==0 for v in d["nonabelian_squared_abelian_anomaly_coefficients"].values())
def test_optical_crosstalk_breaks_naive_visibility_but_transfer_matrix_recovers():
    from w33_20261019_round8_optics_crosstalk_tomography import run
    d=run()
    assert d["all_checks_pass"]
    assert max(abs(x["diagonal_reference_only_bias"]) for x in d["mode_mixing_series"])>.01
    assert max(x["full_matrix_reconstruction_error"] for x in d["mode_mixing_series"])<1e-12
def test_uv_equal_g_but_unequal_thresholds_preclude_fixed_mass_ratio():
    from w33_20261019_round8_rg_threshold_nogo import run
    d=run()
    assert d["all_checks_pass"]
    assert abs(d["two_sector_threshold_ratio"]-12.3284673944)<1e-9
