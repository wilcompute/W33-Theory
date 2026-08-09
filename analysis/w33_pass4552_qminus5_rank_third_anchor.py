#!/usr/bin/env python3
"""Pass 4552 -- third exact Q^-(5,q) binary-rank anchor and literature-scope correction.

Pass 4537 found q=3 and q=7 anchors for the candidate laws
  rank_2 N = q^4+q^2+1,
  rank_2(N^T N)=(q^2+1)(q^2-q+1).
This pass independently constructs the elliptic quadric Q^-(5,5)=GQ(5,25)
and verifies the same formulas at q=5 using integer-bitset Gaussian elimination.

A literature audit also corrects a tempting but wrong route: the 1991
Bagchi--Brouwer--Wilbrink O(5,q) paper treats the dual of the square symplectic
GQ Sp(4,q), not the elliptic Q^-(5,q)=GQ(q,q^2) family.  It is therefore not
used as proof of this rank law.  The all-odd-q formula remains open here.
"""
from __future__ import annotations
import itertools,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS4552_QMINUS5_RANK_THIRD_ANCHOR.json'

def inv(a,q): return pow(int(a),-1,q)
def norm(v,q):
    v=tuple(int(x)%q for x in v)
    for x in v:
        if x:
            z=inv(x,q); return tuple((z*y)%q for y in v)
    raise ValueError

def nonsquare(q):
    sq={i*i%q for i in range(1,q)}
    return next(d for d in range(2,q) if d not in sq)

def Q(v,q,d): return (v[0]*v[1]+v[2]*v[3]+v[4]*v[4]-d*v[5]*v[5])%q
def B(x,y,q,d):
    return (x[0]*y[1]+x[1]*y[0]+x[2]*y[3]+x[3]*y[2]+2*x[4]*y[4]-2*d*x[5]*y[5])%q

def rank_int(rows):
    piv={}
    for x in rows:
        y=int(x)
        while y:
            p=y.bit_length()-1
            if p in piv:y^=piv[p]
            else:piv[p]=y;break
    return len(piv)

def build(q=5):
    d=nonsquare(q);pts=[]
    for lead in range(6):
        for tail in itertools.product(range(q),repeat=5-lead):
            v=(0,)*lead+(1,)+tail
            if Q(v,q,d)==0:pts.append(v)
    pidx={p:i for i,p in enumerate(pts)}; lines=set()
    for i,x in enumerate(pts):
        for y in pts[i+1:]:
            if B(x,y,q,d):continue
            L=set()
            for a,b in itertools.product(range(q),repeat=2):
                if a or b:L.add(pidx[norm(tuple((a*u+b*v)%q for u,v in zip(x,y)),q)])
            assert len(L)==q+1
            lines.add(tuple(sorted(L)))
    return pts,sorted(lines),d

def main():
    q=5;pts,lines,d=build(q)
    assert (len(pts),len(lines))==((q+1)*(q**3+1),(q*q+1)*(q**3+1))==(756,3276)
    rows=[0]*len(pts)
    for j,L in enumerate(lines):
        bit=1<<j
        for p in L:rows[p]|=bit
    rN=rank_int(rows); assert rN==q**4+q**2+1==651
    gram=[]
    for L in lines:
        x=0
        for p in L:x^=rows[p]
        gram.append(x)
    rho=rank_int(gram);assert rho==(q*q+1)*(q*q-q+1)==546
    c4537=json.loads((ROOT/'data/PART_W33_PASS4537_Q5Q_BINARY_RANK_FRONTIER.json').read_text())
    anchors={a['q']:(a['rank_N'],a['rank_NtN']) for a in c4537['exact_prime_field_anchors']}
    assert anchors=={3:(91,70),7:(2451,2150)}
    allanchors=[{'q':3,'rank_N':91,'rank_NtN':70},{'q':5,'rank_N':rN,'rank_NtN':rho},{'q':7,'rank_N':2451,'rank_NtN':2150}]
    for a in allanchors:
        z=a['q'];assert a['rank_N']==z**4+z**2+1;assert a['rank_NtN']==(z*z+1)*(z*z-z+1)
    out={'pass':4552,'exact_new_anchor':{'q':5,'nonsquare_d':d,'points':len(pts),'lines':len(lines),'rank_N':rN,'rank_NtN':rho},
      'three_exact_anchors':allanchors,
      'candidate_all_odd_q':{'rank_N':'q^4+q^2+1','rank_NtN':'(q^2+1)(q^2-q+1)','status':'OPEN beyond exact q=3,5,7 anchors'},
      'literature_scope_correction':{'paper':'Bagchi-Brouwer-Wilbrink, Geometriae Dedicata 39 (1991), 339-355','doi':'10.1007/BF00150760','correction':'Its O(5,q) is the dual of the square Sp(4,q) generalized quadrangle; it is not the elliptic Q^-(5,q)=GQ(q,q^2) family and is not evidence for this formula.'},
      'theorem':'Q^-(5,5) has binary incidence rank 651 and line-Gram rank 546, giving a third independent exact anchor for the Pass-4537 rank law.',
      'boundary':'The q=3,5,7 computations are exact. Three anchors are not an infinite proof; the closed odd-q rank formula remains open until the correct elliptic-quadric modular-rank theorem is supplied.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
