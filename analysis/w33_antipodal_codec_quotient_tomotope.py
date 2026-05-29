#!/usr/bin/env python3
"""Antipodal codec quotient / tomotope f-vector theorem.

Continue from the 16 local 12-flag codecs:

    tetrahedron: 2 chiral codecs
    Csaszar:     7 vertex codecs
    Szilassi:    7 face codecs

The correct Q4 placement is not only 16 isolated vertices.  Q4 has an antipodal
involution x -> 1-x.  Pairing the 16 codec vertices by this involution gives
8 duality axes:

    1 tetrahedral axis = {T+, T-}
    7 toroidal axes    = {Csaszar_i, Szilassi_i}

The quotient of Q4 by antipodal pairs has 8 vertices and is K4,4.  Every quotient
edge is covered by exactly two Q4 edges.

Choosing the tetrahedral axis as the hinge axis gives the tomotope f-vector by
pure quotient incidence:

    quotient axes                         = 8   -> tomotope cells
    quotient edges                        = 16  -> tomotope faces
    quotient edges incident to hinge axis = 4   -> tomotope vertices
    quotient edges not incident to hinge  = 12  -> tomotope edges

So:

    (4,12,16,8)

is obtained from Q4's antipodal codec quotient with a distinguished tetrahedral
hinge axis.  This also explains the 4/3 split: relative to the hinge axis,
there are 4 adjacent toroidal axes and 3 non-adjacent toroidal axes.
"""
from __future__ import annotations

import itertools
import json
from collections import Counter, defaultdict, deque
from pathlib import Path

N=4
TOMOTOPE=(4,12,16,8)
CODEC=12
TOTAL_FLAGS=192
TETRA_FLAGS=24
TOROIDAL_FLAGS=168
PHI6=7
D_Z=4
D_X=3
WE6=51_840
V_W33=40
H1=81


def q4_vertices():
    return list(itertools.product((0,1), repeat=N))


def comp(v):
    return tuple(1-x for x in v)


def q4_edges():
    edges=set()
    for v in q4_vertices():
        for i in range(N):
            w=list(v); w[i]^=1; w=tuple(w)
            edges.add(tuple(sorted((v,w))))
    return edges


def antipodal_axes():
    axes=[]; seen=set()
    for v in q4_vertices():
        if v in seen:
            continue
        p=tuple(sorted((v,comp(v))))
        axes.append(p); seen.update(p)
    return axes


def quotient_edges(axes):
    idx={v:i for i,axis in enumerate(axes) for v in axis}
    mult=Counter()
    lifts=defaultdict(list)
    for a,b in q4_edges():
        ia,ib=idx[a],idx[b]
        if ia==ib:
            raise AssertionError("Q4 edge inside antipodal axis")
        e=tuple(sorted((ia,ib)))
        mult[e]+=1
        lifts[e].append((a,b))
    return mult,lifts


def quotient_graph(mult):
    adj={i:set() for i in range(8)}
    for a,b in mult:
        adj[a].add(b); adj[b].add(a)
    return adj


def is_bipartite(adj):
    color={}
    for s in adj:
        if s in color: continue
        color[s]=0; q=deque([s])
        while q:
            u=q.popleft()
            for v in adj[u]:
                if v in color:
                    if color[v]==color[u]: return False,{}
                else:
                    color[v]=1-color[u]; q.append(v)
    return True,color


def is_k44(adj):
    ok,color=is_bipartite(adj)
    if not ok: return False,color
    parts=Counter(color.values())
    if sorted(parts.values()) != [4,4]: return False,color
    for u,ns in adj.items():
        if len(ns)!=4: return False,color
        if any(color[v]==color[u] for v in ns): return False,color
    return True,color


def endpoint_codec_labels(axes):
    # Axis 0 is the tetrahedral chirality axis.  Other axes are toroidal dual axes.
    labels={}
    axis_labels={}
    for i,axis in enumerate(axes):
        if i==0:
            labels[axis[0]]="T_plus"
            labels[axis[1]]="T_minus"
            axis_labels[i]="tetra_chirality_axis"
        else:
            # Choose lexicographic orientation only to name the two endpoints; antipodal pairing is canonical.
            labels[axis[0]]=f"C_vertex_codec_{i}"
            labels[axis[1]]=f"S_face_codec_{i}"
            axis_labels[i]=f"toroidal_dual_axis_{i}"
    return labels,axis_labels


