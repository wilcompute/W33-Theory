#!/usr/bin/env python3
"""Pass10565-10572: the reduced nine-state Fourier factor is not the Hesse F3^2 DFT.

The canonical selector Fourier factors as F3 tensor F35^C6.  It is tempting to
replace the nine-dimensional reduced factor by the ordinary two-qutrit Fourier
transform on F3^2.  This pass gives an exact obstruction.

For any finite abelian group DFT, F^2 is inversion.  On the nine C6-orbits of
C35 (multiplier 9), inversion fixes exactly three orbit-states.  On F3^2,
inversion x->-x fixes only zero, hence exactly one state.  Therefore the two
Fourier operators have different trace(F^2) and cannot be unitarily conjugate.

The nine arithmetic states also carry a canonical order stratification:
  order 1: 1 orbit, order 5: 2, order 7: 2, order 35: 4.
So 9 = 1+2+2+4 is intrinsic to the C35 arithmetic quotient.
"""
from __future__ import annotations
from collections import Counter
import json,math,cmath
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS10565_10572_REDUCED9_HESSE_FOURIER_NO_GO.json'

def orbits(n,m):
    seen=set();out=[]
    for s in range(n):
      if s in seen:continue
      O=[];x=s
      while x not in O:O.append(x);seen.add(x);x=m*x%n
      out.append(O)
    return out

def order_add(x,n):
    if x==0:return 1
    return n//math.gcd(x,n)

def main():
    O=orbits(35,9);assert len(O)==9
    oid={x:i for i,C in enumerate(O) for x in C}
    neg=[oid[(-C[0])%35] for C in O]
    fixed=sum(i==j for i,j in enumerate(neg));assert fixed==3
    strata=Counter(order_add(C[0],35) for C in O)
    assert strata==Counter({35:4,5:2,7:2,1:1})
    # On F3^2, x=-x iff 2x=0; characteristic 3 implies x=0 only.
    hesse_fixed=1
    assert fixed!=hesse_fixed

    # Numerical spectral fingerprints as an independent check.
    z=cmath.exp(2j*math.pi/35);F=np.zeros((9,9),complex)
    for i,A in enumerate(O):
      for j,B in enumerate(O):F[i,j]=sum(z**(a*b) for a in A for b in B)/math.sqrt(35*len(A)*len(B))
    roots=[1,-1,1j,-1j];cnt=Counter()
    for w in np.linalg.eigvals(F):cnt[str(roots[int(np.argmin([abs(w-r) for r in roots]))])]+=1
    assert cnt==Counter({'1':3,'-1':3,'1j':2,'(-0-1j)':1})

    out={
      'schema':'w33.pass10565_10572.reduced9_hesse_fourier_no_go.v1','status':'PASS','passes':'10565-10572',
      'arithmetic9':{'carrier':'C35 / <x->9x> orbit states','dimension':9,'orbit_lengths':dict(Counter(map(len,O))),'element_order_strata':{'1':1,'5':2,'7':2,'35':4},'Fourier_square':'negation','negation_fixed_states':3,'Fourier_eigenvalue_multiplicities':{'1':3,'-1':3,'i':2,'-i':1}},
      'Hesse_two_qutrit':{'carrier':'F3^2','dimension':9,'Fourier':'F3 tensor F3','Fourier_square':'negation','negation_fixed_states':1},
      'no_go':'Different traces of Fourier-square (3 versus 1) are unitary-conjugacy invariants, so F35^C6 is not unitarily equivalent to F3 tensor F3.',
      'architecture':'The canonical 27-state selector is one genuine qutrit Fourier factor F3 tensored with an arithmetic nine-state factor; it is not the standard three-qutrit product Fourier transform.',
      'boundary':'The no-go is exact. Fourier eigenvalue multiplicities of the arithmetic factor are additionally checked numerically from the explicit orbit-sum matrix.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','arithmetic9':'1+2+2+4','trace_F2':[3,1],'three_qutrit_product':False}))
if __name__=='__main__':main()
