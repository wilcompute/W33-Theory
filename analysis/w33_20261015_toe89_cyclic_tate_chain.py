"""TOE89: cyclic Tate chain-cell theorem and its polarization no-go.

The 99-face H27 complex restricted to any of the four noncentral C3
Pauli directions has an IDENTICAL projective/trivial decomposition:
3 fixed triangle faces + 32 length-three free orbits. Thus the face
C3 Tate group has dimension 3 in each degree for every two-orbit pair,
irrespective of the unique H1/H2 preferred direction.

That cell-level invariant is insufficient to force the observed
homology selector, demonstrated by a three-orbit counterexample.
"""
from __future__ import annotations
import json
from analysis.w33_20261015_toe85_h2_relation_module import ROOT
from analysis.w33_20261015_toe87_modular_bockstein_triples import (
    geometry_data, geometry_for_orbits
)
from analysis.w33_20261015_toe86_geometry_integral_routing import H,mul

DIR=((1,0,0),(0,1,0),(1,1,0),(1,2,0))
def cycle_structure(pair,geom,g):
    rows,cycles,action,squares=geometry_for_orbits(pair,geom)
    dest,sign=action(g)[2]
    unseen=set(range(len(rows)))
    cycles=[]
    while unseen:
        i=min(unseen);s=i;cyc=[];sgn=1
        while s in unseen:
            unseen.remove(s);cyc.append(s);sgn*=sign[s];s=dest[s]
        assert s==i and len(cyc) in (1,3) and sgn==1
        if len(cyc)==1:
            assert cyc[0]<45
        cycles.append({"length":len(cyc),"triangle":cyc[0]<45})
    one=sum(x["length"]==1 for x in cycles)
    three=sum(x["length"]==3 for x in cycles)
    assert one==3 and (len(rows)-3)//3==three,(g,one,three)
    return {"fixed_oriented_triangle_faces":one,
            "free_C3_orbits":three,
            "signed_3cycle_product":1,
            "F3_Tate_dimension_H0_Hminus1":one}
def certificate():
    geom=geometry_data()
    frozen=json.loads((ROOT/"data/w33_20261015_toe88_tate_albert_bridge.json").read_text())
    cls=frozen["ternary_H1_H2_Jordan_Tate_all_13_classes"]
    witnesses=[]
    for c in cls:
        pair=tuple(c["pair"])
        structure=[cycle_structure(pair,geom,g) for g in DIR]
        assert len({(x["fixed_oriented_triangle_faces"],x["free_C3_orbits"]) for x in structure})==1
        vals=c["cyclic_Jordan_Tate"][:4]
        mins1=[i for i,v in enumerate(vals) if v["H1"]["rank_g_minus_identity"]==
               min(t["H1"]["rank_g_minus_identity"] for t in vals)]
        mins2=[i for i,v in enumerate(vals) if v["H2"]["rank_g_minus_identity"]==
               min(t["H2"]["rank_g_minus_identity"] for t in vals)]
        assert mins1==mins2 and len(mins1)==1
        witnesses.append({"pair":list(pair),"class_size":c["size"],
                          "selected_Pauli_direction_index":mins1[0],
                          "all_four_C3_face_decompositions":structure})
    assert sum(x["class_size"] for x in witnesses)==468
    original=cycle_structure((0,10),geom,DIR[1])
    triple=cycle_structure((0,10,1),geom,DIR[1])
    assert original["free_C3_orbits"]==32
    assert triple["free_C3_orbits"]==41
    t=json.loads((ROOT/"data/w33_20261015_toe87_modular_bockstein_triples.json").read_text())["three_orbit_stress"]["cases"]
    counter=next(c for c in t if c["orbit_triple"]==[0,10,1])
    assert counter["H1_four_direction_ranks"]==[2,2,2,2]
    return {
      "chain_level_restriction_theorem":"For any two complete regular H27 square orbits, over F3 and any noncentral order-three g, C2 restricted to <g> is three trivial 1D modules + thirty-two free 3D regular C3 modules.",
      "C1_C3_free_module_count":45,
      "C0_C3_free_module_count":9,
      "C2_C3_fixed_triangle_faces":3,
      "C2_C3_free_3D_modules":32,
      "C2_C3_Tate_dimension_in_each_degree":3,
      "all_13_two_orbit_classes":witnesses,
      "three_orbit_extension":triple,
      "counterexample_flat_H1_direction_rank":counter["H1_four_direction_ranks"],
      "counterexample_nonflat_H2_direction_rank":counter["H2_four_direction_ranks"],
      "mathematical_conclusion":"Local C3 face-cell isotropy and Tate(C2) dimension alone cannot prove a uniquely shared H1/H2 selector: one extra free square orbit retains three fixed triangle faces but destroys uniqueness of H1. The extension maps in the equivariant chain exact sequences matter.",
      "open_theorem":"Prove the 468-pair ternary coincidence conceptually from the connecting morphisms of the Tate long exact sequences. This is not accomplished here."
    }
if __name__=="__main__":
    d=certificate()
    p=ROOT/"data/w33_20261015_toe89_cyclic_tate_chain.json"
    p.write_text(json.dumps(d,indent=2,sort_keys=True)+"\n",encoding="utf8")
    print("TATE-CHAIN",len(d["all_13_two_orbit_classes"]),
          d["C2_C3_Tate_dimension_in_each_degree"],flush=True)
