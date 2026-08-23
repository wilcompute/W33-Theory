#!/usr/bin/env python3
"""Pass9513-9520 outside-box: test the 252/126 Hall-Janko--Qminus count matches.

A fixed G2(4)-graph edge gives vertex cells 36,63,63,252.  Q-(5,3) has 112
singular points and 252 nonsingular points, split into two norm classes of 126.
The cardinalities tempt an identification.  This pass checks the natural graph
relation and falsifies the naive bridge.
"""
from __future__ import annotations
import itertools,json
from collections import Counter
from fractions import Fraction
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS9513_9520_HJ_QMINUS_252_BRIDGE_FALSIFIER.json'
P=3

def canon(v):
 v=tuple(int(x)%P for x in v)
 for x in v:
  if x:
   u=pow(x,-1,P);return tuple(u*y%P for y in v)
 raise ValueError

def main():
 edge=json.loads((ROOT/'data/PART_W33_PASS9365_9372_G24_EDGE_ORBITAL_REFINEMENT.json').read_text())
 part=edge['fixed_edge_vertex_partition'];fc=edge['forced_edge_counts']
 assert (part['A_common'],part['B_u_only'],part['C_v_only'],part['D_neither'])==(36,63,63,252)
 pts=sorted({canon(v) for v in itertools.product(range(P),repeat=6) if any(v)})
 norm=Counter(sum(x*x for x in v)%P for v in pts);assert norm==Counter({0:112,1:126,2:126})
 nons=[np.array(v,dtype=np.int64) for v in pts if sum(x*x for x in v)%P]
 deg=[];within={1:[],2:[]}
 for u in nons:
  tu=int(u@u)%P;d=0;w=0
  for v in nons:
   if np.array_equal(u,v):continue
   if int(u@v)%P==0:
    d+=1
    if int(v@v)%P==tu:w+=1
  deg.append(d);within[tu].append(w)
 assert set(deg)=={81} and set(within[1])==set(within[2])=={45}
 # Natural induced G2(4) degrees from exact edge counts.
 d_avg=Fraction(2*fc['DD'],part['D_neither']);assert d_avg==66
 bc_edges=fc['BB']+fc['CC']+fc['BC'];bc_avg=Fraction(2*bc_edges,part['B_u_only']+part['C_v_only']);assert bc_avg==31
 out={'schema':'w33.pass9513_9520.hj_qminus_252_bridge_falsifier.v1','status':'PASS','passes':'9513-9520','outside_box':True,
  'count_matches':{'G2_fixed_edge_D':252,'Qminus_nonsingular_points':252,'G2_B_union_C':126,'Qminus_each_norm_class':126,'Qminus_singular_points':112},
  'Qminus_orthogonality_graph':{'all_252_degree':81,'within_each_126_norm_class_degree':45},
  'G2_induced_graph':{'D_252_average_degree':66,'B_union_C_126_average_degree':31},
  'falsifier':'252=252 and 126=126 are exact but the natural adjacency invariants disagree (81 != 66 and 45 != 31), so neither obvious cardinality match is an orthogonality-graph identification.',
  'surviving_direction':'A bridge may still exist through a different orbital/relation, especially because Pass9365-9372 exposes a rank-14 edge association scheme rather than a single graph. Any future claim must match that full scheme, not counts alone.',
  'theorem':'The Hall-Janko/G2(4) fixed-edge partition and Q-(5,3) have striking 252 and 126 cardinality coincidences, but the most natural objectwise identification is ruled out by degree invariants. This converts a tempting numerology into a precise association-scheme matching problem.',
  'boundary':'Negative theorem for the natural induced-edge versus orthogonality relations only; it does not rule out a nontrivial correspondence using another G2(4) orbital.'}
 OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps({'status':'PASS','matches':[252,126],'degree_mismatches':[[66,81],[31,45]]}));return 0
if __name__=='__main__':raise SystemExit(main())
