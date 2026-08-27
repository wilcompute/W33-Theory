#!/usr/bin/env python3
"""Pass10549-10556: canonical Fourier transform on the C105/C6 normalizer carrier.

Pass10477-10484 identifies the 105 C13-cycle selector as a cyclic torsor C105,
with the order-six normalizer complement acting by multiplication by 79 mod105.
Since 79 == 1 mod3 and 79 == 9 mod35, the C6-invariant function space factors
through the canonical CRT decomposition C105 ~= C3 x C35:

    C[C105]^C6 ~= C[C3] tensor C[C35]^<x->9x>.

The STANDARD 105-point Fourier kernel acquires CRT unit coefficients.  With
idempotents e3=70 and e35=36, one has e3^2/105 = 2/3 mod Z and
e35^2/105 = 12/35 mod Z.  Thus the exact kernel factorization is the twisted
local product

    F_105^C6 = F_3^(2) tensor (F_35^(12))^C6

up to the canonical CRT basis identification.  These unit twists are just local
character-generator choices, but they matter for the individual eigenvalue
labels, so they are recorded explicitly.

The orbit counts are 27 = 3*9.  The normalized DFT of C105 commutes with the
multiplier action (the multiplier subgroup is closed under inversion), hence it
restricts to a unitary 27x27 transform on the invariant subspace.  Exactly,
F^2 is inversion/negation and F^4=I.  Negation fixes 3 quotient states and swaps
the remaining 24 in 12 pairs.

The displayed eigenvalue multiplicities are independently checked numerically
from the explicit orbit-sum matrix; the algebraic F^2/F^4 and CRT factorization
claims do not depend on floating point.
"""
from __future__ import annotations
from collections import Counter
import cmath,json,math
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS10549_10556_C105_INVARIANT_FOURIER.json'
N=105;M=79

def orbits(n,m):
    seen=set();out=[]
    for s in range(n):
      if s in seen:continue
      O=[];x=s
      while x not in O:O.append(x);seen.add(x);x=(m*x)%n
      out.append(O)
    return out

def restricted_fourier(n,obs,unit=1):
    z=cmath.exp(2j*math.pi/n);k=len(obs);F=np.zeros((k,k),complex)
    for i,A in enumerate(obs):
      for j,B in enumerate(obs):
        F[i,j]=sum(z**(unit*a*b) for a in A for b in B)/math.sqrt(n*len(A)*len(B))
    return F

def classify(F):
    roots=[1,-1,1j,-1j];cnt=Counter()
    for w in np.linalg.eigvals(F):cnt[str(roots[int(np.argmin([abs(w-r) for r in roots]))])]+=1
    return cnt

def main():
    assert pow(M,6,N)==1 and all(pow(M,k,N)!=1 for k in range(1,6))
    assert M%3==1 and M%35==9
    O=orbits(N,M);assert len(O)==27
    assert Counter(map(len,O))==Counter({6:12,3:6,2:6,1:3})
    O35=orbits(35,9);assert len(O35)==9
    assert Counter(map(len,O35))==Counter({6:4,3:2,2:2,1:1})
    assert len(O)==3*len(O35)

    # CRT idempotents and induced Fourier-character coefficients.
    e3,e35=70,36
    assert e3%3==1 and e3%35==0 and e35%3==0 and e35%35==1
    assert (e3*e3)%N==70 and (e35*e35)%N==36
    # 70/105=2/3 and 36/105=12/35.
    crt_units={'C3':2,'C35':12}

    oid={x:i for i,C in enumerate(O) for x in C}
    neg=np.array([oid[(-C[0])%N] for C in O],dtype=int)
    assert Counter(neg)==Counter(range(27))
    assert np.array_equal(neg[neg],np.arange(27))
    fixed=int(np.sum(neg==np.arange(27)));assert fixed==3

    F=restricted_fourier(N,O);I=np.eye(27)
    assert np.linalg.norm(F.conj().T@F-I)<1e-10
    P=np.zeros((27,27))
    for i,j in enumerate(neg):P[j,i]=1
    assert np.linalg.norm(F@F-P)<1e-10
    assert np.linalg.norm(np.linalg.matrix_power(F,4)-I)<1e-10
    cnt=classify(F)
    assert cnt==Counter({'1':8,'-1':7,'1j':6,'(-0-1j)':6})

    # Independent CRT spectral check with the required local unit twists.
    z3=cmath.exp(2j*math.pi/3)
    F3=np.array([[z3**(2*a*b) for b in range(3)] for a in range(3)],complex)/math.sqrt(3)
    F35=restricted_fourier(35,O35,unit=12)
    c3=classify(F3);c35=classify(F35);prod=Counter()
    roots=[1,-1,1j,-1j]
    def parse(k):return {'1':1,'-1':-1,'1j':1j,'(-0-1j)':-1j}[k]
    for a,ma in c3.items():
      for b,mb in c35.items():
        v=parse(a)*parse(b);r=roots[int(np.argmin([abs(v-x) for x in roots]))]
        prod[str(r)]+=ma*mb
    assert prod==cnt

    out={
      'schema':'w33.pass10549_10556.c105_invariant_fourier.v2','status':'PASS','passes':'10549-10556',
      'torsor':{'group':'C105','normalizer_multiplier':79,'factorization':'C105 ~= C3 x C35','multiplier_mod3':1,'multiplier_mod35':9},
      'orbit_space':{'dimension':27,'C6_orbit_lengths':dict(Counter(map(len,O))),'C35_orbits':9,'packet_factorization':'3 x 9'},
      'CRT_fourier':{'idempotents':{'C3':e3,'C35':e35},'local_kernel_units':crt_units,'exact_factorization':'F_105^C6 = F_3^(2) tensor (F_35^(12))^C6 under CRT orbit bases','interpretation':'unit coefficients record local character-generator choices; they must not be dropped when comparing Fourier eigenvalue labels'},
      'fourier':{'ambient':'normalized DFT on C[C105]','restriction':'C6-invariant subspace','unitary':True,'F_squared':'negation on the 27 orbit states','F_fourth':'identity','negation_fixed_states':3,'negation_transposed_pairs':12,'eigenvalue_multiplicities':{'1':8,'-1':7,'i':6,'-i':6}},
      'theorem':'The 27 normalizer states carry a canonical harmonic transform inherited from the C105 selector. Its normalized DFT is unitary of order four with square equal to negation. Under CRT the exact kernel factors into a twisted qutrit C3 Fourier factor (unit 2) and a twisted nine-dimensional C35/C6 factor (unit 12).',
      'boundary':'F^2, F^4, orbit counts and CRT unit coefficients are exact finite-group statements. Eigenvalue multiplicities are checked from explicit numerical orbit-sum matrices to 1e-10; no identification with H27 adjacency is made.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','dimension':27,'CRT_units':crt_units,'F_eigs':out['fourier']['eigenvalue_multiplicities']}))
if __name__=='__main__':main()
