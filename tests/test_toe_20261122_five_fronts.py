"""Five independent TOE falsifier/frontier regression families (2026-11-22).

No experimental Standard Model or quantum-gravity assertion is part of these tests.
"""
from __future__ import annotations
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"analysis"))

import toe_20261122_discrete_witting_dense_su4 as gates
import toe_20261122_h27_central_fourier_bridge as h27
import toe_20261122_causal_orientation_no_go as causal
import toe_20261122_optical_control_resources as optics
import toe_20261122_e6_h27_chirality_gate as matter

def test_discrete_gate_adjoint_six_primes():
    d=gates.verify()
    assert d["commutant_over_complex_dimension"]==1
    assert len(d["finite_field_certificates"])==6
    assert all(x["commutant_equation_ranks"]==[126,200,221,224] for x in d["finite_field_certificates"])

def test_discrete_gate_trace_integrality_negative_control():
    d=gates.verify()
    assert d["product_trace"]=="(5+omega)/3; omega^2+omega+1=0"
    assert d["determinant_group"]=="mu6"
    assert d["full_closure"]=="{U in U(4):det(U) in mu6}"

def test_H27_center_fibers_on_actual_witting_rays():
    d=h27.verify()
    assert len(d["center_cycles"])==9
    assert all(len(c)==3 for c in d["center_cycles"])
    assert d["regular_address_order"]==27
    assert d["center_trace_on_address27"]==0

def test_H27_operator_vs_address_no_direct_intertwiner():
    d=h27.verify()
    assert d["invertible_direct_equivariant_intertwiner"] is False
    assert d["max_rank_direct_intertwiner"]==9
    assert d["three_address_copies_projected_dimension"]==27
    assert all(p["sector_commutant_rank"]==72 for p in d["exact_field_checks"])

def test_W33_induced_quadrangle_census():
    d=causal.verify()
    assert d["induced_C4s"]==1620
    assert d["w33_vertices"]==40 and d["w33_edges"]==240

def test_same_unoriented_C4_distinct_causal_intervals():
    d=causal.verify()
    assert d["diamond_poset"]["comparable_pairs"]==5
    assert d["two_plus_two_poset"]["comparable_pairs"]==4
    assert d["diamond_poset"]["proper_interval_interior_histogram"]=={"0":4,"2":1}
    assert d["two_plus_two_poset"]["proper_interval_interior_histogram"]=={"0":4}

def test_optical_epsilon_packing():
    d=optics.verify()
    assert d["SU4_real_dimension"]==15
    for row in d["finite_alphabet_packing_lower_bounds"]:
        assert row["pair_separation_lower_bound"]>2*row["epsilon"]
        L=row["min_required_word_length"]
        assert (8**(L+1)-1)//7>=row["distinct_target_count"]

def test_optical_hypothetical_loss_is_monotone():
    d=optics.verify(); a=d["conditional_component_sweep"]
    assert d["per_support3_Witting_reflection_two_mode_mixers"]==4
    assert all(q["two_mode_mixing_instances"]==4*q["word_length"] for q in a)
    assert all(a[i]["pessimistic_sequential_survival"]>a[i+1]["pessimistic_sequential_survival"]
               for i in range(len(a)-1))

def test_E6_27_branching_anomaly_not_generation_selection():
    d=matter.verify(); a=d["finite_generation_census"]
    assert [x["SU5_cubic_anomaly"] for x in a]==[0]*5
    assert a[2]["SU5_multiplicities"]=={"10":3,"5":3,"5bar":6,"singlet":6}
    assert d["generation_three_selected_by_group_or_anomaly_alone"] is False

def test_H27_exact_schur_mass_degeneracy():
    d=matter.verify()
    assert d["symmetry_breaking_needed_for_triplet_hierarchies"] is True
    assert all(x["H27_triplet_commutant_rank"]==8 for x in d["modular_Schur_certificates"])
