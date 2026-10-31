"""Independent regression gates for the eight-front W33 quantum/topological continuation."""
import itertools,json,math
import numpy as np
import pytest
from analysis import w33_20261031_turan_mub_magic_and_topology as T
from analysis import w33_20261031_native_floquet_chiral_edge as C

@pytest.fixture(scope="module")
def packet():
    return T.build(),C.build()

def test_exact_Turan_formula_and_saturation(packet):
    d=packet[0]["results"]["01_all_n_clock_ground_states"]
    for r in d["finite_examples"]:
        n=r["n"]
        assert r["turan_noncommuting_bonds"]==T.turan(n)
        assert abs(r["exact_Emin_at_J1_K2"]+2*T.turan(n)/3)<1e-9
        if n>=7:assert r["exact_ground_state_count_for_n_ge_7"]>0

def test_clock_small_n_exhaustive_independent_enumeration(packet):
    A=T.ADJ;v=np.arange(40)
    # 40^3=64,000 ordered direction triples, including repetitions.
    E=-2/3
    best=0.
    for p in v:
        for q in v:
            costs=(0 if p==q else (E if not A[p,q] else 2))
            for r in v:
                z=costs+(0 if p==r else(E if not A[p,r] else 2))
                z+=0 if q==r else(E if not A[q,r] else 2)
                if z<best:best=z
    assert abs(best-3*E)<1e-12

def test_clock_eight_global_degeneracy_count(packet):
    x={r["n"]:r for r in packet[0]["results"]["01_all_n_clock_ground_states"]["finite_examples"]}
    assert abs(x[8]["exact_Emin_at_J1_K2"]+18)<1e-10
    assert x[8]["exact_ground_state_count_for_n_ge_7"]==888852787200

def test_spectral_coloring_lower_bound_and_MUB(packet):
    d=packet[0]["results"]["02_exact_chromatic_MUB_geometry"]
    assert d["chromatic_lower_bound_Hoffman"]==d["actual_proper_coloring"]==10
    assert sorted(sum(d["10_disjoint_maximal_commuting_contexts"],[]))==list(range(40))
    assert d["mutual_unbiasedness_max_error"]<1e-11

def test_exact_JW_projector_is_local_strange_resource(packet):
    d=packet[0]["results"]["03_JonesWenzl_rank1_magic_resource"]
    assert d["exact_f4_projector_identity"].startswith("f4=|0><0|")
    assert d["f2_f3_f4_f5_ranks"]==[6,3,1,0]
    assert abs(d["f4_Wigner_min"]+1/9)<1e-11
    assert abs(d["f4_Wigner_L1"]-5/3)<1e-11
    assert abs(d["f4_mana"]-math.log(5/3))<1e-11
    assert abs(d["f4_reduced_purity"]-1)<1e-11

def test_optical_gaussian_phase_noise_transition(packet):
    rows=packet[0]["results"]["04_optical_phase_noise_limit"]["rows"]
    assert abs(rows[0]["optimal_mixed_Helstrom_error"]-(1-2*math.sqrt(10)/7)/2)<1e-11
    assert all(b["optimal_mixed_Helstrom_error"]>=a["optimal_mixed_Helstrom_error"]-1e-12
               for a,b in zip(rows,rows[1:]))
    assert abs(rows[-1]["optimal_mixed_Helstrom_error"]-rows[-1]["fixed_port_min_error"])<1e-10

def test_metric_inertia_not_lorentzian(packet):
    d=packet[0]["results"]["05_gravitational_metric_signature"]
    assert d["inertia_Q"]==[4,0,0] and min(d["Q_eigenvalues"])>0

def test_no_SU24_equivalence_to_S3_double(packet):
    d=packet[0]["results"]["06_anyonic_category_mismatch"]
    assert len(d["SU2_4_simple_quantum_dimensions"])==5
    assert len(d["D_S3_simple_quantum_dimensions"])==8
    assert abs(d["SU2_4_total_dimension_squared"]-12)<1e-11
    assert d["D_S3_total_dimension_squared"]==36

def test_fixed_graph_heat_kernel_no_four_dimensional_limit(packet):
    d=packet[0]["results"]["07_native_spectral_dimension_obstruction"]
    assert d["ultraviolet_limit"]==d["infrared_limit"]==0
    assert d["sample_peak_dimension"]<4
    assert d["laplacian_spectrum"]=={"0":1,"10":24,"16":15}

def test_canonical_characteristic_five_torsion_from_integer_rank(packet):
    d=packet[0]["results"]["08_canonical_characteristic5_torsion"]
    assert d["rank_over_Q"]==18 and d["integer_kernel_dimension"]==6
    assert d["rank_reduction_mod5_of_integer_kernel_basis"]==6
    assert d["kernel_B_mod5_dimension"]==13 and d["canonical_Tor_dimension"]==7
    assert d["order5_induced_Jordan_blocks"]==[3,3,1]

def test_full_Sp43_gate_word_not_just_projective_swap(packet):
    d=packet[1]["gate"]
    assert d["full_symplectic_group_order"]==51840
    assert d["number_ticks"]==13
    assert d["frobenius_unitary_error"]<1e-11
    assert abs(math.hypot(*d["phase_re_im"])-1)<1e-11

def test_open_boundary_shift_and_closed_bulk_identity(packet):
    for r in packet[1]["open_square_runs"]:
        assert r["bulk_identity"]
        assert r["edge_cycle_length"]==2*r["L"]-1
        assert r["active_edge_GNVW_qutrit_index"]==3
        assert len(r["edge_translation_orbit"])==r["edge_cycle_length"]
    for r in packet[1]["periodic_torus_controls"]:
        assert r["bulk_identity"] and r["edge_cycle_length"]==0
        assert len(r["per_stage_swap_pairs"])==4

def test_frozen_json_certs_present(packet):
    assert T.OUT.is_file() and C.OUT.is_file()
    assert json.loads(T.OUT.read_text())["results"]["08_canonical_characteristic5_torsion"]["status"]==packet[0]["results"]["08_canonical_characteristic5_torsion"]["status"]
    assert json.loads(C.OUT.read_text())["status"]==packet[1]["status"]
