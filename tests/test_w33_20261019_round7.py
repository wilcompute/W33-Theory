"""Round7 physically scoped W33 independent reproducibility checks."""
from __future__ import annotations
import sys
from pathlib import Path
import pytest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))

@pytest.fixture(scope="module")
def e8real():
    from w33_20261019_round7_e8m24_involution import check
    return check()

@pytest.fixture(scope="module")
def matter():
    from w33_20261019_round7_matter_rg import calc
    return calc()

def test_E8minus24_involution_lie_bracket_and_signature(e8real):
    assert e8real["all_checks_pass"]
    assert e8real["theta_graded_248_dimensions"]["compact_plus"]==136
    assert e8real["theta_graded_248_dimensions"]["noncompact_minus"]==112
    assert e8real["max_numeric_bracket_realstructure_residual"]<1e-10

def test_clifford_subgroup_not_whole_physical_real_form(e8real):
    r=e8real["five_Clifford_generator_real_structure_screen"]
    assert {k for k,v in r.items() if v["preserves_this_E8m24_fixed_real_structure"]}=={"S1","CZ"}
    assert all(v["D_commutation_residual"]>1 for k,v in r.items() if k not in {"S1","CZ"})

def test_global_full120_negative_interaction_exclusion():
    from w33_20261019_round7_competing_phase import run
    r=run()
    assert r["all_checks_pass"]
    h=next(x for x in r["T_data"] if x["T"]==.5)
    assert h["global_single_guaranteed_if_kappa_at_least"]<0
    assert h["single_tick_excluded_if_kappa_strictly_below"]<h["global_single_guaranteed_if_kappa_at_least"]

def test_18mode_synthetic_mode_resolved_calibration_and_shams():
    from w33_20261019_round7_optical_mode_loss import run
    r=run()
    assert r["all_checks_pass"]
    assert abs(r["mode_by_mode_corrected_deficit"]-8/27)<1e-12
    assert abs(r["global_calibration_bias"])>.005
    assert r["shot_statistics"]["total_photons_per_repetition"]==94500

def test_anomaly_safe_chiral_trinification_and_SU9_caveat(matter):
    assert matter["all_checks_pass"]
    assert all(x["total"]==0 for x in matter["local_SU3_cubic_anomalies"].values())
    assert all(v["effective_Dirac_flavors"]==3 for v in matter["one_loop_flavor_count_and_beta"].values())

def test_one_loop_conditional_dimensional_transmutation(matter):
    x=matter["conditional_transmutation_examples"]
    assert len(x)==3
    assert x[0]["Lambda_one_loop_GeV"]<x[1]["Lambda_one_loop_GeV"]<x[2]["Lambda_one_loop_GeV"]
    assert max(q["relative_RG_invariant_error"] for q in matter["RG_invariant_check"])<1e-12
