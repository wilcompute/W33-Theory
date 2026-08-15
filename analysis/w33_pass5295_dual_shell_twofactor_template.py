#!/usr/bin/env python3
"""Pass5295: q=5,7,9 dual witnesses share a K_{q-1,q-1}+two-2-factors skeleton.

The exact support graphs from Pass5230/5245/5292 admit the same decomposition.
Split the 2(q-1) selected P-blocks into halves A,B of size m=q-1.  Every cross
pair is adjacent and each half contributes a 2-factor.  Thus the support graph is

    K_{m,m} union F_A union F_B,

with F_A,F_B 2-regular.  The concrete finite anchors are
q5: C4 | C4; q7: C6 | (C3+C3); q9: C8 | C8.

This automatically gives selected degree m+2=q+1 and q^2-1 edges, matching the
exact double-cover witnesses.  It is a construction target, not an all-q proof
that such carrier sets exist.
"""
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5295_DUAL_SHELL_TWOFACTOR_TEMPLATE.json'

def cycles_edges(parts,offset=0):
    E=set();s=offset
    for n in parts:
        V=list(range(s,s+n));s+=n
        for i in range(n):E.add(tuple(sorted((V[i],V[(i+1)%n]))))
    return E

def row(q,left,right):
    m=q-1;assert sum(left)==sum(right)==m
    E={(a,m+b) for a in range(m) for b in range(m)}
    E|=cycles_edges(left,0);E|=cycles_edges(right,m)
    deg=[0]*(2*m)
    for a,b in E:deg[a]+=1;deg[b]+=1
    assert set(deg)=={q+1};assert len(E)==q*q-1
    return {'q':q,'vertices':2*m,'bipartition':[m,m],'left_2factor':left,'right_2factor':right,'degree':q+1,'edges':len(E),'active_points_if_every_edge_carries_two':2*len(E)}

def main():
    A=[row(5,[4],[4]),row(7,[6],[3,3]),row(9,[8],[8])]
    out={'pass':5295,'status':'THEOREM_FINITE_Q5_Q7_Q9_DUAL_SUPPORT_TWOFACTOR_SKELETON',
      'template':'selected graph = K_{q-1,q-1} plus a 2-factor on each half',
      'anchors':A,
      'consequence':'The finite witnesses all have 2(q-1) blocks, degree q+1, q^2-1 selected-graph edges, and 2(q^2-1) doubly covered W-points.',
      'all_odd_target':'Construct carrier sets realizing this skeleton geometrically for every odd q and control the resulting PSp4(q) orbit pair codegrees.',
      'boundary':'Finite graph decomposition only. It does not prove existence of a dual check with this skeleton for every odd q.'}
    OUT.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
