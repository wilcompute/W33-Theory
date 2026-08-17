#!/usr/bin/env python3
"""Pass5696 bonkers: full AGL(2,3) returns if the affine eight is an orientation pseudovector.

Pass5686 showed that the plain nine-site augmentation module V8 admits the determinant
su(3) bracket only under ASL(2,3); determinant-reversing affine maps flip the bracket.
That does not force a physical orientation domain wall. Let chi(g)=+1 for det(g)=1
and -1 for det(g)=2 and twist the site action by the determinant character:

    R_tilde(g)=chi(g) R(g).

Because the bracket is orientation odd while its two inputs contribute chi^2=1,

    [R_tilde(g)f,R_tilde(g)h] = R_tilde(g)[f,h]

for all 432 elements of AGL(2,3). Thus the same exact compact su(3) Lie algebra
carries the full affine symmetry when V8 is treated as an orientation-twisted
pseudovector module. The two bracket signs are then two trivializations of the
orientation line, not automatically distinct physical phases.
"""
from __future__ import annotations
import itertools,json
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5696_AGL_ORIENTATION_TWISTED_SU3.json'
PTS=[(x,y) for x in range(3) for y in range(3)];IDX={p:i for i,p in enumerate(PTS)}

def det(A):a,b,c,d=A;return (a*d-b*c)%3
def sgn3(a):a%=3;return 0 if a==0 else (1 if a==1 else -1)
def perm_parity(p):
    inv=sum(p[i]>p[j] for i in range(len(p)) for j in range(i+1,len(p)))
    return -1 if inv%2 else 1

def main():
    GL=[A for A in itertools.product(range(3),repeat=4) if det(A)]
    assert len(GL)==48
    AGL=[]
    for A in GL:
      a,b,c,d=A;chi=1 if det(A)==1 else -1
      for tx,ty in PTS:
        p=tuple(IDX[((a*x+b*y+tx)%3,(c*x+d*y+ty)%3)] for x,y in PTS)
        AGL.append((p,chi))
    assert len(AGL)==432

    phi=np.zeros((9,9,9),dtype=int)
    for i,x in enumerate(PTS):
      for j,y in enumerate(PTS):
       for k,z in enumerate(PTS):
        u=((y[0]-x[0])%3,(y[1]-x[1])%3);v=((z[0]-x[0])%3,(z[1]-x[1])%3)
        phi[i,j,k]=sgn3(u[0]*v[1]-u[1]*v[0])
    def br(f,g):return np.einsum('ijk,i,j->k',phi,f,g)
    def Rmat(p):
      R=np.zeros((9,9),dtype=int)
      for i,j in enumerate(p):R[j,i]=1
      return R
    basis=[]
    for i in range(8):
      v=np.zeros(9,dtype=int);v[i]=1;v[8]=-1;basis.append(v)

    parity_by_chi={1:set(),-1:set()};max_plain=0;max_twist=0
    for p,chi in AGL:
      R=Rmat(p);parity_by_chi[chi].add(perm_parity(p))
      # Orientation tensor itself transforms with chi.
      assert np.array_equal(phi[np.ix_(p,p,p)],chi*phi)
      for f,h in itertools.product(basis,repeat=2):
        plain=br(R@f,R@h)-R@br(f,h)
        twist=br((chi*R)@f,(chi*R)@h)-(chi*R)@br(f,h)
        max_plain=max(max_plain,int(np.max(abs(plain))))
        max_twist=max(max_twist,int(np.max(abs(twist))))
        assert np.max(abs(twist))==0
    assert max_plain>0 and max_twist==0
    assert parity_by_chi[1]=={1} and parity_by_chi[-1]=={-1}

    out={
      'pass':5696,'status':'DETERMINANT_LINE_TWIST_RESTORES_FULL_AGL23_AS_SU3_AUTOMORPHISMS',
      'groups':{'AGL(2,3)':432,'ASL(2,3)':216},
      'orientation_character':'chi(g)=+1 for det(g)=1 and -1 for det(g)=2',
      'twisted_action':'R_tilde(g)=chi(g) R_site(g) on V8',
      'exact_equivariance':'[R_tilde(g)f,R_tilde(g)h]=R_tilde(g)[f,h] for all 432 affine transformations and all augmentation basis pairs',
      'plain_action_failure':'The untwisted site action fails on the determinant-reversing coset exactly as Pass5686 found.',
      'permutation_parity':{'ASL_coset':'all even permutations of the nine sites','determinant_reversing_coset':'all odd permutations'},
      'interpretation':'The affine su3 eight can transform as an orientation pseudovector. Choosing a global orientation is one trivialization of the determinant line, not a theorem that AGL must be dynamically broken to ASL.',
      'domain_wall_verdict':'A bracket-sign domain wall is not topologically forced by the finite algebra alone: the sign can be absorbed into the determinant-character twist. Extra dynamics would be required to turn orientation choices into distinct physical phases or localized modes.',
      'physics_boundary':'This refines Pass5686 at the representation level. It does not identify the twisted eight with QCD gluons or prove a physical parity/CP mechanism.'
    }
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True))
if __name__=='__main__':main()
