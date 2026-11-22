#!/usr/bin/env python3
"""Exact Hessian group quotient tower on one Witting polar pencil.

G25 order 648 -> central quotient on 9 Hesse cells (216),
H27 order 27 -> translations on 9 Hesse cells (9),
and the action on 4 polar lines -> A4 (order 12).
"""
from __future__ import annotations
import json
from pathlib import Path
from sympy.combinatorics import Permutation,PermutationGroup
import toe_20261122_witting_one_phase_three_fixed as model
import toe_20261122_witting_h27_polar_pencil as polar

def verify():
    permutations=model.permutations()
    gens={i:Permutation(permutations[i]) for i in model.FIXED}
    G=PermutationGroup(list(gens.values()))
    N=G.normal_closure([gens[5]*gens[33]**-1])
    Z=N.center()
    assert (G.order(),N.order(),Z.order())==(648,27,3)
    z=next(x for x in Z.generate_schreier_sims() if int(x.order())==3)
    geometry=polar.verify()
    exterior=set(geometry['regular_27_ray_orbit'])
    assert all(z(i)==i for i in range(40) if i not in exterior)
    cells=sorted([tuple(sorted(c)) for c in z.cyclic_form if set(c)<=exterior])
    assert len(cells)==9 and all(len(c)==3 for c in cells)
    assert sorted(v for c in cells for v in c)==sorted(exterior)
    cid={x:i for i,c in enumerate(cells) for x in c}
    def induced_on_cells(g):
        q=[cid[g(c[0])] for c in cells]
        assert sorted(q)==list(range(9))
        for i,c in enumerate(cells):
            assert {cid[g(x)] for x in c}=={q[i]}
        return Permutation(q)
    H=PermutationGroup([induced_on_cells(gens[i]) for i in model.FIXED])
    T=PermutationGroup([induced_on_cells(g) for g in N.generators])
    assert (H.order(),T.order())==(216,9)
    assert len(H.orbit(0))==9 and len(T.orbit(0))==9
    assert H.stabilizer(0).order()==24
    assert T.is_abelian
    assert all(int(g.order()) in (1,3) for g in T.generate_schreier_sims())
    assert H.normal_closure(T.generators).order()==9
    triplets=[tuple(t) for t in geometry['four_three_ray_pencil_lines']]
    tid={v:i for i,three in enumerate(triplets) for v in three}
    def induced_on_pencil(g):
        q=[tid[g(t[0])] for t in triplets]
        assert sorted(q)==list(range(4))
        for i,t in enumerate(triplets):
            assert {tid[g(v)] for v in t}=={q[i]}
        return Permutation(q)
    A4=PermutationGroup([induced_on_pencil(gens[i]) for i in model.FIXED])
    assert A4.order()==12
    assert sorted(int(g.order()) for g in A4.generate_schreier_sims())==[1]+[2]*3+[3]*8
    return dict(status='PASS_EXACT_HESSIAN_27_TO_9_AND_A4_QUOTIENTS',date='2026-11-22',
        G25_order=648,H27_order=27,central_Z3_order=3,
        normal_H27_regular_orbit=27,
        central_Z3_fixes_13_polar_neighborhood_points=True,
        central_Z3_exterior_orbit_sizes=[3]*9,
        nine_center_fibers=[list(c) for c in cells],
        induced_9_cell_group_order=216,
        induced_9_cell_point_stabilizer_order=24,
        induced_H27_translation_order=9,
        induced_H27_translation_is_regular_and_abelian=True,
        induced_pencil_4_line_group_order=12,
        induced_pencil_4_line_group_is_A4=True,
        icosahedral_rhetoric_disallowed=True,
        theorem='G25/Hessian 648 acts projectively on the 9 center-orbits of a normal H27 27-ray torsor through group of order 216, with regular F3^2 translation quotient. The action on the four isotropic lines of its fixed Witting ray is A4, order 12.',
        boundary='The 9x3 labels are a finite symmetry address/phase bundle, not 27 mutually orthogonal photon states, observed physical time bins, spacetime or Standard Model fields.')

def main():
    d=verify(); path=Path(__file__).resolve().parents[1]/'data'/'toe_20261122_witting_hessian_quotient_tower.json'
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(d,indent=2,sort_keys=True)+'\n',encoding='utf-8')
    print('PASS G25 648 -> Hesse 216 on 9 cells, A4 12 on 4 lines')
if __name__=='__main__':main()
