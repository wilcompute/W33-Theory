#!/usr/bin/env python3
"""Pass8241-8248 (outside-box): 336 closed anticommuting Pauli triangles dualize to 336 W(3,2) copies.

In the Leech W(5,2) three-qubit carrier, a nondegenerate symplectic 2-plane has
three nonzero vectors {a,b,a+b}; all three pairwise symplectic products are one.
Thus it is a closed anticommuting Pauli triangle. Orthogonal complement is a
nondegenerate 4-space and hence a W(3,2). This is a bijection.
"""
from __future__ import annotations
import itertools,json
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS8241_8248_BINARY_PAULI_TRIANGLE_W3_DUALITY.json'
V=[tuple((n>>i)&1 for i in range(6)) for n in range(1,64)]
def om(a,b):return (a[0]*b[3]+a[1]*b[4]+a[2]*b[5]+a[3]*b[0]+a[4]*b[1]+a[5]*b[2])&1
def add(a,b):return tuple(x^y for x,y in zip(a,b))
def main():
    tri=set()
    noncomm_edges=0
    for a,b in itertools.combinations(V,2):
        if om(a,b):
            noncomm_edges+=1;T=frozenset((a,b,add(a,b)));assert len(T)==3;assert all(om(x,y) for x,y in itertools.combinations(T,2));tri.add(T)
    assert noncomm_edges==1008 and len(tri)==336 and noncomm_edges//len(tri)==3
    comps=[]
    for T in tri:
        W=frozenset(v for v in V if all(om(v,u)==0 for u in T));assert len(W)==15;comps.append(W)
    assert len(set(comps))==336
    inc=Counter()
    for T in tri:
        for x in T:inc[x]+=1
    assert set(inc.values())=={16}
    out={'schema':'w33.pass8241_8248.binary_pauli_triangle_w3_duality.v1','status':'PASS','passes':'8241-8248','outside_box':True,
      'ambient':'W(5,2) / three-qubit Pauli classes','noncommuting_edges':1008,'closed_anticommuting_triangles':336,'triangles_through_each_point':16,
      'closure':'each noncommuting pair {a,b} belongs to the unique linear triangle {a,b,a+b}',
      'orthogonal_complement':'each triangle spans a nondegenerate F2^2; its perp is a nondegenerate F2^4 carrying W(3,2)',
      'W3_copies':336,'bijection':True,
      'theorem':'The 336 embedded W(3,2) sectors of the Leech W(5,2) carrier are canonically dual to the 336 closed anticommuting Pauli triangles {a,b,a+b}. Selecting a two-qubit symplectic sector is exactly selecting one such closed anticommuting triangle.',
      'claim_boundary':'Exact finite symplectic/Pauli-class statement; no physical subsystem factorization is inferred.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps({'status':'PASS','triangles':336,'W3':336}))
if __name__=='__main__':main()
