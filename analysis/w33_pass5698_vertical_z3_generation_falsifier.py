#!/usr/bin/env python3
"""Pass5698 bonkers: the obvious fiber-qutrit = three-generations reading fails the module test.

The 27 E6 bundle vertices are nine affine base sites times a three-state vertical
fiber, so over C

    C^27 = C^9 tensor C[Z3].

Under ASL(2,3), C^9=1+V8 with V8 irreducible. If the vertical Z3 action is ignored,
this looks like three copies of 1+V8 and the ASL commutant is M3(C) plus M3(C),
complex dimension 18. That is the tempting generation-three multiplicity.

But the vertical shift is part of the actual bundle gauge structure. Fourier
transforming the fiber gives three distinct Z3 characters chi^0,chi^1,chi^2, so

 C^27 = direct_sum_{k=0}^2 [(1 tensor chi^k) + (V8 tensor chi^k)].

These six ASL x Z3 irreducibles are pairwise inequivalent and occur once. The joint
commutant is therefore C^6, not M3: no symmetry-preserving operator mixes the three
fiber phases as identical generations. A genuine generation triplet needs a separate
three-dimensional multiplicity space commuting with the gauge action.
"""
from __future__ import annotations
import itertools,json
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5698_VERTICAL_Z3_GENERATION_FALSIFIER.json'
PTS=[(x,y) for x in range(3) for y in range(3)];IDX={p:i for i,p in enumerate(PTS)}

def det(A):a,b,c,d=A;return (a*d-b*c)%3
def compose(p,q):return tuple(p[q[i]] for i in range(9))

def main():
    SL=[A for A in itertools.product(range(3),repeat=4) if det(A)==1]
    assert len(SL)==24
    G=[]
    for a,b,c,d in SL:
      for tx,ty in PTS:
        G.append(tuple(IDX[((a*x+b*y+tx)%3,(c*x+d*y+ty)%3)] for x,y in PTS))
    assert len(set(G))==216
    chi8=[]
    for g in G:chi8.append(sum(i==g[i] for i in range(9))-1)
    inner=sum(x*x for x in chi8)/216;assert inner==1 # V8 irreducible

    w=np.exp(2j*np.pi/3);C3=np.array([[0,0,1],[1,0,0],[0,1,0]],complex)
    ev=np.linalg.eigvals(C3);ev=sorted(ev,key=lambda z:np.angle(z))
    # On C^27=base tensor fiber each fiber eigenvalue occurs nine times.
    T=np.kron(np.eye(9),C3);tev=np.linalg.eigvals(T)
    mult=[]
    for z in [1,w,w**2]:mult.append(int(np.sum(abs(tev-z)<1e-7)))
    assert mult==[9,9,9]

    out={
      'pass':5698,'status':'VERTICAL_Z3_FOURIER_SECTORS_ARE_THREE_GAUGE_CHARGES_NOT_THREE_IDENTICAL_GENERATIONS',
      'bundle_module':'C^27 = C^9 tensor C[Z3]',
      'base_ASL_module':'C^9 = 1 + V8 with V8 irreducible','V8_character_self_inner_product':inner,
      'vertical_shift_spectrum':'1^9 + omega^9 + omega_bar^9',
      'ASL_only_decomposition':'3 copies of 1 plus 3 copies of V8; commutant M3(C) direct-sum M3(C), complex dimension 18',
      'joint_ASL_times_Z3_decomposition':['1 x chi0','V8 x chi0','1 x chi1','V8 x chi1','1 x chi2','V8 x chi2'],
      'joint_multiplicities':[1,1,1,1,1,1],
      'joint_commutant':'C^6, complex dimension 6',
      'falsifier':'Once the actual vertical Z3 gauge action is respected, the three fiber Fourier sectors carry inequivalent charges and cannot be mixed by a gauge-commuting M3 generation algebra.',
      'open_generation_candidate':'The separate E8 grading factor 27 tensor 3 is not identified here with the vertical fiber qutrit. A genuine generation interpretation requires an explicit three-dimensional multiplicity/intertwiner commuting with the physical gauge algebra.',
      'physics_boundary':'The recurring number three in the fiber is structural Z3 charge data. This pass rules out the simplest fiber-phase=three-generation identification; it does not rule out every possible three-generation mechanism elsewhere in the repo.'
    }
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True))
if __name__=='__main__':main()
