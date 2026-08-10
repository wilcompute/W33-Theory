#!/usr/bin/env python3
"""Pass 4629 bonkers -- full PGSp turns the three-spread packet into an S3 fiber.

Pass4624 identifies each 45-object protected support with a packet of three
maximal size-8 partial spreads.  Over PSp their common order-192 stabilizer H has
normalizer/support stabilizer 576 and quotient C3.  Here the outer similitude is
adjoined.  The full support stabilizer has order 1152 and induces all six
permutations of the three spreads, with kernel exactly H.  Thus its quotient is
S3; the PSp subgroup supplies A3=C3 and the outer coset supplies transpositions.
"""
from __future__ import annotations
import itertools,json
from collections import deque
from pathlib import Path
import numpy as np
from w33_pass4472_4479_apartment_module_thermo_ihara_pauli import build_geometry,build_line_perm,transvection_matrix,norm3
from w33_pass4587_w33_derived_d4_triality import rank_basis_int,span
from w33_pass4595_concrete_d4_triality_w33_lifts import max_generators,partial8

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS4629_FULL_OUTER_PACKET_S3_FIBER.json'

def compose(p,q):return tuple(p[q[i]] for i in range(len(p)))
def pair_group(gens):
    I=(tuple(range(40)),tuple(range(40)));S={I};Q=deque([I])
    while Q:
        a,b=Q.popleft()
        for x,y in gens:
            z=(compose(x,a),compose(y,b))
            if z not in S:S.add(z);Q.append(z)
    return S
def point_perm(M,pts,pidx):
    out=[]
    for p in pts:
        y=(np.asarray(M,dtype=int)@np.asarray(p,dtype=int))%3
        out.append(pidx[norm3(tuple(map(int,y)))])
    return tuple(out)
def pmask(mask,p):
    y=0
    for i in range(len(p)):
        if (mask>>i)&1:y|=1<<p[i]
    return y

def main()->int:
    pts,pidx,lines,lidx,_,Astar,_,_,_=build_geometry();Astar=np.asarray(Astar,dtype=np.uint8);j=(1<<40)-1
    cols=[]
    for c in range(40):
        m=0
        for r in np.flatnonzero(Astar[:,c]):m|=1<<int(r)
        cols.append(m)
    B=rank_basis_int([cols[i]^cols[k] for i,k in itertools.combinations(range(40),2) if Astar[i,k]])
    rep=lambda x:min(int(x),int(x)^j);q=lambda x:(rep(x).bit_count()//4)&1
    polar=lambda x,y:q(x)^q(y)^q(rep(x)^rep(y))
    singular=sorted(x for x in {rep(v) for v in span(B)} if x and q(x)==0)
    MG=max_generators(singular,rep,q,polar);assert len(MG)==270
    gens=[];PSp={(tuple(range(40)),tuple(range(40)))}
    for v in pts:
        M=transvection_matrix(v);z=(point_perm(M,pts,pidx),build_line_perm(M,pts,pidx,lines,lidx))
        trial=pair_group(gens+[z])
        if len(trial)>len(PSp):gens.append(z);PSp=trial
        if len(PSp)==25920:break
    actX=lambda X,g:frozenset(rep(pmask(x,g[1])) for x in X)
    rem=set(MG);orbits=[]
    while rem:
        X=next(iter(rem));O={actX(X,g) for g in PSp};orbits.append(O);rem-=O
    O135=[O for O in orbits if len(O)==135][0];X=min(O135,key=lambda z:tuple(sorted(z)))
    H=[g for g in PSp if actX(X,g)==X];assert len(H)==192
    P8=partial8(lines);unext=[]
    for S in P8:
        used=set().union(*(set(lines[i]) for i in S))
        if not any(used.isdisjoint(lines[k]) for k in range(40) if k not in S):unext.append(S)
    actS=lambda S,g:tuple(sorted(g[1][i] for i in S))
    fixed=[S for S in unext if all(actS(S,g)==S for g in H)];assert len(fixed)==3
    support=frozenset(set(range(40))-set().union(*(set(S) for S in fixed)));assert len(support)==16

    outer=np.diag([1,2,1,2])%3
    PGSp=pair_group(gens+[(point_perm(outer,pts,pidx),build_line_perm(outer,pts,pidx,lines,lidx))])
    assert len(PGSp)==51840
    stab=[g for g in PGSp if frozenset(g[1][i] for i in support)==support];assert len(stab)==1152
    index={S:i for i,S in enumerate(fixed)};perms=set();kernel=[]
    for g in stab:
        p=[];ok=True
        for S in fixed:
            z=actS(S,g)
            if z not in index:ok=False;break
            p.append(index[z])
        assert ok;pp=tuple(p);perms.add(pp)
        if pp==(0,1,2):kernel.append(g)
    assert len(perms)==6 and len(kernel)==192 and set(kernel)==set(H)
    even={p for p in perms if sum(p[i]>p[k] for i in range(3) for k in range(i+1,3))%2==0}
    assert len(even)==3
    inner_perms=set()
    for g in [z for z in PSp if frozenset(z[1][i] for i in support)==support]:
        inner_perms.add(tuple(index[actS(S,g)] for S in fixed))
    assert inner_perms==even
    out={'pass':4629,'fiber':{'base_objects':45,'fiber_size':3,'fiber_objects':'maximal size-8 partial spreads'},
      'PSp':{'support_stabilizer_order':576,'kernel_H_order':192,'quotient':'C3=A3','induced_permutations':3},
      'PGSp':{'support_stabilizer_order':1152,'kernel_H_order':192,'quotient':'S3','induced_permutations':6,'PSp_image_is_even_subgroup':True},
      'theorem':'The three-valued maximal-partial-spread lift of each protected/E6 45-object is a genuine S3 fiber under full PGSp: 1 -> H_192 -> Htilde_1152 -> S3 -> 1. Its PSp restriction is the C3=A3 deck rotation and the outer coset supplies transpositions.',
      'boundary':'Finite stabilizer/fiber theorem. The S3 is an actual induced permutation action on the three W33 partial spreads, not a physical family symmetry.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n',encoding='utf-8');print(json.dumps(out,indent=2,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
