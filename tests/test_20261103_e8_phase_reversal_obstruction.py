"""Exact E8 base-fixing phase-reversal no-go regression."""
from __future__ import annotations
import json,runpy
from pathlib import Path
import networkx as nx
ROOT=Path(__file__).resolve().parents[1]
SCRIPT=ROOT/"analysis"/"2026_11_03_e8_fiberwise_phase_reversal_obstruction.py"

def test_exact_reflection_no_go():
    d=runpy.run_path(str(SCRIPT))["run"]()
    assert d["status"]=="PASS_BASE_FIXING_FIBERWISE_E8_REFLECTION_OBSTRUCTION"
    assert d["fibers"]==40 and d["e8_root_count"]==240
    assert d["coupled_fiber_pairs"]==540
    assert d["base_complement_triangles"]==3240
    assert d["uniform_c6_phase_shift_automorphisms_verified"]==6
    assert d["oriented_triangle_holonomy_mod6_counts"]=={"1":1440,"3":360,"5":1440}

def test_odd_phase_requirement_no_bipartite_gauge():
    E=runpy.run_path(str(ROOT/"analysis"/"w33_pass7163_7170_e8_hexagonal_lift.py"))
    R,F,phase,radj,adj,zero,pairs,hist=E["e8_fibers"]()
    graph=nx.Graph()
    graph.add_nodes_from(range(40))
    graph.add_edges_from(pairs)
    assert graph.number_of_edges()==540
    assert not nx.is_bipartite(graph)
    triangle=sum(nx.triangles(graph).values())//3
    assert triangle==3240

def test_z2_origin_gauge_invariance():
    # A change of each sixfold fiber origin shifts s_ab by a difference,
    # hence changes 2*s_ab+1 by an even coboundary; parity stays odd.
    for s in range(6):
        for tau_a in range(6):
            for tau_b in range(6):
                before=(2*s+1)%6
                after=(before+2*(tau_b-tau_a))%6
                assert before%2==1 and after%2==1
