#!/usr/bin/env python3
"""Pass5106: rank-two root derivative/curvature calculus for A2,C2,G2."""
from __future__ import annotations
import itertools,json
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5106_RANK2_LIE_DERIVATIVE_CURVATURE.json'

ROOTS={
 'A2':{(1,0),(0,1),(1,1)},
 'C2':{(1,0),(0,1),(1,1),(2,1)},
 'G2':{(1,0),(0,1),(1,1),(2,1),(3,1),(3,2)},
}
HEIGHTS={'A2':[1,1,2],'C2':[1,1,2,3],'G2':[1,1,2,3,4,5]}

def add(a,b):return (a[0]+b[0],a[1]+b[1])
def additive_closure(pair,roots):
    S=set(pair);changed=True
    while changed:
        changed=False
        for a,b in itertools.product(list(S),repeat=2):
            c=add(a,b)
            if c in roots and c not in S:S.add(c);changed=True
    return frozenset(S)

def chevalley_magnitude(r,s,roots):
    if add(r,s) not in roots:return 0
    full=roots|{(-a,-b) for a,b in roots};p=0
    while (s[0]-(p+1)*r[0],s[1]-(p+1)*r[1]) in full:p+=1
    return p+1

def lie_closure_mod(pair,roots,p):
    S=set(pair);changed=True
    while changed:
        changed=False
        for r,s in itertools.combinations(list(S),2):
            c=chevalley_magnitude(r,s,roots);t=add(r,s)
            if c and c%p and t in roots and t not in S:S.add(t);changed=True
    return frozenset(S)

def hist_good(roots):return Counter(len(additive_closure(pair,roots)) for pair in itertools.combinations(sorted(roots),2))
def hist_mod(roots,p):return Counter(len(lie_closure_mod(pair,roots,p)) for pair in itertools.combinations(sorted(roots),2))

def main():
    expected={'A2':Counter({2:2,3:1}),'C2':Counter({2:4,3:1,4:1}),'G2':Counter({2:10,3:3,5:1,6:1})}
    good={}
    for typ,R in ROOTS.items():
        h=hist_good(R);assert h==expected[typ];N=len(R)
        good[typ]={'positive_roots':N,'root_heights':HEIGHTS[typ],'first_derivative':f'{N} q^{N-1}','pair_generated_root_count_histogram':{str(k):v for k,v in sorted(h.items())}}
    # Exact root-string magnitudes for positive G2 brackets.
    nonzero={}
    for r,s in itertools.combinations(sorted(ROOTS['G2']),2):
        c=chevalley_magnitude(r,s,ROOTS['G2'])
        if c:nonzero[f'{r}+{s}']={'sum':add(r,s),'magnitude':c}
    h2=hist_mod(ROOTS['G2'],2);h3=hist_mod(ROOTS['G2'],3);h5=hist_mod(ROOTS['G2'],5)
    assert h2==Counter({2:11,3:4}) and h3==Counter({2:12,3:2,4:1}) and h5==expected['G2']
    out={'pass':5106,'status':'THEOREM_RANK2_GOOD_CHARACTERISTIC_WITH_BAD_PRIME_LIE_SHADOW','good_characteristic':good,
         'curvature_polynomials':{'A2':'2 z^2 + z^3','C2':'4 z^2 + z^3 + z^4','G2':'10 z^2 + 3 z^3 + z^5 + z^6'},
         'G2_positive_bracket_structure_constants':nonzero,
         'G2_bad_prime_Lie_shadows':{'p2':{str(k):v for k,v in sorted(h2.items())},'p3':{str(k):v for k,v in sorted(h3.items())}},
         'interpretation':'First derivative counts root-subgroup cosets; second-direction composition is deformed by Chevalley commutators. The pair-closure histogram is a finite curvature signature.',
         'boundary':'The p=2,3 G2 entries are Lie-bracket shadows only; bad-characteristic group commutator formulas may retain higher divided terms. The good-characteristic group closure statement is for A2 all p, C2 odd p, and G2 p>3.'}
    OUT.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
