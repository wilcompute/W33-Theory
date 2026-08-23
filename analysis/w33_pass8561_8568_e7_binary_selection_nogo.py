#!/usr/bin/env python3
"""Pass8561-8568: E7 itself does not select one of the 336 W(3,2) sectors.

Dependency: Pass8489-8496 identifies the 63 E7 antipodal root pairs with all
three-qubit Pauli classes.  Here we stay entirely in E7 root geometry: every
nonorthogonal pair closes to a unique three-pair A2 triangle, giving the same
336 closed anticommuting Pauli triangles.  The E7 Weyl action is then computed
on those 336 triangles.
"""
from __future__ import annotations
import itertools,json
from collections import Counter
from pathlib import Path
from sympy.combinatorics import Permutation,PermutationGroup
from analysis import w33_pass8489_8496_e7_pauli_rootpair_bridge as E
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS8561_8568_E7_BINARY_SELECTION_NOGO.json'

def main():
    R=E.roots();r0=E.S[1]
    E7=[r for r in R if sum(a*b for a,b in zip(r,r0))==0]
    assert len(E7)==126
    pairs=sorted({E.key(r) for r in E7});pi={p:i for i,p in enumerate(pairs)}
    assert len(pairs)==63

    tri=set()
    for x,y in itertools.combinations(pairs,2):
        d=sum(a*b for a,b in zip(x,y))
        if abs(d)!=4:continue
        s=1 if d>0 else -1
        z=E.key(tuple(x[i]-s*y[i] for i in range(8)))
        assert z in pi
        tri.add(frozenset((x,y,z)))
    assert len(tri)==336
    assert set(Counter(x for T in tri for x in T).values())=={16}

    gens=[];G=PermutationGroup([Permutation(list(range(63)))])
    growth=[]
    for r in E7:
        p=Permutation([pi[E.key(E.refl(x,r))] for x in pairs],size=63)
        H=PermutationGroup(gens+[p])
        if int(H.order())>int(G.order()):
            gens.append(p);G=H;growth.append(int(H.order()))
            if int(H.order())==1451520:break
    assert int(G.order())==1451520

    tris=sorted(tri,key=lambda T:tuple(sorted(pi[x] for x in T)))
    ti={frozenset(pi[x] for x in T):i for i,T in enumerate(tris)}
    tgens=[]
    for g in gens:
        tgens.append(Permutation([ti[frozenset(int(g(pi[x])) for x in T)] for T in tris],size=336))
    GT=PermutationGroup(tgens)
    assert int(GT.order())==1451520
    assert [len(o) for o in GT.orbits()]==[336]
    H=GT.stabilizer(0)
    assert int(H.order())==4320
    assert int(H.derived_subgroup().order())==1080

    out={
      'schema':'w33.pass8561_8568.e7_binary_selection_nogo.v1','status':'PASS','passes':'8561-8568',
      'E7_root_pairs':63,'closed_A2_rootpair_triangles':336,'triangles_through_each_pair':16,
      'weyl_projective_action':{'order':1451520,'identification':'Sp6(2)','triangle_orbits':[336],
         'triangle_stabilizer_order':4320,'triangle_stabilizer_derived_order':1080,
         'stabilizer_identification':'Sp4(2) x Sp2(2) ~= S6 x S3'},
      'generator_order_growth':growth,
      'theorem':'The full projective E7 Weyl symmetry is transitive on the 336 E7 A2 root-pair triangles, hence on the 336 W(3,2) sectors / closed anticommuting Pauli triangles of Pass8489. Lifting Leech W(5,2) to the exact E7 root model supplies no canonical binary sector selector.',
      'claim_boundary':'Exact E7 finite-root/symplectic no-selection theorem; no physical subsystem claim.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','triangles':336,'orbit':[336],'stabilizer':4320}))
if __name__=='__main__':main()
