"""Independent regressions of eight finite W33/physics controls."""
import importlib.util
import itertools
import math
from collections import Counter
from fractions import Fraction as Q
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "analysis" / "toe_20261114_five_fronts_plus_three_field_eom_spectral.py"


@pytest.fixture(scope="module")
def m():
    spec = importlib.util.spec_from_file_location("research_20261114_five_plus_three", SRC)
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


def test_F8_exhaustive_Bell_spectrum_and_symmetric_guard(m):
    d = m.f8_two_copy_bell_spectral_barrier()
    assert d["full_K_spectrum"] == {"567":1,"55":567,"-9":3528}
    assert d["symmetric_two_copy_spectrum"] == {"567":1,"55":567,"-9":1512}
    assert d["antisymmetric_two_copy_spectrum"] == {"-9":2016}
    assert sum(d["symmetric_two_copy_spectrum"].values()) == 2080
    assert sum(d["antisymmetric_two_copy_spectrum"].values()) == 2016


def test_F8_GF8_arithmetic_against_multiplication_field_axioms(m):
    for a,b,c in itertools.product(range(8),repeat=3):
        assert m.gf8_mul(a,b)==m.gf8_mul(b,a)
        assert m.gf8_mul(a,m.gf8_mul(b,c))==m.gf8_mul(m.gf8_mul(a,b),c)
        assert m.gf8_trace(m.gf8_mul(a,b)^m.gf8_mul(a,c))== (
            m.gf8_trace(m.gf8_mul(a,b)) ^ m.gf8_trace(m.gf8_mul(a,c))
        )


def test_F8_exact_spectral_relaxation_failure_and_contraction(m):
    d=m.f8_two_copy_bell_spectral_barrier()
    assert d["independent_numeric_CZ_vs_Pauli_absolute_difference"]<1e-10
    assert min(map(int,d["symmetric_two_copy_spectrum"]))==-9
    assert d["convex_mixed_state_relaxation_min"]==0


def test_9D_Einstein_Maxwell_stress_tensor_direct(m):
    d=m.nine_dimensional_einstein_maxwell_full_equations()
    q=Q(14,5);F2=4*q
    for i in range(9):
        direct = (q/2 if i>=5 else Q(0))-F2/Q(4*(9-2))
        target = Q(d["external_Ricci_tensor_coefficient"] if i<5 else
                   d["internal_Ricci_tensor_coefficient_each_sphere"])
        assert direct==target
    assert Q(d["AdS5_radius_squared"])==10
    assert Q(d["scalar_curvature_9D"])==2


def test_9D_radion_hessian_by_independent_SymPy(m):
    sp=pytest.importorskip("sympy")
    u,v=sp.symbols("u v",real=True)
    V=sp.Rational(14,5)*sp.exp(-sp.Rational(20,3)*u)*sp.cosh(4*v)-4*sp.exp(-sp.Rational(14,3)*u)*sp.cosh(2*v)
    assert sp.simplify(V.subs({u:0,v:0}))==-sp.Rational(6,5)
    assert [sp.diff(V,x).subs({u:0,v:0}) for x in (u,v)]==[0,0]
    H=sp.hessian(V,(u,v)).subs({u:0,v:0})
    assert H==sp.diag(sp.Rational(112,3),sp.Rational(144,5))


def test_QCA_unitary_lattice_and_light_cone(m):
    d=m.microscopic_coin_quantum_clock()
    assert d["checked_ticks"]==11
    assert d["max_dispersion_trace_error"]<1e-12
    assert d["max_observed_group_speed"]<=1


