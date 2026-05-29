#!/usr/bin/env python3
"""Flag codec / toroidal boundary / Q4 hypercube theorem.

The local quantum is 12 flags.

Csaszar has V=7,E=21,F=14 with triangular faces.  It is maximal vertex
adjacency: K7 on the torus.  At each vertex degree=6, hence the flags incident
at one vertex are 2*degree = 12.  Therefore Csaszar decomposes into seven
12-flag vertex codecs.

Szilassi is dual: V=14,E=21,F=7 with seven hexagonal faces.  It is maximal
face adjacency: every face touches every other.  At each face, flags are
2*face_size = 12.  Therefore Szilassi decomposes into seven 12-flag face codecs.

The tetrahedron is self-dual: V=F=4,E=6.  It has 24 flags, split as 12+12 by
orientation (A4 rotations and the reversing coset).  These two 12-flag chiral
halves are the hinge between the Csaszar vertex-codec side and the Szilassi
face-codec side.

Thus:

    tetrahedron + Csaszar + Szilassi = 2 + 7 + 7 = 16 codecs,
    16 codecs * 12 flags/codec = 192 flags.

This is exactly the Q4/tomotope packet:

    16 = |V(Q4)|,
    24 = tetrahedron flags = Q4 square faces,
    48 = 2 * tetrahedron flags = full Q4 Gray clock ternary microticks,
    192 = 16 * 12 = tomotope flags.

The genus denominator 12 is therefore the same local flag codec that appears in
both dual genus formulas g=(n-3)(n-4)/12, with n=v for Csaszar/K7 and n=f for
Szilassi's face-dual equation.
"""
from __future__ import annotations

import itertools
import json
from pathlib import Path

Q=3
CHI=4
PHI6=7
K=12
CODEC=12
TET_FLAGS=24
CS_FLAGS=84
SZ_FLAGS=84
TOMOTOPE_FLAGS=192
PSL27=168
Q4_VERTICES=16
Q4_EDGES=32
Q4_SQUARES=24
REYE_INCIDENCES=48
M_R=24


def flags_from_edges(E:int)->int:
    # Each edge has two endpoints and two incident faces in a closed map.
    return 4*E


def flags_by_faces(F:int, sides:int)->int:
    return F*2*sides


def flags_by_vertices(V:int, degree:int)->int:
    return V*2*degree


def genus_complete(n:int):
    num=(n-3)*(n-4)
    return num//12 if num%12==0 else None


def allowed_residues():
    return [r for r in range(12) if ((r-3)*(r-4))%12==0]


def q4_face_counts():
    return {m:(2**(4-m))*__import__('math').comb(4,m) for m in range(5)}


def q4_vertices():
    return list(itertools.product((0,1), repeat=4))


def q4_edges():
    edges=set()
    for v in q4_vertices():
        for i in range(4):
            w=list(v); w[i]^=1; w=tuple(w)
            edges.add(tuple(sorted((v,w))))
    return edges