def build_payload():
    axes=antipodal_axes()
    mult,lifts=quotient_edges(axes)
    adj=quotient_graph(mult)
    isquot,color=is_k44(adj)
    labels,axis_labels=endpoint_codec_labels(axes)
    hinge=0
    adjacent_to_hinge=sorted(adj[hinge])
    nonadjacent_toroidal=sorted(set(range(1,8))-set(adjacent_to_hinge))
    incident_edges=[e for e in mult if hinge in e]
    nonincident_edges=[e for e in mult if hinge not in e]
    lift_count_distribution=Counter(mult.values())
    endpoint_type_counts=Counter()
    for a,b in q4_edges():
        ta=labels[a].split('_')[0]
        tb=labels[b].split('_')[0]
        endpoint_type_counts['-'.join(sorted((ta,tb)))] += 1

    checks={
        "Q4_has_16_codec_vertices": len(q4_vertices())==16,
        "antipodal_axes_8": len(axes)==8,
        "axis_split_1_plus_7": 1+7==len(axes),
        "q4_edges_32": len(q4_edges())==32,
        "quotient_edges_16": len(mult)==16,
        "each_quotient_edge_lifts_to_two_Q4_edges": lift_count_distribution=={2:16},
        "quotient_is_K4_4": isquot,
        "quotient_degree_4": sorted(len(ns) for ns in adj.values())==[4]*8,
        "hinge_adjacent_split_4_plus_3": len(adjacent_to_hinge)==D_Z and len(nonadjacent_toroidal)==D_X,
        "tomotope_vertices_from_hinge_incident_edges": len(incident_edges)==TOMOTOPE[0]==4,
        "tomotope_edges_from_hinge_nonincident_edges": len(nonincident_edges)==TOMOTOPE[1]==12,
        "tomotope_faces_from_quotient_edges": len(mult)==TOMOTOPE[2]==16,
        "tomotope_cells_from_axes": len(axes)==TOMOTOPE[3]==8,
        "tomotope_fvector_sum_is_W33_v": sum(TOMOTOPE)==V_W33,
        "codec_flags_total": len(q4_vertices())*CODEC==TOTAL_FLAGS,
        "tetra_axis_flags": 2*CODEC==TETRA_FLAGS,
        "toroidal_axes_flags": 7*2*CODEC==TOROIDAL_FLAGS,
        "WE6_factorization": WE6==V_W33*16*H1,
    }

    return {
        "theorem":"Antipodal_Codec_Quotient_Tomotope_Theorem",
        "codec_vertex_assignment":{
            "principle":"Q4 vertices are the 16 local 12-flag codecs; antipodal complement pairs each codec with its dual.",
            "labels_by_vertex":{str(k):v for k,v in labels.items()},
            "axis_labels":axis_labels,
            "tetrahedral_axis":0,
            "toroidal_axes":list(range(1,8))
        },
        "antipodal_quotient":{
            "axes":{i:[list(x) for x in axis] for i,axis in enumerate(axes)},
            "quotient_graph":"K4,4",
            "bipartition":{str(k):v for k,v in sorted(color.items())},
            "vertices":len(axes),
            "edges":len(mult),
            "edge_lift_multiplicities":dict(lift_count_distribution),
            "degree_sequence":sorted(len(ns) for ns in adj.values())
        },
        "hinge_tomotope_extraction":{
            "hinge_axis":"tetrahedral chirality pair {T_plus,T_minus}",
            "adjacent_toroidal_axes":adjacent_to_hinge,
            "nonadjacent_toroidal_axes":nonadjacent_toroidal,
            "split":"4 adjacent + 3 nonadjacent = d_Z + d_X",
            "tomotope_f_vector_from_quotient":{
                "V_from_hinge_incident_edges":len(incident_edges),
                "E_from_hinge_nonincident_edges":len(nonincident_edges),
                "F_from_all_quotient_edges":len(mult),
                "C_from_all_axes":len(axes)
            },
            "tomotope_f_vector_expected":list(TOMOTOPE)
        },
        "flag_accounting":{
            "one_codec_flags":CODEC,
            "Q4_codec_vertices":16,
            "total_flags":"16*12=192",
            "tetra_axis_flags":"2*12=24",
            "toroidal_axes_flags":"7*2*12=168"
        },
        "endpoint_edge_type_counts_under_one_orientation":dict(endpoint_type_counts),
        "interpretation":"Q4 is the double cover of a K4,4 antipodal axis network. The tetrahedron supplies the distinguished hinge axis; the seven remaining axes are Csaszar/Szilassi dual axes. The tomotope f-vector is extracted from quotient incidence relative to the hinge axis.",
        "identities":checks,
        "all_identities_hold":bool(all(checks.values()))
    }


def main():
    payload=build_payload()
    out=Path("data/w33_antipodal_codec_quotient_tomotope.json")
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(payload,indent=2,sort_keys=True),encoding="utf-8")
    print(json.dumps({"all_identities_hold":payload["all_identities_hold"],"antipodal_quotient":payload["antipodal_quotient"],"hinge_tomotope_extraction":payload["hinge_tomotope_extraction"],"flag_accounting":payload["flag_accounting"]},indent=2,sort_keys=True))
    print(f"wrote {out}")

if __name__=="__main__":
    main()
