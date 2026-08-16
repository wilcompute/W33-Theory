#!/usr/bin/env python3
"""Pass5684: the collision projector is exactly the support mask of the E8 firewall deformation.

Existing repo results establish:
  * 45 E6 cubic supports = 36 horizontal affine lifts + 9 vertical full Z3 fibers;
  * the firewall/L-infinity program deletes exactly those nine vertical fibers from l2;
  * deleting them creates the Jacobi anomaly repaired by l3.

Pass5676 defines C(T)=sum_b binom(n_b(T),2), with C=0 on all 36 horizontal
supports and C=3 on all 9 vertical supports. Therefore

    delta_fw(T) = C(T)/3

is not merely correlated with the firewall: on the 45 support basis it IS the exact
0/1 deletion mask. Hence the firewall bracket can be written supportwise as

    l2_fw = l2_other + (I-C/3) l2_cubic.

Important boundary: the Jacobiator is quadratic in l2. Consequently the resulting
L-infinity l3 tensor is not in general 'equal to C'. C/3 selects the deleted cubic
support; the Jacobi anomaly contains compositions/cross-terms of the deleted and
retained bracket pieces.
"""
from __future__ import annotations
import itertools,json
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5684_COLLISION_LINFINITY_SUPPORT_WELD.json'
Q=3

def ag23_lines():
    pts=[(x,y) for x in range(3) for y in range(3)];idx={p:i for i,p in enumerate(pts)}
    dirs=[(1,m) for m in range(3)]+[(0,1)];L=set()
    for p in pts:
        for dx,dy in dirs:
            L.add(tuple(sorted(idx[((p[0]+t*dx)%3,(p[1]+t*dy)%3)] for t in range(3))))
    return pts,sorted(L)

def collision(n):
    n=np.asarray(n,dtype=int);return int((n@n-3)//2)

def main():
    pts,lines=ag23_lines();assert (len(pts),len(lines))==(9,12)
    supports=[]
    for L in lines:
        n=np.zeros(9,dtype=int);n[list(L)]=1
        for k in range(3):supports.append(('horizontal',L,k,n.copy()))
    for b in range(9):
        n=np.zeros(9,dtype=int);n[b]=3
        supports.append(('vertical',(b,),0,n))
    assert len(supports)==45
    c=[collision(x[3]) for x in supports]
    delta=[x/3 for x in c]
    assert c.count(0)==36 and c.count(3)==9
    assert set(delta)=={0.0,1.0}
    PH=np.diag([1-d for d in delta]);PV=np.diag(delta)
    assert np.allclose(PH@PH,PH) and np.allclose(PV@PV,PV)
    assert int(round(np.trace(PH)))==36 and int(round(np.trace(PV)))==9

    # Algebraic expansion of a Jacobiator under l' = l-D.  Record coefficient
    # pattern only: J is bilinear in its two l2 occurrences, so support deletion
    # necessarily generates retained/deleted cross terms as well as D-D terms.
    expansion=['J(l)','-B(l,D)','-B(D,l)','+J(D)']
    out={
      'pass':5684,'status':'COLLISION_PROJECTOR_IS_EXACT_FIREWALL_SUPPORT_MASK_NOT_THE_FULL_JACOBIATOR',
      'cubic_supports':{'total':45,'horizontal':36,'vertical':9},
      'collision':'C(T)=sum_b binom(n_b,2)',
      'exact_mask_identity':'delta_fw(T)=C(T)/3: 0 on horizontal36, 1 on vertical9',
      'projectors':{'keep_horizontal':'P_H=I-C/3, rank36','delete_vertical':'P_V=C/3, rank9'},
      'firewall_bracket_identity':'l2_fw = l2_other + P_H l2_cubic',
      'repo_weld':['analysis/w33_pass5620_e6_horizontal_vertical_selector.py','analysis/w33_pass5676_e6_fiber_collision_projector.py','tools/compute_firewall_jacobiator_tensor.py','tools/verify_e8_firewall_filtered_bracket_jacobi.py'],
      'jacobiator_expansion_under_l_minus_D':expansion,
      'Linfinity_conclusion':'The same-fiber collision observable gives the exact support shadow of the L-infinity firewall deformation. The l3/Jacobi tensor carries compositional cross-terms and is not a scalar multiple of C.',
      'physics_boundary':'This weld explains why the hard-core projector and the old Jacobi firewall select the same 36/9 supports. It does not derive the coefficient of a collision penalty or prove a microscopic dynamical origin for l3.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True))
if __name__=='__main__':main()
