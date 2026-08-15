#!/usr/bin/env python3
"""Pass5302: exact orbit reduction of the Hoffman four-cell shortening layer.

Pass5294 proved all <=3-cell spans have minimum 40.  The remaining C(13,4)=715
four-cell subsets collapse under the order-576 cover stabilizer to only ten
orbits.  Their exact (orbit size, span rank) data are frozen here.  This reduces
the first still-open shortening layer from 715 cases to ten representatives.

An optional MILP can look for words below 40 in representatives, but timeout or
noncompletion is NEVER promoted to a lower-bound certificate.  The exact
shortened distance remains open until all ten reps (and then >=5-cell effects, if
needed) are certified.
"""
from __future__ import annotations
import argparse,itertools,json
from pathlib import Path
from sympy.combinatorics import Permutation,PermutationGroup
from analysis.w33_pass5074_gauge_active_chart_tester import build_W
from analysis.w33_pass5214_q5_connectedL_point_footprint_gluing import p_component_assignment
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5302_HOFFMAN_FOURCELL_ORBIT_REDUCTION.json'
COVER=(6,30,73,111,128,140,157,189,193,226,254,277,320)

def basis(rows):
    piv={};B=[]
    for x in rows:
        y=x
        while y:
            p=y.bit_length()-1
            if p in piv:y^=piv[p]
            else:piv[p]=y;B.append(x);break
    return B

def construct():
    G=build_W(5);acid,nc=p_component_assignment(G);assert nc==325
    blocks=[set() for _ in range(325)]
    for a,A in enumerate(G['apartments']):blocks[acid[a]].update(A)
    F=[]
    for p in range(156):
        z=0
        for c,B in enumerate(blocks):
            if p in B:z|=1<<c
        F.append(z)
    cells=[]
    for c in COVER:
        P=sorted(blocks[c]);a=F[P[0]];cells.append(basis([a^F[p] for p in P[1:]]))
    pts=G['pts'];pi={p:i for i,p in enumerate(pts)};bk={tuple(sorted(B)):i for i,B in enumerate(blocks)}
    def norm(v):
        for x in v:
            if x:
                s=pow(x,-1,5);return tuple(s*y%5 for y in v)
        raise ValueError
    def sp(u,v):return (u[0]*v[2]-u[2]*v[0]+u[1]*v[3]-u[3]*v[1])%5
    def bperm(v):
        pp=[]
        for x in pts:
            a=sp(x,v);pp.append(pi[norm(tuple((x[k]+a*v[k])%5 for k in range(4)))])
        return [bk[tuple(sorted(pp[p] for p in B))] for B in blocks]
    vs=((1,0,0,0),(0,1,0,0),(0,0,1,0),(0,0,0,1),(1,1,0,0),(1,0,0,1))
    GP=PermutationGroup([Permutation(bperm(v)) for v in vs]);assert GP.order()==4680000
    C=set(COVER);base,strong=GP.schreier_sims_incremental(base=list(COVER))
    def prop(g):return {g(i) for i in COVER}==C
    tests=[]
    for l in range(len(base)):
        inds=base[:l+1];tests.append(lambda words,l=l,inds=inds:all((i in C)==(words[l](i) in C) for i in inds))
    H=GP.subgroup_search(prop,base=base,strong_gens=strong,tests=tests);assert H.order()==576
    ci={c:i for i,c in enumerate(COVER)};hgens=[[ci[g(c)] for c in COVER] for g in H.generators]
    def orbit(T):
        T=tuple(sorted(T));seen={T};Q=[T]
        while Q:
            s=Q.pop()
            for g in hgens:
                t=tuple(sorted(g[i] for i in s))
                if t not in seen:seen.add(t);Q.append(t)
        return seen
    rem=set(itertools.combinations(range(13),4));out=[]
    while rem:
        O=orbit(next(iter(rem)));rem-=O;T=min(O);B=basis(sum((cells[i] for i in T),[]));out.append((len(O),len(B),T))
    return sorted(out)

def main():
    O=construct();want=sorted([(3,33),(12,33),(16,35),(144,35),(96,38),(144,38),(36,39),(48,40),(72,40),(144,40)])
    assert sorted((a,r) for a,r,T in O)==want and sum(a for a,r,T in O)==715
    out={'pass':5302,'status':'THEOREM_HOFFMAN13_FOURCELL_LAYER_HAS_TEN_ORBITS',
      'cover_stabilizer_order':576,'four_subsets':715,'orbits':len(O),
      'orbit_rank_data':[{'orbit_size':a,'rank':r,'representative':list(T)} for a,r,T in O],
      'rank_histogram':{'33':15,'35':160,'38':240,'39':36,'40':264},
      'consequence':'After Pass5294, any shortened word below40 must occur in the >=4-cell layer; at exactly four cells only ten symmetry representatives remain.',
      'search_note':'A rank33 representative admits a weight40 word. Bounded MILP searches for <=36 timed out without a feasible word and without an infeasibility certificate, so they are not evidence for d=40.',
      'boundary':'Exact orbit/rank reduction only. The shortened [312,52] distance remains in {28,32,36,40}.'}
    OUT.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
