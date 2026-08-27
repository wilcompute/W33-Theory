#!/usr/bin/env python3
"""Pass10645-10652: Fourier-conjugate the actual H(4)/(13:6) weighted transport into the canonical 3x3x3 harmonic basis.

Reads the repaired Pass10477 v2 artifact containing the exact 27x27 equitable
matrix R, orbit weights, and C3xC5xC7 tensor labels.  The natural Hilbert-space
operator is the reversible symmetrization S=D^(1/2) R D^(-1/2).  We construct
the normalized C105 DFT restricted to C6-orbit sums and compute T=F S F^dagger.

Results:
* F is unitary and F^4=I; T is Hermitian with the H4 spectrum.
* The global trivial harmonic state (0,0,0) is exactly isolated with eigenvalue20.
* T is otherwise dense (only 60/729 entries vanish numerically to 1e-10).
* No local factor is conserved: every off-diagonal 3x3 factor block has nonzero
  Frobenius norm for each of C3,C5,C7.
* Conjugate local sectors 1<->2 have equal block norms, the surviving exact
  charge/negation symmetry.

The block-norm tables are robust numerical cyclotomic evaluations; the isolation
of the trivial state follows exactly from regularity and character orthogonality.
"""
from __future__ import annotations
import json,cmath,math
from pathlib import Path
from fractions import Fraction
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS10645_10652_H4_HARMONIC_TENSOR_TRANSPORT.json'

def local_orbits(n,m):
    seen=set();out=[]
    for s in range(n):
      if s in seen:continue
      O=[];x=s
      while x not in O:O.append(x);seen.add(x);x=(m*x)%n
      out.append(tuple(O))
    return out

def main():
    q=json.loads((ROOT/'data/PART_W33_PASS10477_10484_H4_NORMALIZER_27STATE_QUOTIENT.json').read_text())
    R=np.array(q['quotient27']['matrix'],dtype=float)
    w=np.array(q['quotient27']['reversible_orbit_weights'],dtype=float)
    labels=[tuple(x) for x in q['cyclic_torsor']['state_tensor_labels_C3_C5_C7']]
    assert R.shape==(27,27) and len(set(labels))==27
    assert np.max(np.abs(np.diag(w)@R-R.T@np.diag(w)))<1e-12
    S=np.diag(np.sqrt(w))@R@np.diag(1/np.sqrt(w))
    assert np.max(np.abs(S-S.T))<1e-12

    o5=local_orbits(5,4);o7=local_orbits(7,2)
    assert o5==[(0,),(1,4),(2,3)] and o7==[(0,),(1,2,4),(3,6,5)]
    # Each tensor label (r,a,b) is exactly one C6=<79> orbit in C105.
    orbs=[]
    for r,a,b in labels:
      O=tuple(k for k in range(105) if k%3==r and k%5 in o5[a] and k%7 in o7[b])
      assert len(O) in (1,2,3,6)
      orbs.append(O)
    assert sorted(map(len,orbs))==sorted(map(int,w))

    z=cmath.exp(2j*math.pi/105)
    F=np.zeros((27,27),dtype=complex)
    for i,A in enumerate(orbs):
      for j,B in enumerate(orbs):
        F[i,j]=sum(z**((x*y)%105) for x in A for y in B)/math.sqrt(105*len(A)*len(B))
    assert np.max(np.abs(F.conj().T@F-np.eye(27)))<1e-10
    assert np.max(np.abs(np.linalg.matrix_power(F,4)-np.eye(27)))<1e-10
    T=F@S@F.conj().T
    assert np.max(np.abs(T-T.conj().T))<1e-10

    # Global trivial character is tensor label (0,0,0), isolated by regularity.
    j0=labels.index((0,0,0))
    assert abs(T[j0,j0]-20)<1e-9
    assert max(abs(T[j0,j]) for j in range(27) if j!=j0)<1e-9
    assert max(abs(T[j,j0]) for j in range(27) if j!=j0)<1e-9

    block_tables={}
    expected={
      'C3':np.array([[504,48,48],[48,57,72],[48,72,57]],dtype=float),
      'C5':np.array([[504,32,32],[32,33,128],[32,128,33]],dtype=float),
      'C7':np.array([[23592,2736,2736],[2736,2601,3504],[2736,3504,2601]],dtype=float)/49.0,
    }
    for fac,name in enumerate(('C3','C5','C7')):
      tab=np.zeros((3,3),dtype=float)
      for a in range(3):
        rr=[i for i,l in enumerate(labels) if l[fac]==a]
        for b in range(3):
          cc=[j for j,l in enumerate(labels) if l[fac]==b]
          tab[a,b]=float(np.linalg.norm(T[np.ix_(rr,cc)])**2)
      assert np.max(np.abs(tab-expected[name]))<1e-8
      assert min(tab[a,b] for a in range(3) for b in range(3) if a!=b)>1e-8
      block_tables[name]=[[str(Fraction(float(x)).limit_denominator(1000)) for x in row] for row in tab]

    zero_count=int(np.count_nonzero(np.abs(T)<1e-9))
    assert zero_count==60
    frob=float(np.linalg.norm(T)**2)
    assert abs(frob-954)<1e-8
    out={
      'schema':'w33.pass10645_10652.h4_harmonic_tensor_transport.v1','status':'PASS','passes':'10645-10652',
      'operator':'T=F D^(1/2) R D^(-1/2) F^dagger on the C3 x C5 x C7 harmonic tensor basis',
      'Fourier_checks':{'unitary_error_lt':'1e-10','F_fourth_error_lt':'1e-10'},
      'exact_selection_rule':{'trivial_tensor_state':'(0,0,0)','eigenvalue':20,'coupling_to_other_26':0},
      'support':{'matrix_entries':729,'numerically_zero_lt_1e-9':zero_count,'nonzero':729-zero_count,'Frobenius_norm_squared':954},
      'factor_block_Frobenius_squared':block_tables,
      'local_conservation':{'C3':False,'C5':False,'C7':False,'meaning':'every off-diagonal local-sector block has nonzero norm'},
      'surviving_symmetry':'for each local factor, sectors 1 and 2 have conjugate/equal block norms',
      'theorem':'In the canonical 3-5-7 harmonic tensor basis, the H(4)/(13:6) transport isolates only the global trivial harmonic state. All three local factors are otherwise coupled: the qutrit, pentagon, and Fano quantum numbers are not separately conserved. The harmonic tensor cube is therefore a natural coordinate system for a genuinely entangling finite transport, not a tensor-product decomposition of the H(4) dynamics.',
      'boundary':'R and the reversible symmetrization are exact. Fourier matrix and block norms are evaluated numerically from exact C105 orbit sums with 1e-8 verification against the displayed rational values; this pass does not claim those rational norms as a separate symbolic cyclotomic proof.'
    }
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','zero_entries':zero_count,'local_factors_conserved':False,'trivial_state_isolated':True}))
if __name__=='__main__':main()
