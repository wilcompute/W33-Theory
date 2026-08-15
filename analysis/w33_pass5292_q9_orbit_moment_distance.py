#!/usr/bin/env python3
"""Pass5292: q=9 dual-16 orbit closes footprint distance 81.

Extends Pass5287.  Reconstruct the 3321 P-component carriers over GF(9), build
PSp4(9) from symplectic transvections, compute the setwise stabilizer of the
explicit weight-16 dual support, and derive its orbit replication and pair
codegrees without enumerating the full 13.45M-word orbit.

The support stabilizer has order 128 in PSp4(9) (order 1,721,606,400), so the
orbit has 13,450,050 words.  Coordinate replication is 64,800.  A block
stabilizer has nontrivial orbital valencies 800,360,720,720,720.  The seed
contains 80,0,16,12,12 unordered pairs in those orbitals, yielding shell pair
codegrees 810,0,180,135,135.  Hence r/lambda_max=80=q^2-1 and the even-shell
moment lemma gives d>=81.  Point footprints have weight81, so
C_F(q=9)=[3321,369,81]_2.
"""
from __future__ import annotations
import itertools,json
from collections import Counter
from pathlib import Path
from sympy.combinatorics import Permutation,PermutationGroup

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5292_Q9_ORBIT_MOMENT_DISTANCE81.json'
WIT=(97,102,223,528,543,657,789,804,963,1656,2070,2292,2621,2670,2801,2910)

def add(x,y):return ((x%3+y%3)%3)+3*((x//3+y//3)%3)
def neg(x):return (-x%3)+3*((-(x//3))%3)
def sub(x,y):return add(x,neg(y))
def mul(x,y):
    a,b=x%3,x//3;c,d=y%3,y//3
    return ((a*c+2*b*d)%3)+3*((a*d+b*c)%3)
def inv(x):
    for y in range(1,9):
        if mul(x,y)==1:return y
    raise ValueError(x)
def smul(a,v):return tuple(mul(a,x) for x in v)
def vadd(u,v):return tuple(add(a,b) for a,b in zip(u,v))
def norm(v):
    for x in v:
        if x:return smul(inv(x),v)
    raise ValueError('zero')
def sp(u,v):
    z=0;z=add(z,mul(u[0],v[2]));z=sub(z,mul(u[2],v[0]));z=add(z,mul(u[1],v[3]));z=sub(z,mul(u[3],v[1]));return z

def build():
    pts=sorted({norm(v) for v in itertools.product(range(9),repeat=4) if any(v)})
    pi={p:i for i,p in enumerate(pts)};assert len(pts)==820
    lines={}
    for i,u in enumerate(pts):
        for j in range(i+1,len(pts)):
            v=pts[j];S={norm(v)}
            for a in range(9):S.add(norm(vadd(u,smul(a,v))))
            if len(S)==10:
                key=tuple(sorted(pi[x] for x in S));lines.setdefault(key,(u,v))
    assert len(lines)==7462
    carriers={}
    for H,(u,v) in lines.items():
        if sp(u,v)==0:continue
        Hp=tuple(i for i,x in enumerate(pts) if sp(x,u)==0 and sp(x,v)==0)
        C=tuple(sorted(set(H)|set(Hp)));assert len(C)==20;carriers[C]=1
    C=sorted(carriers);assert len(C)==3321
    bk={c:i for i,c in enumerate(C)}
    cols=[];rows=[0]*820
    for j,c in enumerate(C):
        z=0
        for p in c:z|=1<<p;rows[p]|=1<<j
        cols.append(z)
    return pts,pi,C,bk,cols,rows

def main():
    pts,pi,C,bk,cols,rows=build();n=len(C)
    def pperm(v):
        out=[]
        for x in pts:
            a=sp(x,v);out.append(pi[norm(vadd(x,smul(a,v)))])
        return out
    vs=[(1,0,0,0),(0,1,0,0),(0,0,1,0),(0,0,0,1),(1,1,0,0),(1,0,0,1),(1,3,0,0),(1,0,3,0),(0,1,0,3),(3,0,1,0)]
    gens=[]
    for v in vs:
        pp=pperm(v);gens.append(Permutation([bk[tuple(sorted(pp[p] for p in c))] for c in C]))
    G=PermutationGroup(gens);Gorder=G.order();assert Gorder==1721606400

    # Setwise stabilizer of the seed.  Put the 16 seed points first in the BSGS
    # so membership tests prune the subgroup search immediately.
    S=set(WIT);base,strong=G.schreier_sims_incremental(base=list(WIT))
    def prop(g):return {g(i) for i in WIT}==S
    tests=[]
    for l in range(len(base)):
        inds=base[:l+1]
        tests.append(lambda words,l=l,inds=inds:all((i in S)==(words[l](i) in S) for i in inds))
    H=G.subgroup_search(prop,base=base,strong_gens=strong,tests=tests)
    stab=H.order();assert stab==128
    orbit=Gorder//stab;assert orbit==13450050
    replication=orbit*16//n;assert replication==64800

    # Pair orbitals from a block stabilizer.  Strong generators fixing block0
    # generate the full point stabilizer when the BSGS begins at 0.
    b0,sg0=G.schreier_sims_incremental(base=[0]);stabgens=[g for g in sg0 if g(0)==0]
    unseen=set(range(n));orbs=[]
    while unseen:
        s=next(iter(unseen));O={s};Q=[s];unseen.remove(s)
        while Q:
            u=Q.pop()
            for g in stabgens:
                v=g(u)
                if v not in O:
                    O.add(v);unseen.discard(v);Q.append(v)
        orbs.append(O)
    assert sorted(map(len,orbs))==[1,360,720,720,720,800]
    rid={x:i for i,O in enumerate(orbs) for x in O}
    val={i:len(O) for i,O in enumerate(orbs)}
    seedpairs=Counter()
    for a,b in itertools.combinations(WIT,2):
        g=G.orbit_rep(a,0);seedpairs[rid[g(b)]]+=1
    # reorder nontrivial orbitals by valency then seed count for stable output
    rec=[]
    for i,O in enumerate(orbs):
        if 0 in O:continue
        cnt=seedpairs[i];tot=n*len(O)//2
        lam=orbit*cnt//tot
        rec.append((len(O),cnt,lam))
    rec=sorted(rec,key=lambda x:(x[0],-x[1],-x[2]))
    assert sorted(rec)==sorted([(800,80,810),(360,0,0),(720,16,180),(720,12,135),(720,12,135)])
    lmax=max(x[2] for x in rec);assert replication//lmax==80

    # Seed is a dual check and point rows have weight81 (Pass5287 anchors).
    z=0
    for j in WIT:z^=cols[j]
    assert z==0 and {r.bit_count() for r in rows}=={81}
    out={'pass':5292,'status':'THEOREM_Q9_FOOTPRINT_CODE_3321_369_81',
      'PSp4_9_order':Gorder,'seed_stabilizer_order':stab,'dual16_orbit_size':orbit,
      'coordinate_replication':replication,
      'pair_orbitals':[{'valency':v,'seed_pairs':c,'shell_codegree':l} for v,c,l in rec],
      'maximum_pair_codegree':lmax,'r_over_lambda':replication//lmax,
      'moment_conclusion':'Every primal word meets every orbit check evenly, so w>=1+r/lambda_max=81.',
      'footprint_code':'[3321,369,81]_2',
      'boundary':'The orbit suffices for primal d=81. Completeness/minimality of the entire weight-16 dual shell is not claimed.'}
    OUT.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
