#!/usr/bin/env python3
"""Tetrahedron 24-flag codec split diagnostics.

Question tested:
    Are the tetrahedron's two 12-flag codecs vertex-type, face-type, edge-type,
    or something else?

Result:
    The canonical 12+12 split is the orientation/chirality split of S4 into
    A4 and its odd coset.  Each chirality is perfectly balanced over vertices,
    faces, edges, and opposite-edge axes:

        per chirality: 4 vertices * 3 flags, 4 faces * 3 flags,
                       6 edges * 2 flags, 3 edge axes * 4 flags.

    Therefore the two tetrahedral 12-codecs are not vertex-only or face-only.
    They are self-dual chiral hinge codecs.

    The edge geometry is nevertheless more canonical than arbitrary vertex/face
    halves: tetrahedron edges split canonically into three opposite-edge axes,
    each carrying 8 flags.  This gives a transverse decomposition

        24 = 2 chiralities * 3 edge axes * 4 flags.

    So the tetrahedron is edge-mediated in the middle: chirality gives the two
    12-codecs, while the self-dual edge axes supply the ternary bridge between
    Csaszar vertex-codecs and Szilassi face-codecs.
"""
from __future__ import annotations

import itertools
import json
from collections import Counter, defaultdict
from pathlib import Path

VERTS=(0,1,2,3)
CODEC=12
Q=3
CHI=4
TET_FLAGS=24


def parity(perm):
    inv=0
    for i in range(len(perm)):
        for j in range(i+1,len(perm)):
            inv += perm[i] > perm[j]
    return inv % 2


def edge_of(flag):
    a,b,c,d=flag
    return tuple(sorted((a,b)))


def face_of(flag):
    a,b,c,d=flag
    return tuple(sorted((a,b,c)))


def vertex_of(flag):
    return flag[0]


def missing_vertex_of_face(face):
    return tuple(sorted(set(VERTS)-set(face)))[0]


def opposite_edge(edge):
    return tuple(sorted(set(VERTS)-set(edge)))


def dual_flag(flag):
    # Incidence duality reverses the flag chain: vertex <-> opposite face,
    # edge <-> opposite edge.  Reversal on four symbols has even parity.
    a,b,c,d=flag
    return (d,c,b,a)


def axis_label(edge):
    e=edge
    oe=opposite_edge(e)
    return tuple(sorted((e,oe)))


def flags():
    return list(itertools.permutations(VERTS))


def count_by(items, key):
    c=Counter(key(x) for x in items)
    return {str(k):v for k,v in sorted(c.items(), key=lambda kv: str(kv[0]))}


