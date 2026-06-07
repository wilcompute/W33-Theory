#!/usr/bin/env python3
"""BT528: Past/Future Toroidal Harmonic-Now Operator Theorem.

Executes branch 1 and corrects the memory-braid model.

Correction to the working picture:
  The 30-now braid from BT501/BT524 is not the whole 600-cell BC-helix
  reservoir.  The 600-cell has 20 BC helices of 30 tetrahedra.  Therefore the
  natural reservoir is 20 counter-rotating past/future helix tracks, each with
  30 addresses.  The earlier 30-now braid is the quotient by helix index, i.e.
  one emitted/addressed now-track.

Past/future toroidal operator:
  Past memory is Csaszar vertex-complete K7 adjacency.
  Future memory is Szilassi/Heawood face-complete adjacency, squared and
  loop-corrected.  BT494 says:
      A_Heawood^2 - 3I on either bipartition = A(K7).
  Hence the harmonic-now operator is the common K7 adjacency recovered from
  both past and future.

Reservoir result:
  20 helix tracks * 30 ejected tetrahedral nows = 600 now-cells.
  Quotienting by helix index gives the BT501 30-now braid.
"""
from __future__ import annotations

import itertools, json
from pathlib import Path
from collections import Counter

import networkx as nx
import sympy as sp

FANO_LINES=[(0,1,3),(0,2,5),(0,4,6),(1,2,4),(1,5,6),(2,3,6),(3,4,5)]
H=20
T=30

def fano_incidence():
    B=sp.zeros(7,7)
    for li,line in enumerate(FANO_LINES):
        for p in line: B[p,li]=1
    return B

def node(kind,h,t): return (kind,h%H,t%T)
def now_cell(h,t):
    return (node('P',h,t), node('P',h,t+1), node('F',h,t), node('F',h,t-1))

def quotient_cell(t):
    return (('P',t%T),('P',(t+1)%T),('F',t%T),('F',(t-1)%T))

def main()->dict:
    # Toroidal operator equality.
    J=sp.ones(7,7); I=sp.eye(7); AK7=J-I
    B=fano_incidence()
    AH=sp.zeros(14,14); AH[:7,7:]=B; AH[7:,:7]=B.T
    future_point=AH**2
    assert future_point[:7,:7]-3*I == AK7
    assert future_point[7:,7:]-3*I == AK7
    past=AK7; future=future_point[:7,:7]-3*I
    harmonic=sp.simplify((past+future)/2)
    assert harmonic==AK7
    assert past*future-future*past==sp.zeros(7)
    anticom=sp.simplify(past*future+future*past)
    assert anticom==2*(AK7**2)
    assert AK7.charpoly().as_expr().factor()==(sp.Symbol('lambda')-6)*(sp.Symbol('lambda')+1)**6

    # 20x30 counter-rotating now reservoir.
    G=nx.Graph(); cells=[]; triangles=set()
    for h in range(H):
        for t in range(T):
            c=now_cell(h,t); cells.append(c); G.add_nodes_from(c)
            for e in itertools.combinations(c,2): G.add_edge(*e)
            for tri in itertools.combinations(c,3): triangles.add(tuple(sorted(tri)))
    assert len(cells)==600
    assert G.number_of_nodes()==1200
    assert G.number_of_edges()==3000
    assert len(triangles)==2400
    assert G.number_of_nodes()-G.number_of_edges()+len(triangles)-len(cells)==0

    # Quotient by helix index recovers the one-track 30-now braid.
    Q=nx.Graph(); qcells=[]; qtri=set()
    for t in range(T):
        c=quotient_cell(t); qcells.append(c); Q.add_nodes_from(c)
        for e in itertools.combinations(c,2): Q.add_edge(*e)
        for tri in itertools.combinations(c,3): qtri.add(tuple(sorted(tri)))
    assert len(qcells)==30 and Q.number_of_nodes()==60 and Q.number_of_edges()==150 and len(qtri)==120
    assert Q.number_of_nodes()-Q.number_of_edges()+len(qtri)-len(qcells)==0

    # Ejection schedule: each helix track contributes one 30-address now braid.
    address_counts=Counter(t for h,t in itertools.product(range(H),range(T)))
    helix_counts=Counter(h for h,t in itertools.product(range(H),range(T)))
    assert address_counts==Counter({t:20 for t in range(T)})
    assert helix_counts==Counter({h:30 for h in range(H)})

    results={
        'theorem':'BT528 Past/Future Toroidal Harmonic-Now Operator Theorem',
        'toroidal_operator':{
            'past':'Csaszar K7 adjacency A_C',
            'future':'Szilassi/Heawood squared operator A_H^2-3I on one bipartition',
            'identity':'A_C = A_H^2 - 3I = harmonic now operator',
            'commutator':'0',
            'anticommutator':'2 A(K7)^2',
            'K7_spectrum':'6^1, (-1)^6'},
        'reservoir_model':{'BC_helices':20,'addresses_per_helix':30,'ejected_now_cells':600,'vertices':1200,'edges':3000,'triangles':2400,'euler_characteristic_3_complex':0},
        'quotient_30_now_braid':{'interpretation':'collapse helix index h; this recovers BT501/BT524 one-track 30-now braid','now_cells':30,'vertices':60,'edges':150,'triangles':120,'euler_characteristic':0},
        'past_future_reading':{'past':'accumulated Csaszar vertex-complete memory rail','future':'counter-rotating Szilassi/Heawood face-complete possibility rail','now':'tetrahedron ejected by the equality of the two K7 adjacency observables','becomes_past':'after ejection, the now-cell boundary is available as the next past rail state in the reservoir'},
        'substrate_reading':{'600':'20*30 tetrahedral now ejections / 600-cell tetrahedra','30':'BC address period','20':'number of BC helix tracks in the 600-cell','K7':'common harmonic adjacency recovered from past and future toroidal memories'}
    }
    out=Path('data/PART_BT528_PAST_FUTURE_TOROIDAL_HARMONIC_NOW_OPERATOR_results.json')
    out.parent.mkdir(exist_ok=True); out.write_text(json.dumps(results,indent=2),encoding='utf-8')
    print(json.dumps(results,indent=2)); return results
if __name__=='__main__': main()
