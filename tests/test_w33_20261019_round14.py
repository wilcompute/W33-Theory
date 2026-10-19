"""Round14 independent five-front regression and falsification checks."""
from __future__ import annotations
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
def test_pair_current_mediator_has_derived_negative_bounded_mixed_effect():
    from w33_20261019_round14_pair_current_mediator import run
    a=run()
    assert a["all_checks_pass"]
    assert len(a["pair_classes"])==17 and len(a["M2_interaction_blocks"])==3
    assert a["example_balanced_two_vacua_Veff_at_g2_over_m2_eq1"].startswith("-")
def test_contiguous_0p95_to_1p30_phase_band_strictly_certified():
    from w33_20261019_round14_phase_grid_certificate import main
    a=main()
    assert a["all_checks_pass"]
    assert a["grid_subintervals"]==1750 and a["T_interval"]==["19/20","13/10"]
    assert a["minimum_proved_energy_advantage_over_entire_band_float"]>.00017
def test_all_40_D5_CAR_generators_but_cubic_incompatibility_flagged():
    from w33_20261019_round14_so10_chevalley_transport import run
    a=run()
    assert a["all_checks_pass"]
    assert len(a["root_labels"])==40
    assert a["first_four_naively_embedded_generators_fail_E6_cubic_lie_invariance"]==[True]*4
def test_19channel_calibration_response_and_deadtime():
    from w33_20261019_round14_optical_calibration_matrix import run
    a=run()
    assert a["all_checks_pass"]
    assert len(a["synthetic_assumed_response"]["rows_19x19"])==19
    assert a["synthetic_assumed_response"]["condition_number"]<2.2
    assert a["assumed_rate"]["deadtime_scenarios"][1]["fractional_loss_single_hot_port"]>.047
def test_three_generation_flux_index_obeys_anomaly_firewall():
    from w33_20261019_round14_magnetic_three_generation import run
    a=run()
    assert a["all_checks_pass"]
    assert a["case_internal_E6_U1_flux"]["net_chiral_indices"]==[3,-6,12]
    assert a["case_external_uniform_U1F_flux"]["net_chiral_indices"]==[3,3,3]
    assert all(z==0 for z in a["case_external_uniform_U1F_flux"]["4D_SO10_U1_anomalies"].values())
