#!/usr/bin/env python3
"""Pass5130: all-odd-q binary Levi bicycle theorem.

Prior art (Sin--Xiang, arXiv:cs/0506011, together with the full symplectic-GQ
incidence rank quoted there) gives, for odd prime powers q,
    rank_2 N = 1 + q(q+1)^2/2
for the W(3,q) point-line incidence matrix N.  Pass5124 gives the Levi linear
algebra: since q+1 is even, BB^T mod2 has off-diagonal blocks N,N^T and
Bike_2(Levi)=2 null_2(N)-1.  Hence Bike=q^3+q-1 for every odd prime power q.
The executable section independently rebuilds q=3,5,7,11 prime anchors.
"""
from __future__ import annotations
import itertools,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5130_ODDQ_BICYCLE_THEOREM.json'

def rank_bits(rows):
    piv={}
    for r0 in rows:
        r=r0
        while r:
            p=r.bit_length()-1
            if p in piv:r^=piv[p]
            else:piv[p]=r;break
    return len(piv)

def incidence_rank(q):
    def norm(v):
        for a in v:
            if a%q:
                z=pow(a,-1,q);return tuple((z*x)%q for x in v)
        raise ValueError
    pts=sorted({norm(v) for v in itertools.product(range(q),repeat=4) if any(v)});pi={p:i for i,p in enumerate(pts)}
    def s(x,y):return (x[0]*y[2]-x[2]*y[0]+x[1]*y[3]-x[3]*y[1])%q
    def span(x,y):
        S=set()
        for a,b in itertools.product(range(q),repeat=2):
            if a or b:S.add(norm(tuple((a*x[i]+b*y[i])%q for i in range(4))))
        return frozenset(pi[z] for z in S)
    lines=set()
    for i,j in itertools.combinations(range(len(pts)),2):
        if s(pts[i],pts[j])==0:lines.add(span(pts[i],pts[j]))
    lines=sorted(lines,key=lambda z:tuple(sorted(z)));rows=[]
    for p in range(len(pts)):
        z=0
        for l,L in enumerate(lines):
            if p in L:z|=1<<l
        rows.append(z)
    return len(pts),rank_bits(rows)

def main():
    A={}
    for q in (3,5,7,11):
        v,r=incidence_rank(q);formula=1+q*(q+1)**2//2
        assert r==formula
        null=v-r;bike=2*null-1;assert bike==q**3+q-1
        A[str(q)]={'points_lines':v,'rank_F2':r,'nullity_F2':null,'Levi_bicycle_dimension':bike}
    out={'pass':5130,'status':'THEOREM_ALL_ODD_PRIME_POWER_LEVI_BICYCLE',
         'prior_art':'Sin--Xiang, On the dimensions of certain LDPC codes based on q-regular bipartite graphs, arXiv:cs/0506011; odd-q W(3,q) binary incidence-rank theorem.',
         'incidence_rank_formula':'rank_F2 N = 1 + q(q+1)^2/2',
         'incidence_nullity_formula':'null_F2 N = q(q^2+1)/2',
         'Levi_mechanism':'For odd q, q+1 is even and BB^T mod2=[[0,N],[N^T,0]], giving dim Bike_2(Levi)=2 null_F2(N)-1.',
         'bicycle_formula':'dim Bike_2(Levi)=q^3+q-1',
         'anchors':A,'connection':'q=3 gives Bike29 exactly.',
         'boundary':'The all-q statement is for odd prime powers. Even q follows a different incidence-rank law and is not covered by this formula.'}
    OUT.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