def build_payload():
    F=flags()
    even=[f for f in F if parity(f)==0]
    odd=[f for f in F if parity(f)==1]
    chiral={"even_A4":even,"odd_coset":odd}
    edges=sorted({edge_of(f) for f in F})
    axes=sorted({axis_label(e) for e in edges}, key=str)
    axis_flags={str(ax):[f for f in F if axis_label(edge_of(f))==ax] for ax in axes}

    chirality_stats={}
    for name,fs in chiral.items():
        chirality_stats[name]={
            "flags":len(fs),
            "vertex_counts":count_by(fs, vertex_of),
            "face_counts":count_by(fs, face_of),
            "edge_counts":count_by(fs, edge_of),
            "edge_axis_counts":count_by(fs, lambda f: axis_label(edge_of(f))),
        }

    axis_stats={}
    for ax in axes:
        fs=[f for f in F if axis_label(edge_of(f))==ax]
        axis_stats[str(ax)]={
            "flags":len(fs),
            "chirality_counts":Counter("even" if parity(f)==0 else "odd" for f in fs),
            "edges":[list(e) for e in ax],
            "dual_closed":all(axis_label(edge_of(dual_flag(f)))==ax for f in fs),
        }
        axis_stats[str(ax)]["chirality_counts"] = dict(axis_stats[str(ax)]["chirality_counts"])

    vertex_halves=[]
    for subset in itertools.combinations(VERTS,2):
        fs=[f for f in F if vertex_of(f) in subset]
        vertex_halves.append({"chosen_vertices":subset,"flags":len(fs),"chirality_counts":dict(Counter(parity(f) for f in fs))})

    face_list=sorted({face_of(f) for f in F})
    face_halves=[]
    for subset in itertools.combinations(face_list,2):
        fs=[f for f in F if face_of(f) in subset]
        face_halves.append({"chosen_faces":[list(x) for x in subset],"flags":len(fs),"chirality_counts":dict(Counter(parity(f) for f in fs))})

    edge_3_subsets=[]
    for subset in itertools.combinations(edges,3):
        fs=[f for f in F if edge_of(f) in subset]
        star_subset=tuple(sorted((opposite_edge(e) for e in subset)))
        edge_3_subsets.append({
            "edges":[list(e) for e in subset],
            "flags":len(fs),
            "dual_edges":[list(e) for e in star_subset],
            "dual_is_complement":set(star_subset)==set(edges)-set(subset),
            "chirality_counts":dict(Counter(parity(f) for f in fs)),
        })
    edge_dual_complement_splits=[x for x in edge_3_subsets if x["dual_is_complement"]]

    dual_checks={
        "dual_is_involution": all(dual_flag(dual_flag(f))==f for f in F),
        "dual_preserves_chirality": all(parity(dual_flag(f))==parity(f) for f in F),
        "dual_swaps_vertex_and_face": all(vertex_of(dual_flag(f))==missing_vertex_of_face(face_of(f)) for f in F),
        "dual_sends_edge_to_opposite_edge": all(edge_of(dual_flag(f))==opposite_edge(edge_of(f)) for f in F),
        "dual_preserves_edge_axis": all(axis_label(edge_of(dual_flag(f)))==axis_label(edge_of(f)) for f in F),
    }

    checks={
        "total_flags_24": len(F)==TET_FLAGS,
        "chirality_split_12_12": len(even)==len(odd)==CODEC,
        "each_chirality_balanced_over_vertices_3_each": all(set(Counter(vertex_of(f) for f in fs).values())=={3} for fs in chiral.values()),
        "each_chirality_balanced_over_faces_3_each": all(set(Counter(face_of(f) for f in fs).values())=={3} for fs in chiral.values()),
        "each_chirality_balanced_over_edges_2_each": all(set(Counter(edge_of(f) for f in fs).values())=={2} for fs in chiral.values()),
        "each_chirality_balanced_over_three_edge_axes_4_each": all(set(Counter(axis_label(edge_of(f)) for f in fs).values())=={4} for fs in chiral.values()),
        "three_opposite_edge_axes_8_each": len(axes)==Q and all(len(v)==8 for v in axis_flags.values()),
        "edge_axis_chirality_split_4_4": all(axis_stats[str(ax)]["chirality_counts"]=={"even":4,"odd":4} for ax in axes),
        "dual_checks_all_hold": all(dual_checks.values()),
        "vertex_12_halves_exist_but_are_noncanonical": len(vertex_halves)==6 and all(x["flags"]==12 for x in vertex_halves),
        "face_12_halves_exist_but_are_noncanonical": len(face_halves)==6 and all(x["flags"]==12 for x in face_halves),
        "edge_12_halves_exist_but_are_choice_dependent": len(edge_3_subsets)==20 and all(x["flags"]==12 for x in edge_3_subsets),
        "dual_complement_edge_splits_count_8_subsets_4_splits": len(edge_dual_complement_splits)==8,
    }

    return {
        "theorem":"Tetrahedron_Codec_Split_Diagnostics",
        "main_conclusion":"The two canonical 12-flag tetrahedral codecs are chiral orientation codecs. They are balanced over vertices, faces, edges, and the three opposite-edge axes. Edge geometry is canonical as a 3-axis x 8-flag decomposition, transverse to the 2-chirality x 12-codec split.",
        "flag_model":"A flag is a permutation (a,b,c,d): vertex=a, edge={a,b}, face={a,b,c}, missing vertex=d.",
        "chirality_codecs":chirality_stats,
        "edge_axis_decomposition":axis_stats,
        "dual_action":{
            "definition":"dual(a,b,c,d)=(d,c,b,a)",
            "checks":dual_checks,
            "interpretation":"duality preserves chirality and edge axes, while swapping vertex and face incidence"
        },
        "noncanonical_12_splits":{
            "vertex_halves_count":len(vertex_halves),
            "face_halves_count":len(face_halves),
            "edge_three_edge_halves_count":len(edge_3_subsets),
            "dual_complement_edge_splits_subsets":len(edge_dual_complement_splits),
            "interpretation":"12-flag vertex/face/edge halves exist, but require choosing a subset. The invariant 12+12 split is chirality; the invariant edge structure is 3 opposite-edge axes of 8 flags."
        },
        "architecture_reading":{
            "csaszar_side":"7 vertex codecs of 12 flags",
            "szilassi_side":"7 face codecs of 12 flags",
            "tetrahedron_side":"2 chiral self-dual codecs of 12 flags, cut transversely by 3 edge axes of 8 flags",
            "best_answer_to_user_hypothesis":"The tetrahedron is not purely vertex-type or face-type. The two 12-codecs are chiral; edge-duality supplies the canonical ternary 3-axis bridge in the middle."
        },
        "identities":checks,
        "all_identities_hold":bool(all(checks.values()))
    }


def main():
    payload=build_payload()
    out=Path("data/w33_tetrahedron_codec_split_diagnostics.json")
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(payload,indent=2,sort_keys=True),encoding="utf-8")
    print(json.dumps({"all_identities_hold":payload["all_identities_hold"],"main_conclusion":payload["main_conclusion"],"dual_action":payload["dual_action"],"noncanonical_12_splits":payload["noncanonical_12_splits"],"architecture_reading":payload["architecture_reading"]},indent=2,sort_keys=True))
    print(f"wrote {out}")

if __name__=="__main__":
    main()
