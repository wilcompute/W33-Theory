#!/usr/bin/env python3
"""Pass5694: exact Jacobi expansion for the collision-deformed bracket and an l3 no-go.

Write the full Lie bracket as b and the deleted vertical-cubic contribution as D,
so the firewall bracket is b'=b-D. Since the Jacobiator has two bracket slots,

 J(b-D) = J(b) - B(b,D) - B(D,b) + J(D).

For the undeformed E8 bracket J(b)=0, hence the entire firewall anomaly is exactly

  -sum_cyc b(D(x,y),z)
  -sum_cyc D(b(x,y),z)
  +sum_cyc D(D(x,y),z).

The collision projector C/3 fixes which nine cubic supports enter D, but not all
coefficients/signs/relative normalizations of b and D. Affine orientation fixes the
sign of the separate V8 su(3) determinant bracket, not the full E8 bracket. Thus
collision support + affine orientation do not uniquely reconstruct the Jacobiator.

Even after J is known, an L-infinity equation d l3 = -J determines l3 only modulo
ker(d): l3 and l3+z give the same Jacobi repair whenever dz=0. The repo's restricted
CE-H3 tooling is therefore the right uniqueness/obstruction gate; no committed
certificate proving zero kernel and existence for the full problem is assumed here.
"""
from __future__ import annotations
import json
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5694_COLLISION_JACOBI_L3_NO_GO.json'

def apply(T,x,y):return np.einsum('kij,i,j->k',T,x,y)
def jac(T,x,y,z):
    return apply(T,apply(T,x,y),z)+apply(T,apply(T,y,z),x)+apply(T,apply(T,z,x),y)
def mixed(T,U,x,y,z):
    # outer T / inner U in each cyclic slot
    return apply(T,apply(U,x,y),z)+apply(T,apply(U,y,z),x)+apply(T,apply(U,z,x),y)

def main():
    # Verify the bilinear identity on deterministic arbitrary alternating brackets.
    rng=np.random.default_rng(5694);n=5
    def alt_tensor():
      A=rng.integers(-3,4,size=(n,n,n)).astype(float)
      return A-A.swapaxes(1,2)
    b=alt_tensor();D=alt_tensor()
    maxres=0.0
    for _ in range(32):
      x,y,z=[rng.normal(size=n) for _ in range(3)]
      lhs=jac(b-D,x,y,z)
      rhs=jac(b,x,y,z)-mixed(b,D,x,y,z)-mixed(D,b,x,y,z)+jac(D,x,y,z)
      maxres=max(maxres,float(np.max(abs(lhs-rhs))))
    assert maxres<1e-10

    # Support data from the established 36+9 collision selector.
    C=np.array([0]*36+[3]*9,dtype=int);mask=C//3
    assert list(mask).count(0)==36 and list(mask).count(1)==9

    # Linear-algebra demonstration of the generic l3 ambiguity: d l3 = -J.
    # A rank-deficient d has an affine solution set translated by ker d.
    d=np.array([[1.,0.,1.],[0.,1.,1.]])
    ker=np.array([1.,1.,-1.]);assert np.max(abs(d@ker))<1e-12
    J=np.array([2.,-1.]);l0=np.linalg.lstsq(d,-J,rcond=None)[0]
    assert np.max(abs(d@l0+J))<1e-12
    assert np.max(abs(d@(l0+7*ker)+J))<1e-12

    out={
      'pass':5694,'status':'JACOBIATOR_FULLY_EXPANDS_FROM_B_MINUS_D__COLLISION_PLUS_ORIENTATION_DO_NOT_UNIQUELY_FIX_L3',
      'exact_expansion':'J(b-D)=J(b)-B(b,D)-B(D,b)+J(D); for Lie b, J(b-D)=-B(b,D)-B(D,b)+J(D)',
      'numerical_symbolic_identity_max_residual':maxres,
      'collision_support':{'horizontal_kept':36,'vertical_deleted':9,'deletion_mask':'C/3'},
      'information_no_go':[
        'C/3 determines deleted support but not the full signed/normalized E8 bracket coefficients.',
        'Affine orientation determines the sign of the V8 determinant su3 bracket, not the complete E8 bracket b.',
        'Therefore collision support plus affine orientation do not by themselves determine J(b-D).'
      ],
      'l3_no_go':'Even for known J, solutions of d l3=-J form l3_0+ker(d) when they exist. Uniqueness requires a vanishing relevant closed-3-cochain freedom plus existence; neither follows from the collision projector.',
      'repo_gate':'tools/compute_restricted_ce_h3.py and the exhaustive homotopy tools are the appropriate coefficient-level obstruction/nonuniqueness tests before any unique l3 theorem is promoted.',
      'physics_boundary':'This closes an algebraic information question. It neither proves that the full firewall l3 exists uniquely nor assigns the homotopy bracket a microscopic physical interaction.'
    }
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True))
if __name__=='__main__':main()
