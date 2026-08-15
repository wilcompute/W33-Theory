#!/usr/bin/env python3
"""Pass5294: close every three-cell Hoffman shortening orbit at distance 40.

Pass5264 showed any shortened word below40 needs at least three Hoffman cells.
The setwise stabilizer of the 13-cell cover in PSp4(5) has order576 and has only
six orbits on 3-subsets.  Their (orbit size, span rank) pairs are
(16,25),(18,28),(12,28),(48,30),(144,30),(48,30).

This producer reconstructs those orbit representatives and emits a compact C++
Gray-code enumerator.  Exhausting 2^rank words for one representative of each
orbit gives minimum40 in all six cases.  Hence every shortened word below40
must require at least four cover cells.
"""
from __future__ import annotations
import argparse,itertools,json
from pathlib import Path
from sympy.combinatorics import Permutation,PermutationGroup
from analysis.w33_pass5074_gauge_active_chart_tester import build_W
from analysis.w33_pass5214_q5_connectedL_point_footprint_gluing import p_component_assignment

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5294_HOFFMAN_TRIPLE_ORBIT_CLOSURE.json'
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
        P=sorted(blocks[c]);a=F[P[0]]
        cells.append(basis([a^F[p] for p in P[1:]]))
    assert set(map(len,cells))=={10} and len(basis(sum(cells,[])))==52

    pts=G['pts'];pidx={p:i for i,p in enumerate(pts)};bk={tuple(sorted(B)):i for i,B in enumerate(blocks)}
    def norm(v):
        for x in v:
            if x:
                s=pow(x,-1,5);return tuple(s*y%5 for y in v)
        raise ValueError
    def sp(u,v):return (u[0]*v[2]-u[2]*v[0]+u[1]*v[3]-u[3]*v[1])%5
    def bperm(v):
        pp=[]
        for x in pts:
            a=sp(x,v);pp.append(pidx[norm(tuple((x[k]+a*v[k])%5 for k in range(4)))])
        return [bk[tuple(sorted(pp[p] for p in B))] for B in blocks]
    gens=[Permutation(bperm(v)) for v in ((1,0,0,0),(0,1,0,0),(0,0,1,0),(0,0,0,1),(1,1,0,0),(1,0,0,1))]
    GP=PermutationGroup(gens);assert GP.order()==4680000
    C=set(COVER);base,strong=GP.schreier_sims_incremental(base=list(COVER))
    def prop(g):return {g(i) for i in COVER}==C
    tests=[]
    for l in range(len(base)):
        inds=base[:l+1];tests.append(lambda words,l=l,inds=inds:all((i in C)==(words[l](i) in C) for i in inds))
    H=GP.subgroup_search(prop,base=base,strong_gens=strong,tests=tests);assert H.order()==576
    ci={c:i for i,c in enumerate(COVER)}
    hgens=[[ci[g(c)] for c in COVER] for g in H.generators]
    def orbit(T):
        T=tuple(sorted(T));seen={T};Q=[T]
        while Q:
            s=Q.pop()
            for g in hgens:
                t=tuple(sorted(g[i] for i in s))
                if t not in seen:seen.add(t);Q.append(t)
        return seen
    rem=set(itertools.combinations(range(13),3));orbs=[]
    while rem:
        O=orbit(next(iter(rem)));rem-=O;T=next(iter(O));B=basis(sum((cells[i] for i in T),[]));orbs.append((len(O),T,B))
    sig=sorted((n,len(B)) for n,T,B in orbs)
    assert sig==sorted([(16,25),(18,28),(12,28),(48,30),(144,30),(48,30)])
    return orbs

def emit_cpp(orbs,path):
    s=['#include <bits/stdc++.h>\nusing namespace std; int main(){\n']
    for osz,T,B in orbs:
        W=[[(x>>(64*k))&((1<<64)-1) for k in range(6)] for x in B]
        s.append('{\nstatic const unsigned long long B[%d][6]={\n'%len(B))
        for w in W:s.append('{'+','.join(str(x)+'ULL' for x in w)+'},\n')
        s.append('}; unsigned long long cur[6]={0,0,0,0,0,0},prev=0; int best=999;\n')
        s.append('for(unsigned long long i=1;i<(1ULL<<%d);++i){auto g=i^(i>>1),d=g^prev;int b=__builtin_ctzll(d);prev=g;for(int k=0;k<6;k++)cur[k]^=B[b][k];int w=0;for(int k=0;k<6;k++)w+=__builtin_popcountll(cur[k]);best=min(best,w);}\n'%len(B))
        s.append('cout<<"%d %d %d %d %d "<<best<<"\\n";}\n'%(osz,T[0],T[1],T[2],len(B)))
    s.append('}\n');Path(path).write_text(''.join(s))

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--emit-cpp');ap.add_argument('--certificate');args=ap.parse_args()
    O=construct()
    if args.emit_cpp:emit_cpp(O,args.emit_cpp)
    expected=sorted((n,len(B),40) for n,T,B in O)
    if args.certificate:
        got=[]
        for ln in Path(args.certificate).read_text().splitlines():
            a,i,j,k,r,m=map(int,ln.split());got.append((a,r,m))
        assert sorted(got)==expected
    out={'pass':5294,'status':'THEOREM_HOFFMAN13_ALL_THREE_CELL_SPANS_HAVE_MINIMUM40',
      'cover_stabilizer_order':576,
      'triple_orbits':[{'orbit_size':n,'representative':list(T),'rank':len(B),'minimum':40} for n,T,B in sorted(O)],
      'conclusion':'Every shortened word of weight<40 requires at least four Hoffman cells.',
      'shortened_code':'[312,52,d]_2 with d in {28,32,36,40}; exact d remains open.',
      'replay':'Use --emit-cpp FILE; compile with g++ -O3; run to CERT; rerun producer with --certificate CERT.',
      'boundary':'Three-cell layer is exhaustive. Four-or-more-cell cancellation remains open.'}
    OUT.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
