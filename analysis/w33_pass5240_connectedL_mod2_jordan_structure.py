#!/usr/bin/env python3
"""Pass5240: exact GF(2) Jordan structure of the connected odd-q L graph at q=3,5.

Pass5216 gives the exact characteristic-zero factorization and Pass5221 gives
nullities of A and A+I over F2.  Modulo two, every q=3,5 characteristic factor
collapses to x or x+1.  Here we compute nullities of powers directly with
bitset matrix arithmetic.  This determines every Jordan block size.
"""
from __future__ import annotations
import json
from pathlib import Path
from analysis.w33_pass5074_gauge_active_chart_tester import build_W
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5240_CONNECTEDL_MOD2_JORDAN_STRUCTURE.json'

def graph_rows(q):
    G=build_W(q);L=[loc for t,loc in G['charts'] if t=='L'];own=[[] for _ in G['apartments']]
    for i,loc in enumerate(L):
        for a in loc.values():own[a].append(i)
    assert set(map(len,own))=={2}
    rows=[0]*len(L)
    for u,v in own:rows[u]|=1<<v;rows[v]|=1<<u
    return rows

def rank2(rows):
    piv={}
    for x in rows:
        while x:
            p=x.bit_length()-1
            if p in piv:x^=piv[p]
            else:piv[p]=x;break
    return len(piv)

def mul_rows(X,A):
    out=[]
    for x in X:
        y=0
        while x:
            b=x&-x;j=b.bit_length()-1;x-=b;y^=A[j]
        out.append(y)
    return out

def data(q,alg0,alg1):
    A=graph_rows(q);n=len(A);I=[1<<i for i in range(n)]
    A2=mul_rows(A,A);A3=mul_rows(A2,A);A4=mul_rows(A3,A)
    Apows=[A,A2,A3,A4]
    N1=[A[i]^I[i] for i in range(n)]
    N2=[A2[i]^I[i] for i in range(n)]                  # (A+I)^2=A^2+I
    N3=[A3[i]^A2[i]^A[i]^I[i] for i in range(n)]      # binomial coeffs 3=1 mod2
    N4=[A4[i]^I[i] for i in range(n)]                  # (A+I)^4=A^4+I
    znull=[n-rank2(X) for X in Apows]
    onull=[n-rank2(X) for X in (N1,N2,N3,N4)]
    assert znull[-1]==alg0 and onull[-1]==alg1
    def blocks(nulls,alg):
        inc=[nulls[0]]+[nulls[i]-nulls[i-1] for i in range(1,len(nulls))]
        # inc[j-1]=number of Jordan blocks of size >=j; stabilization at j=4.
        exact={}
        for j in range(1,4):exact[j]=inc[j-1]-inc[j]
        exact[4]=inc[3]
        assert sum(j*c for j,c in exact.items())==alg
        return {str(j):c for j,c in exact.items() if c}
    return {'q':q,'vertices':n,'algebraic_multiplicity_0':alg0,'algebraic_multiplicity_1':alg1,
            'nullity_A_powers_1_to_4':znull,'nullity_AplusI_powers_1_to_4':onull,
            'zero_primary_Jordan_blocks':blocks(znull,alg0),
            'one_primary_Jordan_blocks':blocks(onull,alg1)}

def main():
    q3=data(3,100,440);q5=data(5,3716,6034)
    assert q3['zero_primary_Jordan_blocks']=={'1':100}
    assert q3['one_primary_Jordan_blocks']=={'1':70,'2':22,'3':26,'4':62}
    assert q5['zero_primary_Jordan_blocks']=={'1':2156,'3':520}
    assert q5['one_primary_Jordan_blocks']=={'1':804,'2':1471,'3':48,'4':536}
    out={'pass':5240,'status':'THEOREM_EXACT_CONNECTEDL_MOD2_JORDAN_STRUCTURE_Q3_Q5',
      'q3':q3,'q5':q5,
      'q5_mod2_characteristic_polynomial':'x^3716 (x+1)^6034',
      'q3_mod2_characteristic_polynomial':'x^100 (x+1)^440',
      'interpretation':'The large Pass5221 modular radicals are now resolved into exact nilpotent Jordan chains. The real spectral sectors do not reduce semisimply mod2.',
      'boundary':'Exact q3/q5 modular theorem only; no all-odd-q block formula or direct distance consequence is claimed.'}
    OUT.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
