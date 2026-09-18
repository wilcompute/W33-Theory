#!/usr/bin/env python3
"""Non-Abelian S3 commutator Ramsey witness on the W33 logical doublet.

In the exact common normal form,
  z=diag(omega,omega^-1), X=swap.
The group commutator is
  K = X z X^-1 z^-1 = z^-2 = z
because X z X = z^-1 and z^3=I.

A Ramsey/interferometric test starts in
  |+>=(|r=1>+|r=2>)/sqrt(2).
If X and z commuted, the closed commutator loop would return |+> with
probability 1.  For the certified S3 relation,
  <+|K|+>=(omega+omega^-1)/2=-1/2,
so the X-basis return probability is exactly 1/4.

This provides a sharp physical witness for the non-Abelian outer action in any
rail implementation of the logical doublet.
"""
import cmath,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/w33_s3_commutator_ramsey_witness.json'

def mm(A,B):
    return [[sum(A[i][k]*B[k][j] for k in range(2)) for j in range(2)] for i in range(2)]
def dag(A):return [[A[j][i].conjugate() for j in range(2)] for i in range(2)]
def close(A,B,tol=1e-9):return all(abs(A[i][j]-B[i][j])<tol for i in range(2) for j in range(2))
def main(write=True):
    w=cmath.exp(2j*cmath.pi/3)
    z=[[w,0],[0,w.conjugate()]];X=[[0,1],[1,0]]
    K=mm(mm(mm(X,z),dag(X)),dag(z))
    assert close(K,z)
    amp=(w+w.conjugate())/2
    prob=abs(amp)**2
    assert abs(amp.real+0.5)<1e-9 and abs(prob-0.25)<1e-9
    out={'schema':'w33.s3_commutator_ramsey_witness.v1','status':'PASS_EXACT_INTERFEROMETRIC_SIGNATURE',
      'sequence':'K=X_L z X_L^-1 z^-1',
      'exact_result':'K=z',
      'input':'|+>=(|r=1>+|r=2>)/sqrt(2)',
      'return_amplitude':'-1/2',
      'return_probability':0.25,
      'commuting_null_hypothesis_return_probability':1.0,
      'contrast':0.75,
      'interpretation':'A rail experiment implementing the closed pulse loop distinguishes the S3 semidirect action from a commuting C3xC2 model without tomography.',
      'boundary':'Assumes the previously specified coherent sector-to-rail interface exists.',
      'checks':{'commutator_equals_z':True,'ramsey_probability_quarter':True}}
    if write:OUT.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2));return out
if __name__=='__main__':main(True)
