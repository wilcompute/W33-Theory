#!/usr/bin/env python3
"""Pass 4657 — identify the order-216 triality intersection group.

Pass4649 found pairwise intersections of triality-conjugate PSp(4,3) copies of
order 216. Pass4654 proved that the fixed anisotropic 2-plane corresponds
PSp-equivariantly to a W33 point, with setwise stabilizer 648 and pointwise
stabilizer 216. This verifier reconstructs the W33 point action directly and
classifies that 216 subgroup from its derived series and quotients.

The W33 point stabilizer has derived series
  648 -> 216 -> 54 -> 27 -> 3 -> 1.
Its order-27 third derived subgroup is extraspecial of exponent three. The 216
subgroup modulo that 3^{1+2} radical is Q8; the full 648 stabilizer modulo the
same radical is SL(2,3)=2A4. Thus the pairwise triality intersection is
3^{1+2}:Q8, exactly the derived subgroup of the W33 point parabolic
3^{1+2}:2A4.
"""
from __future__ import annotations
import json
from collections import Counter, deque
from pathlib import Path
import numpy as np
from sympy.combinatorics import Permutation, PermutationGroup
from w33_pass4472_4479_apartment_module_thermo_ihara_pauli import build_geometry, norm3, transvection_matrix
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS4657_TRIALITY_INTERSECTION_GROUP_REGEN.json'

def compose(p,q): return tuple(p[q[i]] for i in range(len(p)))
def perm_group(gens,n):
    I=tuple(range(n)); S={I}; Q=deque([I])
    while Q:
        a=Q.popleft()
        for g in gens:
            b=compose(g,a)
            if b not in S: S.add(b); Q.append(b)
    return S
def point_perm(M,pts,pidx):
    out=[]
    for p in pts:
        y=(np.asarray(M,dtype=int)@np.asarray(p,dtype=int))%3
        out.append(pidx[norm3(tuple(map(int,y)))])
    return tuple(out)
def sympy_group(perms): return PermutationGroup([Permutation(list(p)) for p in perms])
def subgroup_elements(H): return list(H.generate_schreier_sims())
def quotient_order(g,N,maxn=24):
    x=Permutation(list(range(g.size)))
    for n in range(1,maxn+1):
        x=g*x
        if N.contains(x): return n
    raise RuntimeError('quotient order bound')
def coset_reps(H,N):
    elems=subgroup_elements(H); unseen={tuple(g.array_form) for g in elems}; reps=[]; Ne=subgroup_elements(N)
    while unseen:
        key=min(unseen); g=Permutation(list(key)); reps.append(g)
        unseen-={tuple((g*n).array_form) for n in Ne}
    return reps

def main():
    pts,pidx,_,_,_,_,_,_,_=build_geometry(); assert len(pts)==40
    candidates=[point_perm(transvection_matrix(v),pts,pidx) for v in pts]
    gens=[]; G={tuple(range(40))}
    for p in candidates:
        trial=perm_group(gens+[p],40)
        if len(trial)>len(G): gens.append(p); G=trial
        if len(G)==25920: break
    assert len(G)==25920 and len(gens)==5
    Pset=[g for g in G if g[0]==0]; assert len(Pset)==648
    P=sympy_group(Pset); assert P.order()==648
    series=[P]
    while series[-1].order()>1: series.append(series[-1].derived_subgroup())
    orders=[int(H.order()) for H in series]; assert orders==[648,216,54,27,3,1]
    I=series[1]; O=series[3]
    assert I.order()==216 and O.order()==27 and I.center().order()==3 and I.derived_subgroup().order()==54
    assert O.center().order()==3 and O.derived_subgroup().order()==3
    assert Counter(int(g.order()) for g in subgroup_elements(O))==Counter({3:26,1:1})
    qI=Counter(quotient_order(g,O) for g in coset_reps(I,O))
    qP=Counter(quotient_order(g,O) for g in coset_reps(P,O))
    assert qI==Counter({4:6,1:1,2:1})
    assert qP==Counter({3:8,6:8,4:6,1:1,2:1})
    old=json.loads((ROOT/'data/PART_W33_PASS4649_FULL_TRIALITY_GROUP_INTERSECTIONS.json').read_text())
    old54=json.loads((ROOT/'data/PART_W33_PASS4654_TRIALITY_PLANE_W33_POINT_INTERTWINER.json').read_text())
    assert old['PSp_intersections']['pairwise_order']==216
    assert old['PSp_intersections']['pairwise_center_order']==3
    assert old['PSp_intersections']['pairwise_derived_order']==54
    assert '648' in json.dumps(old54) and '216' in json.dumps(old54)
    out={'pass':4657,
      'W33_point_stabilizer':{'order':648,'derived_series_orders':orders,'structure':'3^{1+2}:SL(2,3) = 3^{1+2}:2A4'},
      'triality_pair_intersection':{'order':216,'center_order':3,'derived_order':54,'structure':'3^{1+2}:Q8','equals_point_stabilizer_derived_subgroup':True},
      'extraspecial_radical':{'order':27,'center_order':3,'derived_order':3,'nonidentity_element_orders':{'3':26},'structure':'3_+^{1+2}'},
      'quotients':{'intersection_mod_3radical':{'order':8,'element_order_census':{str(k):v for k,v in sorted(qI.items())},'isomorphism':'Q8'},'point_stabilizer_mod_3radical':{'order':24,'element_order_census':{str(k):v for k,v in sorted(qP.items())},'isomorphism':'SL(2,3)=2A4'}},
      'tower':'3^{1+2}:Q8 (216) < 3^{1+2}:2A4 (648) < PSp(4,3) (25920)',
      'theorem':'The order-216 pairwise intersection of triality-conjugate PSp(4,3) copies is exactly the derived subgroup of the W33 point stabilizer, with structure 3^{1+2}:Q8; its extraspecial 3-radical is the third derived subgroup of the 648 parabolic.',
      'boundary':'Finite subgroup/action theorem only.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n',encoding='utf-8'); print(json.dumps(out,indent=2,sort_keys=True)); return 0
if __name__=='__main__': raise SystemExit(main())
