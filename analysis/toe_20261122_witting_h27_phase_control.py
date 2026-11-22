#!/usr/bin/env python3
"""Exact normal H27 torsor in the Witting four-mode optical control group.

The order-27 subgroup is the normal closure of R5 R33^-1 in the
three-reflection order-648 Hessian permutation group. All ray actions
come from exact arithmetic in Q(omega), not floating-point matching.
"""
from __future__ import annotations
import json
from collections import Counter
from pathlib import Path
from sympy.combinatorics import Permutation,PermutationGroup
import toe_20261122_witting_one_phase_three_fixed as base

def verify():
    permutations=base.permutations()
    R={i:Permutation(permutations[i]) for i in base.FIXED}
    group=PermutationGroup(list(R.values()))
    assert group.order()==648
    heisenberg=group.normal_closure([R[5]*R[33]**-1])
    assert heisenberg.order()==27
    assert heisenberg.center().order()==3
    assert heisenberg.derived_subgroup().order()==3
    orders=Counter(int(g.order()) for g in heisenberg.generate_schreier_sims())
    assert orders=={1:1,3:26}
    orbit=sorted(heisenberg.orbit(base.TUNABLE))
    assert len(orbit)==27
    assert heisenberg.stabilizer(base.TUNABLE).order()==1
    assert orbit==sorted(base.orbit_and_paths(permutations))
    quotient_order=group.order()//heisenberg.order()
    assert quotient_order==24
    control=base.verify()
    assert control['orbit_size']==27
    return dict(status='PASS_EXACT_H27_REGULAR_WITTING_ORBIT',date='2026-11-22',
      fixed_mirror_indices=list(base.FIXED),
      normal_generator_word='R5 * inverse(R33)',
      group_order=int(group.order()),normal_subgroup_order=int(heisenberg.order()),
      normal_subgroup_center_order=int(heisenberg.center().order()),
      normal_subgroup_derived_order=int(heisenberg.derived_subgroup().order()),
      subgroup_element_order_profile={str(k):int(v) for k,v in sorted(orders.items())},
      quotient_order=int(quotient_order),
      regular_orbit_size=len(orbit),regular_orbit_indices=orbit,
      stabilizer_of_tunable_ray_in_H27=1,
      group_identification='extraspecial Heisenberg 3_+^{1+2}: nonabelian order 27, exponent 3, center=derived subgroup of order 3',
      controller='continuous phase on ray 36 plus fixed order-three mirrors on 5,26,33',
      controller_lie_dimension=16,
      caveat='H27 regular address action and single-photon U4 Lie control are exact; there is no experimentally verified spacetime, gauge, gravity, or multiphoton universality here.')

def main():
    out=verify()
    path=Path(__file__).resolve().parents[1]/'data'/'toe_20261122_witting_h27_phase_control.json'
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n',encoding='utf-8')
    print('PASS H27 normal 27, G25 648, regular 27-orbit, U4 control')

if __name__=='__main__':main()
