"""Round-ten W33 reproducibility suite: Frobenius, native chirality,
unrestricted SWAP budget, heralded double faults, actual plaquette Ward."""
import json,math
from pathlib import Path
import numpy as np
from analysis.w33_20261023_char2_allt_C_jordan import run as char2
from analysis.w33_20261023_native_full_qutrit_chirality import run as chirality
from analysis.w33_20261023_heralded_double_Z import run as magic
from analysis.w33_20261023_native_plaquette_ward import build as ward

ROOT=Path(__file__).resolve().parents[1]

def cert(name):
    return json.loads((ROOT/"data"/name).read_text(encoding="utf-8"))


def test_char2_frobenius_tensor_jordan_formula_and_GF16_control():
    x=char2()
    assert x["status"]=="ALL_CHARACTERISTIC_TWO_TRANSVECTION_C_JORDAN_THEOREM"
    for row in x["sample_q"]:
        q=row["q"]
        assert row["J1"]==q and row["J2"]==q*(q-1)//2
        assert row["Cdim"]==q*q
        assert row["rank_D_on_C"]==row["J2"]
    cases=cert("PART_20261023_GF16_FIRST_ORDER_OBSTRUCTION.json")["cases"]
    for case in cases:
        assert case["rankDC"]==case["q"]*(case["q"]-1)//2
        assert case["rank_delta1"]==0
    assert cases[-1]["n"]==4369


def test_full_9D_native_qutrit_parity_even_noncommuting_mixer():
    a=chirality()
    assert a["mixing_noncommutes_with_O"] and a["mixing_commutes_with_parity"]
    assert a["positive_negative_chirality_overlap_norm"]>1
    r=a["spectrum"]
    assert len(r)==8
    for h in (.05,.1,.2):
        first=next(x for x in r if x["mixing"]=="first_only" and x["h"]==h)
        full=next(x for x in r if x["mixing"]=="both_qutrits" and x["h"]==h)
        assert first["ground_degeneracy"]==4
        assert full["ground_degeneracy"]==1 and full["gap"]>0.009
    assert next(x for x in r if x["h"]==0)["ground_degeneracy"]==8


def test_four_layer_34_SWAP_unrestricted_solver_status_not_falsely_promoted():
    a=cert("PART_20261023_SWAPCOUNT_34_ROUND10.json")
    assert a["anchor"]==0 and a["depth"]==4
    assert a["swap_budget"]==34
    assert a["status"]=="UNKNOWN"
    assert a["proof_of_lower_bound_36"] is False
    assert a["branches"]>1e5
    # Existing certified four-layer 36 construction remains the upper bound,
    # and transposition parity gives >=28, NOT >=36.
    from analysis.w33_20261022_five_followups_round5 import routing_four_layers
    b=routing_four_layers()
    assert len(b["all_schedules"])==40
    assert sum(len(x) for x in b["all_schedules"][0]["layers"])==36


def test_integer_cyclotomic_exhaustive_780_double_Z_pairs():
    a=magic()
    assert a["all_double_site_pairs"]==780
    assert a["accepted_double_fault_pairs"]==6
    assert sorted(tuple(x["sites"]) for x in a["all_accepted_pairs"])==[
        (0,1),(0,2),(0,3),(1,2),(1,3),(2,3)]
    for x in a["all_accepted_pairs"]:
        assert math.isclose(x["success"],2/81,rel_tol=0,abs_tol=1e-11)
        assert math.isclose(x["fidelity"],1/58,rel_tol=0,abs_tol=1e-11)
        assert any(any(y!=0 for y in rem) for rem in x["Phi9_remainders"])
    assert math.isclose(a["P_success_series"]["quadratic"],2480/9,abs_tol=1e-10)
    assert math.isclose(a["conditional_fidelity_series"]["quadratic"],-14706/24389,abs_tol=1e-10)


def test_all_45_native_triangle_plaquettes_independent_gauge_exact():
    x=ward()
    assert x["vertices"]==27 and x["edges"]==135
    assert x["total_base_triangles"]==45
    assert x["contractible_zero_voltage_triangles"]==45
    assert x["all_edges_in_exactly_one_triangle"]
    assert x["triangles_per_vertex"]==5
    assert x["finite_2_complex_betti"]==[1,64,0]
    assert x["finite_2_complex_Euler_characteristic"]==-63
    seen=[a for z in x["closed_cycles"] for a in z["edge_ids"]]
    assert np.array_equal(np.bincount(seen,minlength=135),np.ones(135,dtype=int))
    assert [z["rank_grad"] for z in x["controls"]]==[26,27,27]
    assert all(z["rank_contractible_triangle_curl"]==45 for z in x["controls"])
    assert all(z["gauge_ward_max"]<1e-11 for z in x["controls"])


def test_native_zero_period_cycle_completion_is_exactly_four_dimensional():
    from analysis.w33_20261023_native_fourcycle_holonomy import run as four
    from analysis.w33_20261023_native_zero_holonomy_face_completion import run as allshort
    x=four()
    assert x["all_simple_fourcycles"]==1080
    assert x["zero_period_fourcycles"]==189
    assert x["rank_triangle_plus_zero_period_fourcycle_faces_mod3"]==101
    y=allshort()
    assert [(a["length"],a["zero_voltage_cycles"],a["cumulative_F3_face_rank"])
             for a in y["length_census"]]==[(3,45,45),(4,189,101),(5,1053,105)]
    assert y["resulting_h1"]==4
    assert len(y["independent_face_basis"])==105


def test_native_completed_Z3_CSS_has_four_logicals_and_distance_four():
    from analysis.w33_20261023_native_gq24_qutrit_gauge_code import run as triangle_code
    from analysis.w33_20261023_native_135_4_4_css import run as completed_code
    tri=triangle_code()
    assert tri["CSS_parameters"]=="[[135,64,2]]_3"
    a=completed_code()
    assert a["rank_HX"]==26 and a["rank_HZ"]==105
    assert a["logical_qutrits"]==4
    assert a["CSS_parameters"]=="[[135,4,4]]_3"
    assert a["X_logical_distance_lower_bound"]==4
    assert a["Z_logical_distance_exact"]==4
    assert a["rank_native_period_map_mod3"]==4
    assert a["independent_face_lengths"]=={"3":45,"4":56,"5":4}
    assert a["nonzero_4_period_mod3"]==[0,2,2,1]
