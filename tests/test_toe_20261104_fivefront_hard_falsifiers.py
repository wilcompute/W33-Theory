"""Reproducible five-front mathematical and open-system falsifier regression."""
from pathlib import Path
import importlib.util
import math
import numpy as np
import pytest

ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/"analysis"/"toe_20261104_fivefront_hard_falsifiers.py"
spec=importlib.util.spec_from_file_location("fivefront20261104",SRC)
mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)

@pytest.fixture(scope="module")
def r():
    return mod.main()

def test_exact_equidistant_subdivision_characteristic(r):
    f=r["continuum"]
    alpha=math.acos(math.sqrt(6)/4)
    assert math.isclose(f["first_gap_metric_graph_target"],alpha*alpha,rel_tol=1e-12)
    for row in f["results"]:
        L=row["segments"]
        lam=row["laplacian_eigenvalue"]
        theta=math.acos(1-lam/2)
        mu=4*math.cos(L*theta)+2*math.tan(theta/2)*math.sin(L*theta)
        assert abs(mu-math.sqrt(6))<1e-8
        assert row["edges"]-row["subdivision_vertices"]+1==81
    assert abs(f["results"][-1]["asymptotic_coefficient_L_times_relative_error"]-.5)<.001

def test_symmetry_scalar_complete_frame(r):
    s=r["symmetry"]
    assert s["all_apartments"]==1620
    assert math.isclose(s["all_apartment_frame_condition_number"],1,abs_tol=1e-12)
    assert s["all_apartment_undirected_hopping_pairs"]==12720
    assert s["all_apartment_max_offdiagonal_neighbors"]==159

def test_weighted_c3_conditioning(r):
    s=r["symmetry"]
    assert s["each_frame_exact_C3_invariant_and_cycle_preserving"]
    assert s["selected_C3_frame_seeds"]==[5,9,18]
    assert math.isclose(sum(s["sampled_optimal_weights"]),3,abs_tol=1e-10)
    assert min(s["sampled_optimal_weights"])>0
    assert s["unweighted_three_frame_condition_number"]<7.01
    assert s["sampled_optimized_condition_number"]<6.9
    assert s["relative_condition_improvement"]>1.02
    assert s["unweighted_frame_hopping_pairs"]==4320

def test_positive_constraint_zero_locus_trivial(r):
    g=r["gravity"]
    assert g["incidence_rank"]==79
    assert g["cycle_rank"]==81
    assert g["supported_edges"]==160
    assert g["minimum_edge_participation"]>=3
    assert g["explicit_pure_gauge_zero_witness"]

def test_vectorlike_cp_schur_complement(r):
    f=r["flavor"]
    assert f["effective_rank_one_update"]
    assert f["exact_block_determinant_identity"]
    assert f["CP_odd_commutator_imag_cubed_trace"]=="1600"
    assert f["real_flavor_vector_CP_invariant"]==0
    assert f["conjugated_vector_CP_invariant"]=="-1600"

def test_lindblad_reference_witness_and_blind_populations(r):
    h=r["hardware"]
    assert h["status"]=="PASS_LINDBLAD_RAMSEY_PHASE_WITNESS"
    assert len(h["scenarios"])==5
    assert all(s["max_observed_triangle_population_difference"]<1e-12 for s in h["scenarios"])
    assert math.isclose(h["scenarios"][3]["absolute_Ramsey_imaginary_coherence_difference"],
                        .03937993677123733,rel_tol=1e-11)
    assert h["scenarios"][-1]["absolute_Ramsey_imaginary_coherence_difference"]>.035
    for flux in (1,-1):
        rho=mod.density(mod.h_triangle(flux),.1,.1,.4)
        assert np.min(np.linalg.eigvalsh(rho))>-1e-12
        assert abs(np.trace(rho)-1)<1e-12

def test_trotter_pulse_compilation(r):
    rows=r["hardware"]["trotter_results"]
    assert [p["steps"] for p in rows]==[1,2,4,8,16,32,64]
    assert all(row["elementary_signed_edge_pulses"]==3*row["steps"] for row in rows)
    assert rows[-1]["contrast_absolute_error"]<1.1e-5
    assert 3.7<rows[3]["contrast_absolute_error"]/rows[4]["contrast_absolute_error"]<4.3
    assert rows[-1]["max_unitary_entry_error"]<.0013

def test_lindblad_sequential_gate_overhead_depth_optimum(r):
    h=r["hardware"]
    seq=h["noisy_sequential_compile_results"]
    assert h["noisy_sequential_compile_best_depth_in_sample"]==16
    assert [a["steps"] for a in seq]==[1,2,4,8,16,32,64]
    assert all(a["pulses"]==3*a["steps"] for a in seq)
    assert seq[4]["error_relative_to_simultaneous_noisy_analog"]<seq[3]["error_relative_to_simultaneous_noisy_analog"]
    assert seq[4]["error_relative_to_simultaneous_noisy_analog"]<seq[5]["error_relative_to_simultaneous_noisy_analog"]
    assert seq[-1]["loss_vacuum_population"]>seq[4]["loss_vacuum_population"]
    assert seq[-1]["total_physical_duration"]>seq[4]["total_physical_duration"]
