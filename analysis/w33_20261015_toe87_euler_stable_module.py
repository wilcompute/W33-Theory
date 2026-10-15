"""TOE87: prove stable binary H1/H2 relation using the Euler representation ring.

C0, C1 and C2 as F2[H27]-modules are independent of which TWO
regular square orbits are included. Maschke semisimplicity then lifts a
Grothendieck-group virtual identity to a stable direct-sum isomorphism.
"""
from __future__ import annotations
import json
from collections import Counter
from analysis.w33_20261015_toe85_h2_relation_module import ROOT
from analysis.w33_20261015_toe86_geometry_integral_routing import H,IDX
from analysis.w33_20261015_toe87_modular_bockstein_triples import (
    geometry_data,geometry_for_orbits,binary_simple_decomposition
)

def permutation_matrices(actions,n):
    matrices={}
    for g,perm in actions.items():
        assert sorted(perm)==list(range(n))
        matrices[g]=[[int(j==perm[i]) for j in range(n)] for i in range(n)]
    return matrices

def certificate():
    G=geometry_data()
    tri,edges,ei,perms,orbits,*_=G
    rows,cycles,action,squares=geometry_for_orbits((0,10),G)
    V={g:perms[IDX[g]] for g in H}
    E={g:action(g)[0] for g in H}
    T={g:action(g)[2][0][:45] for g in H}
    S={g:[j-45 for j in action(g)[2][0][45:]] for g in H}
    for g in H:
        assert len(set(T[g]))==45 and sorted(S[g])==list(range(54))
    def orbit_lengths(permutations,n):
        unseen=set(range(n));sizes=[]
        while unseen:
            i=min(unseen);orb={permutations[g][i] for g in H}
            unseen-=orb;sizes.append(len(orb))
        return sorted(sizes)
    vertex_orbits=orbit_lengths(V,27)
    edge_orbits=orbit_lengths(E,135)
    tri_orbits=orbit_lengths(T,45)
    sq_orbits=orbit_lengths(S,54)
    assert vertex_orbits==[27]
    assert edge_orbits==[27]*5
    assert tri_orbits==[9]*5
    assert sq_orbits==[27]*2
    reg=binary_simple_decomposition(permutation_matrices(V,27))
    triangle=binary_simple_decomposition(permutation_matrices(T,45))
    assert reg=={"trivial_multiplicity":1,
                 "four_2D_simple_multiplicities":[1]*4,
                 "faithful_6D_simple_multiplicity":3}
    assert triangle=={"trivial_multiplicity":5,
                       "four_2D_simple_multiplicities":[2]*4,
                       "faithful_6D_simple_multiplicity":4}
    # Euler character [H1]-[H2] = [H0]-[C0]+[C1]-[C2]
    # = [1] + 2[regular] - [five 9-cell triangle orbits].
    def v(x):
        return [x["trivial_multiplicity"]]+x["four_2D_simple_multiplicities"]+[x["faithful_6D_simple_multiplicity"]]
    R=v(reg);T=v(triangle)
    virtual=[int(i==0)+2*R[i]-T[i] for i in range(6)]
    assert virtual==[-2,0,0,0,0,2]
    data=json.loads((ROOT/"data/w33_20261015_toe87_modular_bockstein_triples.json").read_text())
    pair_classes=data["modular_pair_classification"]["classes"]
    for entry in pair_classes:
        h1=v(entry["H1"]["F2_semisimple"])
        h2=v(entry["H2"]["F2_semisimple"])
        assert [a-b for a,b in zip(h1,h2)]==virtual
    return {
        "field":"F2",
        "representation_ring_Euler_identity":"[H1]-[H2]=[H0]-[C0]+[C1]-[C2]=[1]+2[Reg(H27)]-[Triangles_45]",
        "vertex_H27_orbit_sizes":vertex_orbits,
        "edge_H27_orbit_sizes":edge_orbits,
        "triangle_H27_orbit_sizes":tri_orbits,
        "added_square_H27_orbit_sizes":sq_orbits,
        "regular_27_simple_multiplicities":reg,
        "triangle_45_simple_multiplicities":triangle,
        "virtual_H1_minus_H2_simple_multiplicities":virtual,
        "stabilized_binary_module_isomorphism":"H1(F2) + 2 trivial modules ~= H2(F2) + 2 faithful 6D simple modules",
        "equivalence_classes_checked":len(pair_classes),
        "pairs_covered":sum(x["equivalence_class_size"] for x in pair_classes),
        "scope":"H27-invariant complexes with 45 native triangles plus ANY two free H27 orbits of square faces, with the 27-vertex and 135-edge native chain action; arbitrary extra square orbits change the Euler term.",
        "limitation":"This stable binary isomorphism does not imply a unique H1/H2 F3 rank-minimizer or a physical clock."
    }

if __name__=="__main__":
    x=certificate()
    p=ROOT/"data/w33_20261015_toe87_euler_stable_module.json"
    p.write_text(json.dumps(x,indent=2,sort_keys=True)+"\n",encoding="utf8")
    print("EULER",x["virtual_H1_minus_H2_simple_multiplicities"],x["stabilized_binary_module_isomorphism"],flush=True)
