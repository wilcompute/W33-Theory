#!/usr/bin/env python3
"""Pass5725: exact center-character pairing on the affine (Z/3)^2 torsion doublet."""
from __future__ import annotations
import itertools,json
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'data/PART_W33_PASS5720_5724_AFFINE_TORSION_HOMOLOGY.json'
OUT=ROOT/'data/PART_W33_PASS5725_TORSION_CENTER_PAIRING.json'

def det3(M):return (int(M[0,0])*int(M[1,1])-int(M[0,1])*int(M[1,0]))%3
def inv2(M):
 d=det3(M);return (pow(d,-1,3)*np.array([[M[1,1],-M[0,1]],[-M[1,0],M[0,0]]],int))%3
def gl23():
 out=[]
 for a,b,c,d in itertools.product(range(3),repeat=4):
  M=np.array([[a,b],[c,d]],int)
  if det3(M):out.append(M)
 assert len(out)==48;return out
def qact(M):
 P=np.array([[0,1],[1,1]],int)
 return (inv2(P)@((det3(M)*M.T)%3)@P)%3

def main():
 src=json.loads(SRC.read_text())
 assert src['pass5720_integral_homology']['H1_full_Z']=='(Z/3)^2'
 Qs=[qact(M) for M in gl23()]
 assert len({tuple(Q.ravel()) for Q in Qs})==48
 V=[np.array(v,int) for v in itertools.product(range(3),repeat=2)]
 nz=[v for v in V if np.any(v)]
 fixed=[ell for ell in V if all(np.array_equal((ell@Q)%3,ell%3) for Q in Qs)]
 assert len(fixed)==1 and not np.any(fixed[0])
 orbit={tuple((np.array([1,0])@Q)%3) for Q in Qs};assert len(orbit)==8
 detect={}
 for h in nz:
  vals=[int(ell@h)%3 for ell in nz]
  detect[str(tuple(map(int,h)))]=sum(x!=0 for x in vals)
 assert set(detect.values())=={6}
 # evaluation pairing is equivariant if charges transform contragrediently
 for Q in Qs:
  Qi=inv2(Q)
  for h in V:
   for ell in V:
    assert int(((ell@Qi)%3)@((Q@h)%3))%3==int(ell@h)%3
 out={
  'pass':5725,
  'status':'TORSION_DOUBLET_IS_CENTER_OBSERVABLE_ONLY_THROUGH_CHARGE_PAIRING__NO_GL23_INVARIANT_SCALAR_CHARACTER',
  'torsion_group':'H=(Z/3)^2','residual_action':'GL(2,3), order 48',
  'nonzero_torsion_classes':8,'nonzero_covector_orbit_size':8,
  'GL23_invariant_covectors':[[0,0]],
  'detecting_nonzero_covectors_per_nonzero_torsion_class':6,
  'wilson_pairing':'W_{t,ell}(h)=omega^(t ell(h)), t=1 or 2; every nonzero h is detected by some nonzero ell',
  'canonical_equivariant_object':'evaluation H^* x H -> F3, with H^* transformed contragrediently',
  'obstruction':'No nonzero GL(2,3)-fixed ell exists. A single scalar H->Z3 center phase is not affine-equivariantly canonical; choosing one reduces/breaks the residual symmetry.',
  'relation_to_pass5709':'This supplies the exact missing abstract triality/character layer but not a physical matter representation or QCD-color identification.',
  'source_affine_action':src['pass5723_affine_symmetry'],
  'physics_boundary':'Finite center-character observability only; no confinement, quark, or gauge-coupling claim.'}
 OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True))
if __name__=='__main__':main()
