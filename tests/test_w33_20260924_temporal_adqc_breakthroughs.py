import json
import subprocess
import sys
from pathlib import Path

import pytest

ROOT=Path(__file__).resolve().parents[1]

SCRIPTS=[
    "w33_20260924_bell_shell_quadratic_history_intertwiner.py",
    "w33_20260924_temporal_quantum_memory_witness.py",
    "w33_20260924_modular_a2_event_clock.py",
    "w33_20260924_intrinsic_transpose_outer.py",
    "w33_20260924_liouville_swap_cp_outer_bridge.py",
    "w33_20260924_adqc_record_arrow.py",
    "w33_20260924_bell_shell_clifford_cyclotomic_lift.py",
]


@pytest.mark.parametrize("name",SCRIPTS)
def test_producers_replay(name):
    subprocess.run(
        [sys.executable,str(ROOT/"analysis"/name)],
        cwd=ROOT,check=True,capture_output=True,text=True,
        timeout=40,
    )


def load(name):
    return json.loads((ROOT/"data"/name).read_text(encoding="utf-8"))


def test_quadratic_history_intertwiner():
    c=load("w33_20260924_bell_shell_quadratic_history_intertwiner.json")
    assert c["status"]=="PASS_BELL_SHELL_QUADRATIC_HISTORY_INTERTWINER"
    assert c["checks"]["orbit_census_1_8_6_12"]==[1,8,6,12]
    assert c["checks"]["Bell_S4_image_order"]==24


def test_quantum_temporal_memory_boundary():
    c=load("w33_20260924_temporal_quantum_memory_witness.json")
    assert c["coherent_memory"]["negativity"]>0.999999
    assert c["classical_label_memory"]["negativity"]==0.0
    assert c["depolarizing_memory"]["recovered_channel_entanglement_breaking_boundary"]=="p=3/4"


def test_modular_clock_and_transpose_outer():
    c=load("w33_20260924_modular_a2_event_clock.json")
    assert c["A2_weyl_bridge"]["group_order"]==6
    assert c["relational_history"]["stationarity_error"]<1e-12
    o=load("w33_20260924_intrinsic_transpose_outer.json")
    assert o["status"]=="PASS_INTRINSIC_QUTRIT_TRANSPOSE_IS_BT172_OUTER_CLASS"
    assert o["centerquad_45_action"]["PSp_conjugate"] is True
    l=load("w33_20260924_liouville_swap_cp_outer_bridge.json")
    assert l["status"]=="PASS_LIOUVILLE_SWAP_IS_INTRINSIC_W33_TEMPORAL_OUTER"
    assert l["reversal"]["fixed_lines"]==2


def test_record_arrow_and_cyclotomic_boundary():
    c=load("w33_20260924_adqc_record_arrow.json")
    assert c["status"]=="PASS_REVERSIBLE_LOGICAL_UPDATE_WITH_CLASSICAL_RECORD_ARROW"
    assert abs(c["exact_gate_fact"]["branch_entropy_bits"]-1.584962500721156)<1e-12
    assert max(
        x["corrected_channel_error"]
        for x in c["exact_gate_fact"]["random_density_trials"]
    )<2e-12

    q=load("w33_20260924_bell_shell_clifford_cyclotomic_lift.json")
    assert q["status"]=="PASS_BELL_SHELL_IS_QUADRATIC_CLIFFORD_AND_T_IS_MU9_LIFT"
    assert q["bell_shell_quadratic_group"]["order"]==27
    assert q["nonclifford_lift"]["T1_is_Clifford"] is False


def test_f4_fold_is_rejected_by_actual_centralizer():
    c=load("w33_20260924_temporal_f4_fold_probe.json")
    assert c["full_centralizer_order"]==96
    assert c["centralizer_image_on_26_order"]==48
    assert sorted(c["centralizer_orbits_on_26"])==[1,3,4,6,12]
