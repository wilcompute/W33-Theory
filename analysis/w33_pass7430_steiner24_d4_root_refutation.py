#!/usr/bin/env python3
"""Pass7430: the 24 local Steiner slots are NOT the 24-root W(D4)-set.

Both carriers have size 24 and an abstract order-192 W(D4) symmetry, but the unique
normal elementary abelian 2^3 subgroup has different orbit structure:
  local slots: 3 regular orbits of size 8;
  D4 roots:    6 orbits of size 4.
This invariant rules out an equivariant identification.
"""
from __future__ import annotations
import itertools,json,math
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'PART_W33_PASS7430_STEINER24_D4_ROOT_REFUTATION.json'

def main():
    # Slot side: Pass7409 gives the regular translation group T=C2^3 on 8 leaves.
    # Pass4965 gives 3 Steiner triples above the fixed line. T fixes the triple label,
    # so its 24-point orbits are 8+8+8.
    slot_orbits=[8,8,8]
    # Root side: standard D4 roots +/-e_i +/-e_j.  The normal even-sign subgroup E=C2^3
    # preserves the support {i,j}; for each of 6 supports it is transitive on 4 signs.
    R=[]
    for i,j in itertools.combinations(range(4),2):
      for a in (1,-1):
       for b in (1,-1):
        v=[0]*4;v[i]=a;v[j]=b;R.append(tuple(v))
    R=sorted(set(R));assert len(R)==24
    E=[]
    for s in itertools.product((1,-1),repeat=4):
        if math.prod(s)==1:E.append(s)
    assert len(E)==8
    unseen=set(R);root_orbits=[]
    while unseen:
        v=next(iter(unseen));O={tuple(s[i]*v[i] for i in range(4)) for s in E};unseen-=O;root_orbits.append(len(O))
    assert sorted(root_orbits)==[4]*6
    # Stabilizer intersection gives the same obstruction locally.
    # Slot stabilizer meets T trivially because T acts regularly on each 8-leaf block.
    # A root stabilizer meets E in order 2.
    v=R[0];fixE=sum(tuple(s[i]*v[i] for i in range(4))==v for s in E);assert fixE==2
    out={'schema':'w33.pass7430.steiner24_d4_root_refutation.v1','status':'PASS',
      'local_Steiner_slots':24,'slot_factorization':'8 Eisenstein leaves x 3 Steiner triples over a fixed A2^4 line',
      'abstract_local_group':'2^3:S4 of order 192, certified in Pass7409',
      'normal_2^3_orbits_on_slots':slot_orbits,
      'D4_roots':24,'normal_2^3_orbits_on_D4_roots':sorted(root_orbits),
      'slot_point_stabilizer_intersection_with_normal_2^3':1,
      'root_point_stabilizer_intersection_with_normal_2^3':fixE,
      'negative_theorem':'The 24 local Steiner chart slots and the 24 D4 roots are not isomorphic W(D4)-sets. The characteristic normal 2^3 subgroup has orbit decompositions 8+8+8 versus 4+4+4+4+4+4.',
      'positive_reading':'The 24-slot carrier is a different degree-24 permutation representation of the same abstract local 192-element symmetry and should be studied on its own terms.',
      'boundary':'This specifically rejects the equivariant identification; it does not deny that both carriers can participate in larger E8 incidence structures.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps({'status':'PASS','slots':slot_orbits,'roots':sorted(root_orbits)}))
if __name__=='__main__':main()
