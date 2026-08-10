#!/usr/bin/env python3
"""Pass 4654 — explicit triality-intersection-plane -> W33 point intertwiner.

Pass4649 found 40 anisotropic F2 2-planes (three nonsingular vectors each)
from pairwise intersections of triality-conjugate PSp(4,3) copies.  Their total
polar-orthogonality graph is SRG(40,12,2,4).  This verifier decides which of the
inequivalent odd-q W33 40-object carriers it actually is.

The base-plane stabilizer has order 648.  It fixes no W33 line but exactly one
W33 point.  Therefore gP0 -> gp0 is a well-defined PSp-equivariant bijection
from the 40 anisotropic planes to the W33 point carrier.  Under this bijection
mutual total polar orthogonality is exactly W33 point collinearity.
"""
from __future__ import annotations

import json
from itertools import combinations
from pathlib import Path

import numpy as np

from w33_pass4472_4479_apartment_module_thermo_ihara_pauli import (
    build_geometry, build_line_perm, perm_group, transvection_matrix,
)
from w33_pass4587_w33_derived_d4_triality import rank_basis_int, span

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS4654_TRIALITY_PLANE_W33_POINT_INTERTWINER.json'


def permute_mask40(m,p,j):
    out=0; x=int(m)
    while x:
        b=x&-x; i=b.bit_length()-1; out|=1<<p[i]; x^=b
    return min(out,out^j)


def main():
    pts,pidx,lines,lidx,A,Astar,_,_,_=build_geometry()
    A=np.asarray(A,dtype=np.uint8); Astar=np.asarray(Astar,dtype=np.uint8)
    all_trans=[build_line_perm(transvection_matrix(v),pts,pidx,lines,lidx) for v in pts]
    gens=[]; G={tuple(range(40))}
    for p in all_trans:
        trial=perm_group(gens+[p])
        if len(trial)>len(G): gens.append(p); G=trial
        if len(G)==25920: break
    assert len(G)==25920

    n=40; j=(1<<n)-1
    cols=[]
    for c in range(n):
        m=0
        for r in np.flatnonzero(Astar[:,c]): m|=1<<int(r)
        cols.append(m)
    edges=[(i,k) for i in range(n) for k in range(i+1,n) if Astar[i,k]]
    B9=rank_basis_int([cols[i]^cols[k] for i,k in edges]); V9=set(span(B9)); assert j in V9
    rep=lambda x:min(int(x),int(x)^j)
    reps={rep(x) for x in V9}
    q=lambda x:(rep(x).bit_count()//4)&1
    polar=lambda x,y:q(x)^q(y)^q(rep(x)^rep(y))
    singular=sorted(x for x in reps if x and q(x)==0)

    # Deterministic greedy hyperbolic basis, identical to Pass4649.
    hb=[]
    for _ in range(4):
        cand=[x for x in singular if x not in hb and all(polar(x,z)==0 for z in hb)]
        e=cand[0]
        f=next(y for y in singular if y!=e and all(polar(y,z)==0 for z in hb) and polar(e,y)==1)
        hb.extend([e,f])
    assert len(rank_basis_int(hb))==8
    coord_to_v={}; v_to_coord={}
    for c in range(256):
        x=0
        for i,b in enumerate(hb):
            if (c>>i)&1: x^=b
        rr=rep(x); coord_to_v[c]=rr; v_to_coord[rr]=c

    # Base anisotropic plane frozen by the Pass4649 pairwise PSp intersection.
    P0=frozenset((48,208,224))
    assert 48^208^224==0
    def qh(m):
        h=[(m>>i)&1 for i in range(8)]
        return (h[0]*h[1]+h[2]*h[3]+h[4]*h[5]+h[6]*h[7])&1
    def ph(x,y): return qh(x)^qh(y)^qh(x^y)
    assert all(qh(x)==1 for x in P0)

    def apply(p,c): return v_to_coord[permute_mask40(coord_to_v[c],p,j)]
    stab=[p for p in G if frozenset(apply(p,c) for c in P0)==P0]
    assert len(stab)==648
    pointwise=[p for p in stab if all(apply(p,c)==c for c in P0)]
    assert len(pointwise)==216

    # Recover the point permutation induced by a line permutation using the four
    # incident W33 lines through each point.
    incsets=[frozenset(li for li,L in enumerate(lines) if x in L) for x in range(40)]
    inc_lookup={S:i for i,S in enumerate(incsets)}
    def point_perm(p):
        return tuple(inc_lookup[frozenset(p[li] for li in incsets[x])] for x in range(40))
    pstab=[point_perm(p) for p in stab]
    fixed_points=[x for x in range(40) if all(pp[x]==x for pp in pstab)]
    fixed_lines=[l for l in range(40) if all(p[l]==l for p in stab)]
    assert len(fixed_points)==1 and fixed_lines==[]
    p0=fixed_points[0]

    # Orbit map gP0 -> gp0; well-definedness is checked on all 25920 elements.
    plane_to_point={}
    for p in G:
        P=frozenset(apply(p,c) for c in P0)
        y=point_perm(p)[p0]
        if P in plane_to_point: assert plane_to_point[P]==y
        else: plane_to_point[P]=y
    assert len(plane_to_point)==40 and len(set(plane_to_point.values()))==40

    # Exact graph transport.
    for P,Q in combinations(plane_to_point,2):
        x,y=plane_to_point[P],plane_to_point[Q]
        total_orth=all(ph(a,b)==0 for a in P for b in Q)
        assert total_orth==bool(A[x,y])

    out={
      'pass':4654,
      'base_plane':sorted(P0),
      'base_plane_setwise_stabilizer_order':648,
      'base_plane_pointwise_stabilizer_order':216,
      'fixed_W33_points':fixed_points,
      'fixed_W33_lines':fixed_lines,
      'orbit_size':40,
      'equivariant_bijection':'gP0 -> gp0',
      'target_carrier':'W33 point carrier',
      'not_target_carrier':'W33 line carrier',
      'graph_transport':'total polar orthogonality of anisotropic planes iff W33 point collinearity',
      'theorem':'The 40 anisotropic planes recovered from triality-conjugate PSp intersections are explicitly the W33 point G-set, not the inequivalent W33 line G-set.',
      'boundary':'Finite G-set/graph intertwiner. This preserves the odd-q point/line distinction and makes no physical identification.'
    }
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n',encoding='utf-8')
    print(json.dumps(out,indent=2,sort_keys=True)); return 0
if __name__=='__main__': raise SystemExit(main())
