"""Regression for exact 21-even, 33-total and 47-erasure E6 Pauli readouts."""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"analysis"))
import toe_20261114_E6_180charge_minimal_even_readout as E
import toe_20261114_E6_full_unknown_charge_twistor_decoder as F
import toe_20261114_E6_47axis_erasure_robust_readout as R

def test_optimal21_charge_menu():
    a=E.main()
    assert a["status"]=="PASS_OPTIMAL_21_OF_27_E6_CHARGE_READOUT_AND_ERASURE_NO_GO"
    assert a["optimal_even_observables_required"]==21
    assert a["optimal_fixed_charge_readout_menu_count"]==72
    assert a["single_any_axis_failure_optimal_even_menu_size"]==27
    assert a["adaptive_greedy_axis_queries_expected"]==8
    assert a["adaptive_greedy_axis_queries_worst"]==14

def test_full_unknown_charge_180_fibers():
    a=F.main()
    assert a["charge_fibers"]==180
    assert a["random_pure_state_reconstructions"]==720
    assert a["menu_total"]==33
    assert a["per_state_nonadaptive_full_settings"]==24
    assert a["ideal_greedy_per_state_expected_full_settings"]==11
    assert a["pure_state_max_matrix_error"]<1e-12
    assert a["noisy_charge_classification"]["0.8"]["empirical_accuracy"]>.95

def test_any_one_failed_axis_full_180_fibers():
    a=R.main()
    assert a["status"]=="PASS_47_GLOBAL_AXES_ANY_ONE_SENSOR_ERASURE_FULL_180_FIBER_TOMOGRAPHY"
    assert a["global_installed_axes_total"]==47
    assert a["failed_global_sensor_cases"]==47
    assert a["full_state_reconstructions_under_axis_failure"]==47*180
    assert a["minimal_odd_two_cover_verified_CPSAT_no19"]
    assert a["selected_total_observables_per_state"]==24
    assert a["max_density_matrix_reconstruction_residual"]<1e-12

if __name__=="__main__":
    funcs=[test_optimal21_charge_menu,test_full_unknown_charge_180_fibers,
           test_any_one_failed_axis_full_180_fibers]
    for fn in funcs:
        fn()
        print("PASS",fn.__name__,flush=True)
    print("PASS",len(funcs),"/",len(funcs),flush=True)
