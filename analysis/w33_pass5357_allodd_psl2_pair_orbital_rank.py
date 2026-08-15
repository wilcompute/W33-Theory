#!/usr/bin/env python3
"""Pass5357: all-odd orbital-rank formula for the local PSL2(q) pair fiber.

Let Omega=P^1(F_q), Lambda=C(Omega,2), q odd, and let H be the stabilizer in
PSL2(q) of {0,infinity}. Then H=N(T_split) is dihedral of order q-1. Write
m=(q-1)/2, so |H|=2m. The orbital rank of PSL2(q) on Lambda equals the number
of H-orbits on Lambda.

Burnside gives an elementary closed formula. The identity fixes |Lambda| pairs.
Every nontrivial split-torus rotation fixes {0,infinity}; if m is even, its
unique involution fixes m additional pairs. Each of the m reflections fixes
m+1 unordered pairs (whether it has 0 or 2 fixed projective points). Hence

  rank = (3m+5+delta)/2,
  delta=1 if m even, 0 if m odd,

or equivalently

  rank = (3q+9)/4 for q=1 mod 4,
         (3q+7)/4 for q=3 mod 4.

The executable prime-anchor check realizes H inside PSL2(p) by
r:x->a^2 x and s:x->-1/x, enumerates H-orbits on two-subsets, and verifies the
Burnside fixed-pair census directly.
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

def rmap(x,p,a2):
    if x==INF:return INF
    return a2*x%p

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
    r=tuple(idx[rmap(x,p,a2)] for x in pts)
    s=tuple(idx[smap(x,p)] for x in pts)
    m=(p-1)//2
    rotations=[power(r,k) for k in range(m)]
    H=set(rotations)
    H.update(compose(s,g) for g in rotations)
    assert len(H)==p-1
    pairs=list(combinations(range(p+1),2)); pind={P:i for i,P in enumerate(pairs)}
    pairperms=[]; fixed=[]
    for g in H:
        pg=tuple(pind[tuple(sorted((g[a0],g[b0])))] for a0,b0 in pairs)
        pairperms.append(pg); fixed.append(sum(pg[i]==i for i in range(len(pairs))))
    unseen=set(range(len(pairs))); orbits=[]
    while unseen:
        x=min(unseen); O={g[x] for g in pairperms}; orbits.append(sorted(O)); unseen-=O
    rank=len(orbits); burnside=sum(fixed)//len(H)
    assert rank==burnside==predicted_rank(p)
    identity_pairs=len(pairs); delta=int(m%2==0)
    expected_sum=identity_pairs+(m-1)+delta*m+m*(m+1)
    assert sum(fixed)==expected_sum
    return {'q':p,'m':m,'H_order':len(H),'fiber_size':len(pairs),'orbital_rank':rank,
      'subdegrees':sorted(map(len,orbits)),'fixed_pair_sum':sum(fixed),
      'burnside_rank':burnside,'q_mod_4':p%4}

def main():
    formulas={}
    for q in range(3,102,2):
        r=predicted_rank(q);m=(q-1)//2;delta=int(m%2==0)
        assert 2*r==3*m+5+delta
        formulas[str(q)]={'q':q,'q_mod_4':q%4,'orbital_rank':r}
    anchors={str(p):anchor(p) for p in (3,5,7,11,13,17,19,23)}
    out={'pass':5357,'status':'THEOREM_ALLODD_LOCAL_PAIR_FIBER_ORBITAL_RANK_FORMULA',
      'domain':'odd prime powers q',
      'rank_formula':{'q=1 mod4':'(3q+9)/4','q=3 mod4':'(3q+7)/4'},
      'burnside_proof':'For m=(q-1)/2, H=N(T_split) has order 2m. Identity contributes |Lambda|; nonidentity rotations contribute the base pair, with m extra pairs for the unique rotational involution iff m is even; each of m reflections fixes m+1 pairs.',
      'prime_anchor_orbit_checks':anchors,'arithmetic_formula_checks_q3_to_q101':formulas,
      'consequence':'The q=5 local rank-6 algebra is the second member of a growing all-odd Hecke-algebra family, not a uniform rank-6 object.',
      'boundary':'This determines orbital rank only. It does not give an all-q Wedderburn decomposition or imply the global footprint rank theorem.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True))
if __name__=='__main__':main()
