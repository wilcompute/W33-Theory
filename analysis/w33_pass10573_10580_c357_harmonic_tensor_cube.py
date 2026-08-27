#!/usr/bin/env python3
"""Pass10573-10580: the 27-state selector is a canonical 3-5-7 harmonic tensor cube.

Use CRT C105 ~= C3 x C5 x C7.  The normalizer complement multiplier 79 has
residues

  79 mod3 = 1,
  79 mod5 = 4 = -1,
  79 mod7 = 2.

The induced C6 action is therefore trivial on C3, inversion C2 on C5, and the
order-three multiplier <2> on C7.  Since C6 ~= C2 x C3 and these actions are on
independent CRT factors,

 C[C105]^C6 ~= C[C3] tensor C[C5]^<-1> tensor C[C7]^<2>.

Each factor has dimension 3:
 C3: {0},{1},{2};
 C5/C2: {0},{1,4},{2,3};
 C7/C3: {0},{1,2,4},{3,5,6}.
Hence 27=3*3*3 canonically.

For the STANDARD C105 DFT the CRT idempotents are e3=70,e5=21,e7=15, giving
local kernel coefficients 2,1,1 respectively.  Thus the restricted Fourier
operator factors as

 F_105^C6 = F_3^(2) tensor (F_5)^{C2} tensor (F_7)^{C3}

under the CRT orbit bases.  This is a tensor cube of three-dimensional harmonic
sectors, but only the first factor is the ordinary C3 group algebra; the other
two are cyclotomic invariant sectors.
"""
from __future__ import annotations
from collections import Counter
import cmath,json,math
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS10573_10580_C357_HARMONIC_TENSOR_CUBE.json'

def orbits(n,m):
    seen=set();out=[]
    for s in range(n):
      if s in seen:continue
      O=[];x=s
      while x not in O:O.append(x);seen.add(x);x=m*x%n
      out.append(O)
    return out

def rf(n,O,u=1):
    z=cmath.exp(2j*math.pi/n);F=np.zeros((len(O),len(O)),complex)
    for i,A in enumerate(O):
      for j,B in enumerate(O):F[i,j]=sum(z**(u*a*b) for a in A for b in B)/math.sqrt(n*len(A)*len(B))
    return F

def classify(F):
    roots=[1,-1,1j,-1j];out=Counter()
    for w in np.linalg.eigvals(F):out[str(roots[int(np.argmin([abs(w-r) for r in roots]))])]+=1
    return out

def main():
    assert (79%3,79%5,79%7)==(1,4,2)
    assert pow(4,2,5)==1 and pow(2,3,7)==1
    O3=[[0],[1],[2]];O5=orbits(5,4);O7=orbits(7,2)
    assert O5==[[0],[1,4],[2,3]]
    assert O7==[[0],[1,2,4],[3,6,5]]
    assert len(O3)*len(O5)*len(O7)==27

    # CRT idempotents for C105 -> C3 x C5 x C7.
    e3,e5,e7=70,21,15
    assert (e3%3,e3%5,e3%7)==(1,0,0)
    assert (e5%3,e5%5,e5%7)==(0,1,0)
    assert (e7%3,e7%5,e7%7)==(0,0,1)
    assert (e3*e3)%105==e3 and (e5*e5)%105==e5 and (e7*e7)%105==e7
    units={'3':2,'5':1,'7':1}  # e_p^2/105 fractional coefficient mod 1.

    F3=rf(3,O3,2);F5=rf(5,O5,1);F7=rf(7,O7,1)
    for F in (F3,F5,F7):assert np.linalg.norm(F.conj().T@F-np.eye(3))<1e-10
    c3,c5,c7=map(classify,(F3,F5,F7))
    assert c3==Counter({'1':1,'-1':1,'(-0-1j)':1})
    assert c5==Counter({'1':2,'-1':1})
    assert c7==Counter({'1':1,'-1':1,'1j':1})

    FT=np.kron(np.kron(F3,F5),F7)
    full=classify(FT)
    assert full==Counter({'1':8,'-1':7,'1j':6,'(-0-1j)':6})
    assert np.linalg.norm(np.linalg.matrix_power(FT,4)-np.eye(27))<1e-10

    out={
      'schema':'w33.pass10573_10580.c357_harmonic_tensor_cube.v1','status':'PASS','passes':'10573-10580',
      'CRT':{'group':'C105 ~= C3 x C5 x C7','normalizer_multiplier_residues':{'3':1,'5':4,'7':2},'action':'trivial on C3; inversion C2 on C5; order-3 multiplier <2> on C7','idempotents':{'3':70,'5':21,'7':15},'Fourier_kernel_units':units},
      'three_factors':{
        'C3_qutrit':{'dimension':3,'orbits':O3,'Fourier_eigs':{'1':1,'-1':1,'-i':1}},
        'C5_even':{'dimension':3,'orbits':O5,'interpretation':'inversion-even functions on C5','Fourier_eigs':{'1':2,'-1':1}},
        'C7_C3_invariant':{'dimension':3,'orbits':O7,'interpretation':'functions invariant under multiplier 2 of order 3','Fourier_eigs':{'1':1,'-1':1,'i':1}}},
      'tensor_identity':'C[C105]^C6 ~= C[C3] tensor C[C5]^C2 tensor C[C7]^C3, dimensions 3 x 3 x 3 = 27',
      'Fourier_identity':'Under CRT orbit bases, standard F105 restricted to C6-invariants factors as F3^(2) tensor F5^C2 tensor F7^C3.',
      'full_fourier_eigenvalue_multiplicities':{'1':8,'-1':7,'i':6,'-i':6},
      'theorem':'The canonical 27-state normalizer carrier is an exact 3-5-7 harmonic tensor cube: one genuine C3 qutrit sector, one three-dimensional inversion-even C5 sector, and one three-dimensional C3-invariant C7 sector. The standard C105 Fourier transform factors across these three sectors with the exact CRT character coefficients (2,1,1).',
      'boundary':'Exact CRT/orbit-space factorization. Numerical matrices only verify the local and total Fourier eigenvalue labels; the tensor decomposition itself is finite-group algebra. The two C5/C7 factors are qutrit-sized harmonic sectors, not asserted to be physical qutrit Hilbert spaces.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','tensor':'3x3x3','primes':[3,5,7],'full_eigs':out['full_fourier_eigenvalue_multiplicities']}))
if __name__=='__main__':main()
