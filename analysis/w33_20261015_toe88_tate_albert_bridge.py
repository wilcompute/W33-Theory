"""TOE88: cyclic Tate/Jordan fingerprints and finite Albert-26 obstructions.

The canonical 26D *augmentation* module of the regular H27 action is
an algebraic candidate for a 27-minus-1 construction. This does NOT
by itself embed H27 into automorphisms of the Albert algebra / F4.
"""
from __future__ import annotations
import collections, json, random
from analysis.w33_20261015_toe85_h2_relation_module import ROOT, rank_and_basis, apply
from analysis.w33_20261015_toe86_geometry_integral_routing import H, IDX, mul
from analysis.w33_20261015_toe87_modular_bockstein_triples import (
    geometry_data, geometry_for_orbits, matrix_actions,
    matrix_rank_minus_identity, radical_filtration
)
G0=(0,0,0)
DIRECTIONS=((1,0,0),(0,1,0),(1,1,0),(1,2,0),(0,0,1))

def rank(rows,p):
    return len(rank_and_basis(rows,p))

def augmentation_action(p):
    nonidentity=[g for g in H if g!=G0]
    ix={g:i for i,g in enumerate(nonidentity)}
    action={}
    for h in H:
        mat=[]
        for g in nonidentity:
            v=[0]*26
            hg=mul(h,g)
            if hg!=G0:v[ix[hg]]+=1
            if h!=G0:v[ix[h]]-=1
            mat.append([q%p for q in v])
        action[h]=mat
    return action

def cyclic_jordan(mats,g,p=3):
    A=mats[g];n=len(A)
    J=[[(v-int(i==j))%p for j,v in enumerate(row)] for i,row in enumerate(A)]
    J2=[[sum(J[i][k]*J[k][j] for k in range(n))%p for j in range(n)]
         for i in range(n)]
    r1=rank(J,p);r2=rank(J2,p)
    assert r1>=r2 and 2*r1>=r2 and n-2*r1+r2>=0
    b3=r2;b2=r1-2*r2;b1=n-2*r1+r2
    # J rank=b2+2 b3, J^2 rank=b3
    assert b2>=0 and b1>=0
    tate=n-r1-r2
    assert tate==b1+b2
    return {"rank_g_minus_identity":r1,"rank_square":r2,
            "Jordan_1_2_3_block_counts":[b1,b2,b3],
            "cyclic_Tate_H0_Hminus1_dimension":tate}

def binary_aug_intertwiner(H1):
    rng=random.Random(8801)
    n=26
    e=H1[G0]
    for trial in range(1,257):
        v=[rng.randrange(2) for _ in range(n)]
        orbit={g:apply(H1[g],v,2) for g in H}
        # basis δ_g+δ_identity of augmentation, g!=identity
        matrix=[[(a+b)%2 for a,b in zip(orbit[g],v)] for g in H if g!=G0]
        if rank(matrix,2)==26:
            assert all(
                apply(H1[h],matrix[IDX[g]-(IDX[g]>IDX[G0])],2)==
                [(a+b)%2 for a,b in zip(orbit[mul(h,g)],orbit[h])]
                for h in H for g in H if g!=G0
            )
            return {"generator_search_trial":trial,
                    "cyclic_vector":v,
                    "explicit_aug_to_H1_basis_images":matrix,
                    "rank":26}
    raise AssertionError("no cyclic vector found")

def certificate():
    geom=geometry_data()
    rows,cycles,action,_=geometry_for_orbits((0,10),geom)
    h12,h13={},{};
    h1_2,h2_2,r2=matrix_actions(rows,cycles,action,2)
    h1_3,h2_3,r3=matrix_actions(rows,cycles,action,3)
    aug2=augmentation_action(2)
    aug3=augmentation_action(3)
    witness=binary_aug_intertwiner(h1_2)
    R3=radical_filtration(aug3,3)
    H3=radical_filtration(h1_3,3)
    ccenter_h1=cyclic_jordan(h1_3,(0,0,1))
    ccenter_aug=cyclic_jordan(aug3,(0,0,1))
    assert ccenter_h1!=ccenter_aug
    assert rank(aug2[(0,0,0)],2)==26
    original={}
    candidates={}
    for g in DIRECTIONS:
        original[str(g)]={"H1":cyclic_jordan(h1_3,g),
                          "H2":cyclic_jordan(h2_3,g)}
        candidates[str(g)]=cyclic_jordan(aug3,g)
    classes=json.loads((ROOT/"data/w33_20261015_toe87_modular_bockstein_triples.json").read_text())["modular_pair_classification"]["classes"]
    allclasses=[]
    for c in classes:
        pair=c["orbit_pair"]
        rows,cycles,action,_=geometry_for_orbits(pair,geom)
        m1,m2,r=matrix_actions(rows,cycles,action,3)
        local=[{"g":list(g),"H1":cyclic_jordan(m1,g),
                "H2":cyclic_jordan(m2,g)} for g in DIRECTIONS]
        allclasses.append({"pair":pair,"size":c["equivalence_class_size"],
                           "torsion":c["integral_torsion"],
                           "cyclic_Jordan_Tate":local})
        print("TATE",pair,
              [(x["H1"]["Jordan_1_2_3_block_counts"],
                x["H2"]["Jordan_1_2_3_block_counts"]) for x in local[:4]],flush=True)
    return {
        "binary_aug_equivariant_isomorphism_to_selected_H1":witness,
        "augmentation_module_dimension":26,
        "F3_aug_radical_filtration":R3,
        "F3_selected_H1_radical_filtration":H3,
        "F3_aug_center_Jordan":ccenter_aug,
        "F3_selected_H1_center_Jordan":ccenter_h1,
        "F3_equivariant_isomorphism_to_regular_augmentation":"OBSTRUCTED_BY_CENTRAL_JORDAN_RANK",
        "ternary_H1_H2_Jordan_Tate_all_13_classes":allclasses,
        "interpretation":"The 26D binary H1 is explicitly an H27-module isomorphic to the regular augmentation. In characteristic 3 the same candidate fails the central Jordan invariant; 26D dimension matching does not establish an F4/Albert embedding.",
        "F4_E6_scope":"Albert J27=traceless J26 plus scalar identity under F4, in suitable characteristic; no F4-equivariant map, integral Albert product, or physical E6 identification is constructed."}

if __name__=="__main__":
    d=certificate()
    p=ROOT/"data/w33_20261015_toe88_tate_albert_bridge.json"
    p.write_text(json.dumps(d,indent=2,sort_keys=True)+"\n",encoding="utf8")
    print("F4",d["binary_aug_equivariant_isomorphism_to_selected_H1"]["rank"],
          d["F3_aug_center_Jordan"],d["F3_selected_H1_center_Jordan"],flush=True)
