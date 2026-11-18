"""Native W33 27-address and Siegel two-qutrit Clifford gate certificate.

Native actions checked at q=3; no claim of new abstract theorem or E6
27D intertwiner (the central-character no-go is in the existing repository).
"""
from itertools import product
from collections import Counter
import json,sys
from pathlib import Path
from sympy.combinatorics import Permutation,PermutationGroup
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
import toe_20261118_W33_triperiodic_Levi_homogenization as W
from toe_20261118_W33_dual_parabolic_radicals_27 import unipotent_radical

def run():
    _,points,lines=W.levi()
    ix={p:i for i,p in enumerate(points)}
    li={L:i for i,L in enumerate(lines)}
    def pmap(v):
        return [ix[W.projective(tuple((x[k]+W.symplectic(x,v)*v[k])%3
                             for k in range(4)))] for x in points]
    group=PermutationGroup([Permutation(pmap(v)) for v in points])
    assert group.order()==25920
    point_anchor=ix[W.projective((1,0,0,0))]
    p_info,H=unipotent_radical(group.stabilizer(point_anchor))
    neighbors={i for i,p in enumerate(points)
               if i!=point_anchor and W.symplectic(points[point_anchor],p)==0}
    opposite=set(range(40))-neighbors-{point_anchor}
    assert (len(neighbors),len(opposite))==(12,27)
    unseen=set(range(40));orbits=[]
    while unseen:
        x=min(unseen);o={g(x) for g in H}
        orbits.append(dict(size=len(o),anchor=int(point_anchor in o),
                           near=len(o&neighbors),far=len(o&opposite)))
        unseen-=o
    assert sorted(v["size"] for v in orbits)==[1,3,3,3,3,27]
    assert {g(next(iter(opposite))) for g in H}==opposite
    # The point radical is regular on the 27-point shell. Its center
    # cycles all 27 as nine disjoint 3-cycles, with trace0 on z,z².
    center=[g for g in H if all(g*h==h*g for h in H)]
    assert len(center)==3
    zz=next(g for g in center if g.order()==3)
    cycles=[]
    pending=set(opposite)
    while pending:
        p=min(pending);cyc={p,zz(p),(zz**2)(p)}
        assert len(cyc)==3
        pending-=cyc;cycles.append(cyc)
    assert len(cycles)==9
    regular_central_multiplicity={"1":9,"omega":9,"omega2":9}
    # The repo's operator/trinification E6 27 has center omega I27,
    # therefore no invertible equivariant map from the regular 27.
    # The rank bound of a map into the center-omega operator module is9.
    assert len(cycles)==regular_central_multiplicity["omega"]

    # Choose native Lagrangian span(q1,q2) in W.symplectic pairing.
    lagrangian={ix[W.projective(v)] for v in
                ((1,0,0,0),(0,0,1,0),(1,0,1,0),(1,0,2,0))}
    assert len(lagrangian)==4
    lineidx=li[tuple(sorted(lagrangian))]
    all_shear_points={}
    all_shear_lines={}
    phase_vectors={}
    for a,b,c in product(range(3),repeat=3):
        def shear(x):
            q1,p1,q2,p2=x
            return ((q1+a*p1+b*p2)%3,p1,
                    (q2+b*p1+c*p2)%3,p2)
        pm=Permutation([ix[W.projective(shear(p))] for p in points])
        assert pm.order() in (1,3)
        assert all(W.symplectic(shear(u),shear(v))==W.symplectic(u,v)
                   for u,v in ((points[0],points[1]),(points[9],points[32])))
        lm=Permutation([li[tuple(sorted(pm(i) for i in L))] for L in lines])
        assert lm(lineidx)==lineidx
        all_shear_points[(a,b,c)]=pm
        all_shear_lines[(a,b,c)]=lm
        # Projective two-qutrit diagonal Clifford representation:
        # U_B |x> = omega^{(1/2)x^T B x}|x>, 1/2=2 in F3.
        phase_vectors[(a,b,c)]=tuple(2*(a*x*x+2*b*x*y+c*y*y)%3
                                  for x,y in product(range(3),repeat=2))
    assert len(set(all_shear_points.values()))==27
    assert len(set(all_shear_lines.values()))==27
    assert len(set(phase_vectors.values()))==27
    lp=PermutationGroup([Permutation([li[tuple(sorted(pmap(v)[i] for i in L))]
                                      for L in lines]) for v in points])
    radical_L,UL=unipotent_radical(lp.stabilizer(lineidx))
    assert set(all_shear_lines.values())==set(UL)
    # This is an EXACT identification with the native W33 Siegel radical,
    # not merely an abstract isomorphism.
    for abc in all_shear_points:
        for def_ in all_shear_points:
            sum_abc=tuple((x+y)%3 for x,y in zip(abc,def_))
            assert all_shear_points[abc]*all_shear_points[def_]==all_shear_points[sum_abc]
            assert all((x+y)%3==z for x,y,z in
                       zip(phase_vectors[abc],phase_vectors[def_],phase_vectors[sum_abc]))
    # Cross shear b=1 gives the entangling two-qutrit CZ:
    # omega^(x y). The diagonal a,c generators are local phase gates.
    cross=phase_vectors[(0,1,0)]
    assert cross==tuple((x*y)%3 for x,y in product(range(3),repeat=2))
    diag_a=phase_vectors[(1,0,0)]
    assert diag_a==tuple((2*x*x)%3 for x,y in product(range(3),repeat=2))
    diag_c=phase_vectors[(0,0,1)]
    assert diag_c==tuple((2*y*y)%3 for x,y in product(range(3),repeat=2))
    # Radical pair intersections: incident and nonincident flag positions.
    point_radicals={}
    for p in (min(lagrangian),min(set(range(40))-lagrangian)):
        _,K=unipotent_radical(group.stabilizer(p))
        point_radicals[str(p)]=dict(incidence=int(p in lagrangian),
                                  intersect_radical_size=len(set(K)&set(all_shear_points.values())))
    assert sorted(z["intersect_radical_size"] for z in point_radicals.values())==[1,9],point_radicals
    out=dict(status="PASS",native_W33_point_orbits=orbits,
             point_H27_regular_noncollinear_shell=27,
             point_H27_central_cycles=len(cycles),
             regular_center_character_multiplicities=regular_central_multiplicity,
             operator_E6_center_character_multiplicities={"1":0,"omega":27,"omega2":0},
             maximal_linear_equivariant_rank_address_to_E6_operator=9,
             no_invertible_intertwiner=True,
             canonical_lagrangian_line_index=lineidx,
             native_line_radical_matches_all_27_F3_symmetric_shears=True,
             shear_parameters="B=[[a,b],[b,c]], a,b,c in F3",
             qutrit_basis="two qutrits |x,y>, x,y in F3",
             Clifford_phase_formula="U_B|x,y>=omega^[2*(a*x^2+2*b*x*y+c*y^2)]|x,y>",
             local_quadratic_generators=2,
             two_qutrit_CZ_entangling_generators=1,
             exact_CZ_01_phase_exponents=list(cross),
             all_27_diagonal_Clifford_operators_distinct=True,
             group_law_exact_all_729_pairs=True,
             native_point_line_radical_intersection_samples=point_radicals,
             prior_art="Regular 27 W33 shell, central-character 9-rank obstruction and two-qutrit Siegel/Clifford link already appear in earlier project passes, including TOE79, Pass11043, Pass11869.",
             new_check="Explicit conjugacy-free equality of all27 native W33 line-parabolic permutations with canonical symmetric 2x2 F3 shears and corresponding two-qutrit phase-gate exponents; compared intersecting W33 radical subgroups.",
             physical_limit="This is a finite Weil/Clifford representation, not a quantum-optical experimental circuit, nor an actual E6 27-intertwiner.")
    outpath=ROOT/"data/toe_20261118_native_W33_dual27_twoqutrit_siegel_crosscheck.json"
    outpath.write_text(json.dumps(out,indent=2)+"\n",encoding="utf-8")
    print("PASS W33 regular H27 shell, Siegel C3^3=27 exact shears, entangling qutrit CZ")
    print("INTERSECTIONS",point_radicals)
    return out

if __name__=="__main__":run()