def test_intrinsic_W33_graph_from_F3_symplectic_incidence(m):
    import networkx as nx
    raw=[]
    for x in itertools.product(range(3),repeat=4):
        if not any(x): continue
        j=next(i for i,t in enumerate(x) if t)
        v=x if x[j]==1 else tuple((2*t)%3 for t in x)
        if v not in raw:raw.append(v)
    assert len(raw)==40
    G=nx.Graph()
    G.add_nodes_from(range(40))
    for i in range(40):
        for j in range(i+1,40):
            a,b=raw[i],raw[j]
            s=(a[0]*b[2]+a[1]*b[3]-a[2]*b[0]-a[3]*b[1])%3
            if s==0:G.add_edge(i,j)
    assert set(dict(G.degree()).values())=={12}
    assert G.number_of_edges()==240
    for L in (2,3,4):
        H=nx.Graph()
        H.add_nodes_from(range(40))
        next_vertex=40
        for v,w in G.edges():
            previous=v
            for segment in range(1,L):
                H.add_edge(previous,next_vertex)
                previous=next_vertex
                next_vertex+=1
            H.add_edge(previous,w)
        assert len(H)==40+240*(L-1)
        assert H.number_of_edges()==240*L
        # Independently compute trace(P^2) from the exact degree-weighted edges.
        moment=2*sum((Q(1, H.degree(v)*H.degree(w)) for v,w in H.edges()),Q())/len(H)
        analytic=Q(120*L-200,240*L-200)
        assert moment==analytic


def test_subdivision_heat_return_approaches_one_dimension(m):
    d=m.intrinsic_edge_subdivision_continuum_guard()
    assert abs(d["limit_values"]["100"]["spectral_dimension"]-1)<.01
    assert abs(d["counts"][-1]["numerical_mu2"]-.5)<.005
    assert d["counts"][-1]["distance4_branch_neighborhood_fraction_upper"]<.05


def test_single_photon_logical_4q_GHZ_resource_growth(m):
    d=m.single_photon_four_logical_qubits()
    assert d["logical_H_requires_disjoint_50_50_couplers"]==8
    assert d["logical_CNOT_permutation_swap_pairs"]==4
    table=d["resource_table"]
    assert all(r["orthogonal_modes"]==2**r["logical_qubits"] for r in table)
    assert all(r["one_qubit_H_disjoint_couplers"]*2==r["orthogonal_modes"] for r in table)
    assert all(r["CNOT_transpositions"]*4==r["orthogonal_modes"] for r in table)


def test_GHZ_noise_and_shot_budget_from_first_principles(m):
    d=m.single_photon_four_logical_qubits()
    assert d["GHZ_X4_visibility_under_relative_phase_noise"]==pytest.approx(math.exp(-.01))
    N=math.ceil(2*math.log(2/.05)/(.05**2))
    assert N==d["Hoeffding_accepted_shots_for_0p05_absolute_precision_95pct"]
    assert N<=d["raw_shots_at_loss_only_survival"]


def test_flux_chirality_spectrum_blind_to_orientation(m):
    d=m.flux_orientation_chirality_blind_spot()
    assert d["energies_at_plus_flux"]==pytest.approx(d["energies_at_minus_flux"])
    assert d["oriented_current_at_plus_flux_groundlabel_k0"]==pytest.approx(
        -d["oriented_current_at_minus_flux_groundlabel_k0"])


def test_cohomology_obstruction(m):
    d=m.flux_topology_sector_obstruction()
    assert d["T4_Betti"]==[1,4,6,4,1]
    assert d["S2xS2_Betti"]==[1,0,2,0,1]
    assert d["T4_three_form_independent_topological_fluxes"]==4
    assert d["S2xS2_three_form_independent_topological_fluxes"]==0


def test_dimensionful_clock_speed_does_not_follow_count(m):
    d=m.clock_dimensionful_speed_no_selection()
    vals=[Q(x["a_over_delta_t"]) for x in d["physical_a_dt_and_max_hop_speed"]]
    assert vals==[Q(1),Q(2),Q(1,3),Q(3,7)]


def test_reproducer_eight_outputs_with_status_and_json(m):
    import json
    data=m.run_all()
    assert data["n_fronts"]==8 and len(data["results"])==8
    assert all(d["status"] for d in data["results"].values())
    assert json.loads(m.OUTPUT.read_text(encoding="utf-8"))["status"]==data["status"]
