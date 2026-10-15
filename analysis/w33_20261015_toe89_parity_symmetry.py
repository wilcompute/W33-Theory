"""TOE89: transport the two Z/2 Bockstein membrane classes under H27.

The two nontrivial parity membranes span a 2D binary simple module.
Its kernel within H27 identifies an order-nine Pauli subgroup and gives
an intrinsic equivariant *non-SNF* torsion-direction label.
"""
from __future__ import annotations
import json
from analysis.w33_20261015_toe85_h2_relation_module import ROOT,rank_and_basis
from analysis.w33_20261015_toe86_geometry_integral_routing import H
from analysis.w33_20261015_toe87_modular_bockstein_triples import geometry_data,geometry_for_orbits

def rank(rows):
    return len(rank_and_basis(rows,2))

def certificate():
    G=geometry_data()
    parity=json.loads((ROOT/"data/w33_20261015_toe88_parity_membranes.json").read_text())
    results=[]
    for c in parity["representatives"]:
        pair=tuple(c["orbit_pair"])
        rows,cycles,action,sq=geometry_for_orbits(pair,G)
        images=[w["bockstein_edge_vector"] for w in c["integer_membrane_witnesses"]]
        if len(images)==0:
            results.append({"pair":list(pair),"torsion_module_dimension":0,
                            "H27_action":"zero", "kernel_order":27})
            continue
        assert len(images)==2
        r=rank(rows)
        assert rank(rows+images)==r+2
        def coords(vec):
            for a in range(2):
                for b in range(2):
                    residual=[(v+a*x+b*y)%2 for v,x,y in zip(vec,*images)]
                    if rank(rows+[residual])==r:
                        return [a,b]
            raise AssertionError("image outside Bockstein subspace")
        acts={}
        for g in H:
            q,sign,_=action(g)
            M=[]
            for v in images:
                moved=[0]*135
                for i,t in enumerate(v):
                    if t:moved[q[i]]=t
                M.append(coords(moved))
            acts[g]=M
        assert acts[(0,0,0)]==[[1,0],[0,1]]
        def prod(A,B):
            return [[sum(B[i][j]*A[j][k] for j in range(2))%2 for k in range(2)]
                    for i in range(2)]
        from analysis.w33_20261015_toe86_geometry_integral_routing import mul
        for g in H:
            for h in H:
                assert prod(acts[g],acts[h])==acts[mul(g,h)]
        kernel=[list(g) for g,M in acts.items() if M==[[1,0],[0,1]]]
        assert len(kernel)==9
        assert all((0,0,c) in [tuple(x) for x in kernel] for c in range(3))
        labels=[(1,0),(0,1),(1,1),(1,2)]
        fixed=[i for i,(a,b) in enumerate(labels)
               if all((a*t%3,b*t%3,z) in [tuple(x) for x in kernel]
                      for t in range(3) for z in range(3))]
        assert len(fixed)==1
        results.append({"pair":list(pair),"torsion_module_dimension":2,
                        "kernel_order":len(kernel),"kernel_H27_addresses":kernel,
                        "kernel_projective_Pauli_direction_index":fixed[0],
                        "quotient_image_is_C3":True,
                        "binary_nontrivial_simple_dim":2,
                        "generator_action_matrices":[{"g":list(g),"M":acts[g]}
                            for g in ((1,0,0),(0,1,0),(0,0,1))]})
        print("TORSION-TRANSPORT",pair,"kernel",kernel,
              "projective_direction",fixed,flush=True)
    return {"source":"Integer 24-face membrane Bockstein images on native cubic-surface oriented chains; 729 H27 representation equations checked.",
            "representatives":results,
            "conclusion":"The 2-torsion Bockstein image carries a faithful two-dimensional F2[H27/A] irreducible C3 module; its order-nine kernel A gives a canonical Pauli-direction label for the two Z/6 torsion families.",
            "limit":"Does not exhibit a canonical minimal geometric 24-face support or extend the order-1296 normalizer to full W(E6)."}
if __name__=="__main__":
    x=certificate()
    p=ROOT/"data/w33_20261015_toe89_parity_symmetry.json"
    p.write_text(json.dumps(x,indent=2,sort_keys=True)+"\n",encoding="utf8")
