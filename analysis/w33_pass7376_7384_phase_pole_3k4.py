#!/usr/bin/env python3
"""Pass7376-7384: identify the phase-flat 3K4 as a canonical local graph.

Pass7370-7372 found 12 phase-flat orthogonal D4-pair coordinates inducing 3K4
inside the 45-coordinate tritangent/disjoint-support graph. This replay proves a
stronger statement: those 12 coordinates are exactly the neighborhood of one
unique coordinate in SRG(45,12,3,3). Thus the fixed Coxeter-phase gauge selects
a distinguished 'phase pole'; 3K4 is its ordinary local graph, not an unrelated
12-object coincidence.
"""
from __future__ import annotations
import json,subprocess,sys,itertools
from pathlib import Path
import networkx as nx
import w33_pass7163_7170_e8_hexagonal_lift as e8
import w33_pass7182_d4_glue_spread_code as d4m

ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'analysis'/'w33_pass7370_7372_global_triality_glue_atlas.py'
CERT=ROOT/'data'/'PART_W33_PASS7370_7372_GLOBAL_TRIALITY_GLUE_ATLAS.json'
OUT=ROOT/'data'/'PART_W33_PASS7376_7384_PHASE_POLE_3K4.json'

def main():
    # Materialize the upstream exact atlas if needed; fail closed on any assertion.
    subprocess.run([sys.executable,str(SRC)],check=True)
    old=json.loads(CERT.read_text())
    flat=sorted(r['pair_index'] for r in old['records'] if r['type']=='flat')
    assert len(flat)==12
    _R,_fib,_phase,_radj,adj,_zero,_twelve,_diff=e8.e8_fibers()
    Q,partner=d4m.cqs(adj);P=d4m.pairs(partner);assert len(P)==45
    supports=[frozenset(Q[a]|Q[b]) for a,b in P]
    G=nx.Graph();G.add_nodes_from(range(45))
    for i,j in itertools.combinations(range(45),2):
        if supports[i].isdisjoint(supports[j]):G.add_edge(i,j)
    assert set(dict(G.degree()).values())=={12}
    poles=[v for v in G if set(G.neighbors(v))==set(flat)]
    assert len(poles)==1
    pole=poles[0]
    H=G.subgraph(flat)
    assert sorted(len(c) for c in nx.connected_components(H))==[4,4,4]
    # In fact every local graph of this SRG is 3K4; Coxeter phase singles out one
    # particular local chart by selecting the neighborhood, not a new graph type.
    local_types=[]
    for v in G:
        L=G.subgraph(list(G.neighbors(v)))
        local_types.append((sorted(len(c) for c in nx.connected_components(L)),L.number_of_edges(),set(dict(L.degree()).values())))
    assert all(x==([4,4,4],18,{3}) for x in local_types)
    out={'schema':'w33.pass7376_7384.phase_pole_3k4.v1','status':'PASS',
         'phase_flat_coordinates':flat,'unique_phase_pole_coordinate':pole,
         'identity':'phase-flat 12-set = neighborhood of the unique phase pole in the deterministic Coxeter gauge',
         'ambient_graph':'SRG(45,12,3,3)','every_local_graph':'3K4',
         'interpretation':'Coxeter phase selects one local 3K4 chart among the 45 equivalent local charts.',
         'older_4K4_boundary':'The repo BT660 4K4 lives on a different 16-flag Levi carrier. No 12-to-16 coordinate identification is asserted without an explicit map.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','pole':pole,'flat':'N(pole)','local':'3K4'}))
if __name__=='__main__':main()