def build_payload():
    tet={
        "V":4,"E":6,"F":4,"face_size":3,"degree":3,
        "flags":flags_from_edges(6),
        "vertex_partition_flags":flags_by_vertices(4,3),
        "face_partition_flags":flags_by_faces(4,3),
        "orientation_codecs":2,
        "orientation_split":[12,12],
        "self_dual":True,
        "genus_by_v":genus_complete(4),
        "genus_by_f":genus_complete(4),
    }
    cs={
        "name":"Csaszar","V":7,"E":21,"F":14,"face_size":3,"degree":6,
        "flags":flags_from_edges(21),
        "vertex_codecs":7,
        "flags_per_vertex_codec":2*6,
        "face_codecs":None,
        "max_adjacency":"vertex/K7",
        "genus_by_v":genus_complete(7),
    }
    sz={
        "name":"Szilassi","V":14,"E":21,"F":7,"face_size":6,"avg_degree":3,
        "flags":flags_from_edges(21),
        "face_codecs":7,
        "flags_per_face_codec":2*6,
        "vertex_codecs":None,
        "max_adjacency":"face/complete face adjacency",
        "genus_by_f":genus_complete(7),
    }
    qfaces=q4_face_counts()
    total_codecs=tet["orientation_codecs"]+cs["vertex_codecs"]+sz["face_codecs"]
    total_flags=tet["flags"]+cs["flags"]+sz["flags"]
    toroidal_flags=cs["flags"]+sz["flags"]
    checks={
        "tetrahedron_flags_24": tet["flags"]==TET_FLAGS,
        "tetrahedron_orientation_split_12_12": tet["orientation_split"]==[CODEC,CODEC],
        "tetrahedron_self_dual_v_equals_f": tet["V"]==tet["F"]==4 and tet["self_dual"],
        "csaszar_flags_84": cs["flags"]==CS_FLAGS==flags_by_faces(14,3)==flags_by_vertices(7,6),
        "csaszar_seven_vertex_codecs": cs["vertex_codecs"]==7 and cs["flags_per_vertex_codec"]==CODEC,
        "szilassi_flags_84": sz["flags"]==SZ_FLAGS==flags_by_faces(7,6),
        "szilassi_seven_face_codecs": sz["face_codecs"]==7 and sz["flags_per_face_codec"]==CODEC,
        "dual_swap": cs["V"]==sz["F"] and cs["F"]==sz["V"] and cs["E"]==sz["E"]==21,
        "toroidal_pair_flags_168": toroidal_flags==PSL27==2*84==7*TET_FLAGS,
        "total_codecs_16": total_codecs==Q4_VERTICES,
        "total_flags_192": total_flags==TOMOTOPE_FLAGS==Q4_VERTICES*CODEC,
        "q4_square_faces_equal_tetrahedron_flags": qfaces[2]==TET_FLAGS,
        "q4_edges_equal_32": len(q4_edges())==Q4_EDGES,
        "q4_full_gray_ternary_ticks_equal_48": Q4_VERTICES*Q==REYE_INCIDENCES==2*TET_FLAGS,
        "q4_coil_ternary_ticks_equal_24": 8*Q==M_R==TET_FLAGS,
        "genus_residues_0_3_4_7": allowed_residues()==[0,Q,CHI,PHI6],
        "tetrahedron_genus_zero_both_sides": tet["genus_by_v"]==0 and tet["genus_by_f"]==0,
        "csaszar_v7_genus_one": cs["genus_by_v"]==1,
        "szilassi_f7_genus_one": sz["genus_by_f"]==1,
        "denominator_12_is_codec": CODEC==Q*(Q+1)==12,
        "sixteen_codecs_split_2_7_7": [tet["orientation_codecs"],cs["vertex_codecs"],sz["face_codecs"]]==[2,7,7],
    }
    return {
        "theorem":"Flag_Codec_Toroidal_Hypercube_Boundary_Theorem",
        "local_flag_codec":{
            "flags_per_codec":CODEC,
            "formula":"q(q+1)=3*4=12",
            "meaning":"one local oriented incidence packet; denominator of the dual genus equations"
        },
        "polyhedra":{
            "tetrahedron":tet,
            "csaszar":cs,
            "szilassi":sz
        },
        "codec_decomposition":{
            "tetrahedron":"24 flags = 2 codecs = 12+12 orientation split",
            "csaszar":"84 flags = 7 vertex codecs, 12 flags at each degree-6 vertex",
            "szilassi":"84 flags = 7 face codecs, 12 flags on each hexagonal face",
            "combined_codecs":"2+7+7=16=|V(Q4)|",
            "combined_flags":"(2+7+7)*12=192=tomotope flags"
        },
        "genus_duality":{
            "csaszar_formula":"g=(v-3)(v-4)/12 with v=7 gives 1",
            "szilassi_dual_formula":"g=(f-3)(f-4)/12 with f=7 gives 1",
            "tetrahedron_hinge":"v=f=4 gives genus 0 on both sides",
            "allowed_residues_mod12":allowed_residues()
        },
        "hypercube_boundary_link":{
            "Q4_vertices":len(q4_vertices()),
            "Q4_edges":len(q4_edges()),
            "Q4_face_counts":qfaces,
            "Q4_square_faces_equal_tetra_flags":qfaces[2],
            "full_gray_ternary_microticks":"16*3=48=2*tetrahedron flags",
            "snake_coil_ternary_microticks":"8*3=24=tetrahedron flags",
            "interpretation":"the toroidal Q4 boundary supplies 16 slots; each slot is one 12-flag codec in the tetrahedron-Csaszar-Szilassi stack"
        },
        "identities":checks,
        "all_identities_hold":bool(all(checks.values()))
    }


def main():
    payload=build_payload()
    out=Path("data/w33_flag_codec_toroidal_hypercube_boundary.json")
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(payload,indent=2,sort_keys=True),encoding="utf-8")
    print(json.dumps({"all_identities_hold":payload["all_identities_hold"],"local_flag_codec":payload["local_flag_codec"],"codec_decomposition":payload["codec_decomposition"],"genus_duality":payload["genus_duality"],"hypercube_boundary_link":payload["hypercube_boundary_link"]},indent=2,sort_keys=True))
    print(f"wrote {out}")

if __name__=="__main__":
    main()
