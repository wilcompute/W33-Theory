#!/usr/bin/env python3
"""Pass10629-10636: classify the C5-even and C7/C3 harmonic factors as rank-3 association schemes.

The 3x3x3 harmonic tensor cube has one literal C3 Fourier factor and two other
three-dimensional factors.  This pass identifies those two factors exactly.

C5 inversion scheme on Z/5:
  R0={0}, R1={+/-1}, R2={+/-2}
  A1^2=2I+A2, A2^2=2I+A1, A1A2=A1+A2.
  A1 has minimal polynomial (x-2)(x^2+x-1), hence the golden field Q(sqrt5).

C7 Singer scheme on Z/7 with D={1,2,4}, -D={3,5,6}:
  A^2=A+2A^T, (A^T)^2=2A+A^T, AA^T=3I+A+A^T.
  A has minimal polynomial (x-3)(x^2+x+2), with Gauss periods
  (-1 +/- sqrt(-7))/2.  The Hermitian observable (A-A^T)/i has three real
  eigenvalues 0,+sqrt7,-sqrt7.

Both are qutrit-sized commutative relation algebras, but neither is unitarily
equivalent to a standard qutrit Pauli operator by spectrum.
"""
from __future__ import annotations
import json
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS10629_10636_LOCAL_THREE_STATE_ASSOCIATION_SCHEMES.json'

def circ(n,S):
    A=np.zeros((n,n),dtype=np.int64)
    for x in range(n):
      for s in S:A[x,(x+s)%n]=1
    return A

def main():
    I5=np.eye(5,dtype=np.int64);A1=circ(5,{1,4});A2=circ(5,{2,3})
    assert np.array_equal(A1@A1,2*I5+A2)
    assert np.array_equal(A2@A2,2*I5+A1)
    assert np.array_equal(A1@A2,A1+A2)
    # Exact polynomial (A1-2I)(A1^2+A1-I)=0.
    assert not np.any((A1-2*I5)@(A1@A1+A1-I5))

    I7=np.eye(7,dtype=np.int64);A=circ(7,{1,2,4});B=A.T
    assert np.array_equal(A@A,A+2*B)
    assert np.array_equal(B@B,2*A+B)
    assert np.array_equal(A@B,3*I7+A+B)
    assert not np.any((A-3*I7)@(A@A+A+2*I7))

    out={
      'schema':'w33.pass10629_10636.local_three_state_association_schemes.v1','status':'PASS','passes':'10629-10636',
      'C5_even':{
        'carrier':'Z/5 with relations 0, +/-1, +/-2','dimension':3,
        'multiplication':['A1^2=2I+A2','A2^2=2I+A1','A1A2=A1+A2'],
        'generator_minimal_polynomial':'(x-2)(x^2+x-1)',
        'generator_spectrum':['2','(sqrt5-1)/2','-(sqrt5+1)/2'],
        'quadratic_field':'Q(sqrt5)'},
      'C7_Singer':{
        'carrier':'Z/7 with relations 0, D={1,2,4}, -D={3,5,6}','dimension':3,
        'multiplication':['A^2=A+2A^T','(A^T)^2=2A+A^T','AA^T=3I+A+A^T'],
        'generator_minimal_polynomial':'(x-3)(x^2+x+2)',
        'generator_spectrum':['3','(-1+sqrt(-7))/2','(-1-sqrt(-7))/2'],
        'Hermitian_skew_observable':'(A-A^T)/i','Hermitian_skew_spectrum':['0','sqrt7','-sqrt7'],
        'quadratic_field':'Q(sqrt(-7))'},
      'qutrit_comparison':{
        'literal_C3_factor':'the third factor from Pass10573 is an actual 3-point Fourier/qutrit carrier',
        'C5_and_C7':'three-dimensional arithmetic relation algebras / three-level observables',
        'standard_Pauli_equivalence':False,
        'reason':'their generator spectra are not cube roots of unity and are unitary-conjugacy invariants'},
      'theorem':'The 3-5-7 harmonic tensor cube contains one literal qutrit Fourier factor and two qutrit-sized rank-3 association schemes. The C5 factor is the pentagon distance algebra over Q(sqrt5); the C7 factor is the Singer/Fano directed scheme over Q(sqrt(-7)), with a canonical Hermitian three-level observable of spectrum 0,+/-sqrt7.',
      'boundary':'Exact finite association-algebra identities. Qutrit-sized means dimension three; no physical qutrit implementation or Pauli equivalence is claimed for the C5/C7 factors.'
    }
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps({'status':'PASS','local_factors':['C5 golden rank3','C7 Fano rank3']}))
if __name__=='__main__':main()
