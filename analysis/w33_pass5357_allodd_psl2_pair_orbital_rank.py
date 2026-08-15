#!/usr/bin/env python3
"""Pass5357: all-odd orbital-rank formula for the canonical PSL2(q) pair space.

Let Omega=P^1(F_q), Lambda=C(Omega,2), q odd, and H=Stab({0,infinity}) in
PSL2(q). Then H=N(T_split) is dihedral of order q-1. Writing m=(q-1)/2,
Burnside's lemma gives

  rank = (3m+5+delta)/2, delta=1 if m is even and 0 otherwise,

hence rank=(3q+9)/4 for q=1 mod4 and (3q+7)/4 for q=3 mod4.

For prime anchors the verifier realizes H using r:x->a^2 x and s:x->-1/x,
enumerates H-orbits on unordered pairs, and checks the fixed-pair Burnside sum.
The all-q statement concerns the canonical incident-line pair space; at q=5 that
space is the local K0 fiber of Pass5336, but no all-q K0-shell theorem is assumed.
"""
from __future__ import annotations
import json
from itertools import combinations
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5357_ALLODD_PSL2_PAIR_ORBITAL_RANK.json'
INF=-1

def primitive_root(p):
    phi=p-1; factors=[]; x=phi; d=2
    while d*d<=x:
        if x%d==0:
            factors.append(d)
            while x%d==0:x//=d
        d+=1
    if x>1:factors.append(x)
    for a in range(2,p):
        if all(pow(a,phi//r,p)!=1 for r in factors):return a
    raise AssertionError('no primitive root')

def rmap(x,p,a2):return INF if x==INF else a2*x%p

def smap(x,p):
    if x==INF:return 0
    if x==0:return INF
    return (-pow(x,-1,p))%p

def compose(g,h):return tuple(g[h[i]] for i in range(len(g)))

def power(g,k):
    out=tuple(range(len(g)))
    for _ in range(k):out=compose(g,out)
    return out

def predicted_rank(q):
    assert q%2==1
    return (3*q+9)//4 if q%4==1 else (3*q+7)//4

def anchor(p):
    pts=list(range(p))+[INF]; idx={x:i for i,x in enumerate(pts)}
    a=primitive_root(p); a2=a*a%p
    r=tuple(idx[rmap(x,p,a2)] for x in pts); s=tuple(idx[smap(x,p)] for x in pts)
    m=(p-1)//2; rotations=[power(r,k) for k in range(m)]
    H=set(rotations); H.update(compose(s,g) for g in rotations); assert len(H)==p-1
    pairs=list(combinations(range(p+1),2)); pind={P:i for i,P in enumerate(pairs)}
    pairperms=[]; fixed=[]
    for g in H:
        pg=tuple(pind[tuple(sorted((g[a0],g[b0])))] for a0,b0 in pairs)
        pairperms.append(pg); fixed.append(sum(pg[i]==i for i in range(len(pairs))))
    unseen=set(range(len(pairs))); orbits=[]
    while unseen:
        x=min(unseen); O={g[x] for g in pairperms}; orbits.append(sorted(O)); unseen-=O
    rank=len(orbits); burnside=sum(fixed)//len(H); assert rank==burnside==predicted_rank(p)
    delta=int(m%2==0)
    assert sum(fixed)==len(pairs)+(m-1)+delta*m+m*(m+1)
    return {'q':p,'m':m,'H_order':len(H),'fiber_size':len(pairs),'orbital_rank':rank,
      'subdegrees':sorted(map(len,orbits)),'fixed_pair_sum':sum(fixed),'burnside_rank':burnside,'q_mod_4':p%4}

def main():
    checked=[]
    for q in range(3,102,2):
        r=predicted_rank(q);m=(q-1)//2;delta=int(m%2==0);assert 2*r==3*m+5+delta;checked.append(q)
    anchors={str(p):anchor(p) for p in (3,5,7,11,13,17,19,23)}
    out={'pass':5357,'status':'THEOREM_ALLODD_CANONICAL_PAIR_SPACE_ORBITAL_RANK_FORMULA',
      'domain':'odd prime powers q','rank_formula':{'q=1 mod4':'(3q+9)/4','q=3 mod4':'(3q+7)/4'},
      'burnside_proof':'For m=(q-1)/2, H=N(T_split) has order 2m. Identity contributes |Lambda|; nonidentity rotations contribute the base pair, with m extra pairs for the unique rotational involution iff m is even; each of m reflections fixes m+1 pairs.',
      'prime_anchor_orbit_checks':anchors,
      'arithmetic_formula_check':{'odd_q_from':checked[0],'odd_q_through':checked[-1],'count':len(checked)},
      'q5_recovery':'The formula gives rank 6 at q=5, agreeing with Pass5336.',
      'consequence':'The q=5 rank-6 local algebra belongs to a growing all-odd Hecke-algebra family, not a uniform rank-6 object.',
      'boundary':'For general q this is the canonical incident-line pair space, not an all-q minimum-K0-shell assertion. Orbital rank alone does not give an all-q Wedderburn decomposition or the binary footprint rank theorem.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True))
if __name__=='__main__':main()
