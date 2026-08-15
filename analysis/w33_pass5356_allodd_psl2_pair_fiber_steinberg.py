#!/usr/bin/env python3
"""Pass5356: all-odd local two-line fiber = Sym^2(Steinberg).

Let G=PSL_2(q), q odd, acting 2-transitively on Omega=P^1(F_q), |Omega|=q+1.
The local K0 fiber over a W(3,q) point is the set Lambda=C(Omega,2) of unordered
pairs of incident lines. The pair stabilizer is the normalizer of a split torus,
of order q-1, so Lambda ~= G/N_G(T_split) and |Lambda|=q(q+1)/2.

Over characteristic zero let V=C[Omega]. Since the projective-line action is
2-transitive, V=1+St with St the q-dimensional Steinberg representation. In
Sym^2(V), diagonal monomials e_x^2 form a copy of V and off-diagonal monomials
e_x e_y (x<y) form C[Lambda]. Semisimplicity therefore gives
C[Lambda] ~= Sym^2(St).

The executable part constructs PSL_2(p) on P^1(F_p) for p=3,5,7,11,13 and
checks the character identity chi_pairs(g)=(chi_St(g)^2+chi_St(g^2))/2 on every
group element. This is deliberately characteristic-zero only; no mod-2
footprint-rank conclusion is inferred.
"""
from __future__ import annotations
import json
from itertools import combinations
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5356_ALLODD_PSL2_PAIR_FIBER_STEINBERG.json'
INF=-1

def canonical_pm(M,p):
    M=tuple(x%p for x in M); neg=tuple((-x)%p for x in M)
    return min(M,neg)

def mobius(M,x,p):
    a,b,c,d=M
    X,Y=(a,c) if x==INF else ((a*x+b)%p,(c*x+d)%p)
    if Y%p==0:return INF
    return X*pow(Y,-1,p)%p

def psl2_permutations(p):
    pts=list(range(p))+[INF]; idx={x:i for i,x in enumerate(pts)}; mats=set()
    for a in range(p):
      for b in range(p):
       for c in range(p):
        if a:
            d=(1+b*c)*pow(a,-1,p)%p; mats.add(canonical_pm((a,b,c,d),p))
        elif b and c and (-b*c)%p==1:
            for d in range(p):mats.add(canonical_pm((a,b,c,d),p))
    perms={tuple(idx[mobius(M,x,p)] for x in pts) for M in mats}
    assert len(perms)==p*(p*p-1)//2
    return sorted(perms)

def compose(g,h):return tuple(g[h[i]] for i in range(len(g)))

def fixed_two_subsets(g):
    return sum(tuple(sorted((g[a],g[b])))==(a,b) for a,b in combinations(range(len(g)),2))

def anchor(p):
    G=psl2_permutations(p); n=p+1; profiles={}
    for g in G:
        g2=compose(g,g); chi=sum(g[i]==i for i in range(n))-1
        chi2=sum(g2[i]==i for i in range(n))-1
        sym=(chi*chi+chi2)//2; pair=fixed_two_subsets(g)
        assert pair==sym
        key=f'fixP1={chi+1},fixPairs={pair}'; profiles[key]=profiles.get(key,0)+1
    return {'q':p,'group_order':len(G),'projective_line_size':n,'steinberg_dimension':p,
      'pair_fiber_size':p*(p+1)//2,'split_torus_normalizer_order':p-1,
      'dimension_Sym2_Steinberg':p*(p+1)//2,'character_identity_checked_on_elements':len(G),
      'fixed_point_pair_profiles':profiles}

def main():
    arithmetic={}
    for q in (3,5,7,9,11,13,17,19,25):
        go=q*(q*q-1)//2; fib=q*(q+1)//2
        assert go//(q-1)==fib
        arithmetic[str(q)]={'q':q,'PSL2_order':go,'pair_fiber_size':fib,
          'pair_stabilizer_order':q-1,'Sym2_Steinberg_dimension':fib}
    anchors={str(p):anchor(p) for p in (3,5,7,11,13)}
    out={'pass':5356,'status':'THEOREM_ALLODD_LOCAL_PAIR_FIBER_IS_SYM2_STEINBERG_IN_CHARACTERISTIC_ZERO',
      'domain':'odd prime powers q',
      'homogeneous_space':'C(P^1(q),2) ~= PSL2(q)/N(T_split), |N(T_split)|=q-1',
      'module_theorem':'Over C, C[C(P^1(q),2)] ~= Sym^2(St_q).',
      'proof_spine':['C[P^1(q)] = 1 + St_q in characteristic zero.',
        'Sym^2(C[P^1(q)]) splits into diagonal and off-diagonal monomials.',
        'The diagonal module is C[P^1(q)] and the off-diagonal module is C[C(P^1(q),2)].',
        'Semisimplicity cancels 1+St_q from Sym^2(1+St_q)=1+St_q+Sym^2(St_q).'],
      'q5_recovery':'dim Sym^2(St_5)=15 and Pass5336 gives 15=1+4+2*5.',
      'arithmetic_checks':arithmetic,'prime_anchor_character_checks':anchors,
      'boundary':'Characteristic-zero representation theorem only. In characteristic 2 the projective-line permutation module is not split as 1+St in the same way; no binary footprint-rank equality is inferred.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True))
if __name__=='__main__':main()
