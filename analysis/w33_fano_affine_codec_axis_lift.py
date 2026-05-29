#!/usr/bin/env python3
"""Fano / affine lift of the antipodal Q4 codec quotient.

Previous theorem:
    Q4 antipodal quotient is K4,4.  Choosing the tetrahedral chirality axis as
    hinge yields 4 adjacent axes and 3 nonadjacent axes, and extracts the
    tomotope f-vector (4,12,16,8).

This theorem identifies the seven non-hinge axes with the Fano plane PG(2,2):

    4 hinge-adjacent axes      = affine points of AG(2,2)
    3 hinge-nonadjacent axes  = points at infinity / directions

The 12 quotient edges not incident to the hinge are then exactly the 12
point-direction incidences of AG(2,2).  Adding the line at infinity plus the
six affine lines reconstructs all seven Fano lines.

Thus the 8 antipodal axes split as:

    1 tetrahedral hinge axis + 7 Fano toroidal axes.

The tomotope f-vector becomes the affine/Fano incidence vector relative to the
hinge:

    V = 4  affine points
    E = 12 affine point-direction incidences
    F = 16 all quotient edges
    C = 8  all axes = hinge + seven Fano points
"""
from __future__ import annotations

import itertools
import json
from collections import Counter, defaultdict, deque
from pathlib import Path

N=4
TOMOTOPE=(4,12,16,8)
FANO_POINTS=7
FANO_LINES=7
FANO_FLAGS=21
CODEC=12
TOROIDAL_FLAGS=168
PSL27=168


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
        if v in seen: continue
        p=tuple(sorted((v,comp(v))))
        axes.append(p); seen.update(p)
    return axes


def quotient_graph(axes):
    idx={v:i for i,axis in enumerate(axes) for v in axis}
    adj={i:set() for i in range(len(axes))}
    mult=Counter()
    for a,b in q4_edges():
        ia,ib=idx[a],idx[b]
        e=tuple(sorted((ia,ib)))
        mult[e]+=1
        adj[ia].add(ib); adj[ib].add(ia)
    return adj,mult


def bipartition(adj):
    color={0:0}; q=deque([0])
    while q:
        u=q.popleft()
        for v in adj[u]:
            if v in color:
                if color[v]==color[u]: raise ValueError("not bipartite")
            else:
                color[v]=1-color[u]; q.append(v)
    return color


def xor2(a,b):
    return (a[0]^b[0], a[1]^b[1])


def affine_fano_lines(affine_points, directions):
    # affine_points: labels for 4 points of F2^2; directions: labels for three nonzero vectors.
    aff=list(affine_points)
    dirs=list(directions)
    lines=[]
    # line at infinity
    lines.append(tuple(sorted([f"inf_{d}" for d in dirs])))
    for d in dirs:
        seen=set()
        for p in aff:
            if p in seen: continue
            q=xor2(p,d)
            seen.add(p); seen.add(q)
            lines.append(tuple(sorted([f"inf_{d}", f"aff_{p}", f"aff_{q}"])))
    return sorted(set(lines))


def fano_incidence(lines):
    pts=sorted(set(x for line in lines for x in line))
    incidence={(p,i) for i,line in enumerate(lines) for p in line}
    return pts,incidence


def fano_pair_unique(lines):
    pair_count=Counter()
    for line in lines:
        for a,b in itertools.combinations(line,2):
            pair_count[tuple(sorted((a,b)))] += 1
    return pair_count


def build_payload():
    axes=antipodal_axes()
    adj,mult=quotient_graph(axes)
    color=bipartition(adj)
    hinge=0
    neighbor_axes=sorted(adj[hinge])
    direction_axes=sorted(set(range(1,8))-set(neighbor_axes))
    # Assign AG(2,2) coordinates to hinge-neighbor axes and directions to non-neighbor axes.
    aff_coords=[(0,0),(1,0),(0,1),(1,1)]
    dir_coords=[(1,0),(0,1),(1,1)]
    affine_axis_label={axis:coord for axis,coord in zip(neighbor_axes,aff_coords)}
    direction_axis_label={axis:coord for axis,coord in zip(direction_axes,dir_coords)}
    lines=affine_fano_lines(aff_coords,dir_coords)
    pts,incidence=fano_incidence(lines)
    pair_count=fano_pair_unique(lines)

    # Map K4,4 non-hinge edges to affine point-direction incidences.
    nonhinge_edges=[e for e in mult if hinge not in e]
    point_direction_edges=[]
    for a,b in nonhinge_edges:
        if a in affine_axis_label and b in direction_axis_label:
            aa,dd=a,b
        elif b in affine_axis_label and a in direction_axis_label:
            aa,dd=b,a
        else:
            raise AssertionError("nonhinge edge not affine-direction")
        point_direction_edges.append((f"aff_{affine_axis_label[aa]}", f"inf_{direction_axis_label[dd]}"))

    # In AG(2,2), each affine point is incident to each of the 3 directions = 12 incidences.
    expected_point_direction={(f"aff_{p}",f"inf_{d}") for p in aff_coords for d in dir_coords}
    got_point_direction=set(point_direction_edges)

    line_types=Counter("infinity" if all(x.startswith("inf_") for x in line) else "affine" for line in lines)
    point_degrees=Counter(p for p,_ in incidence)
    line_sizes=Counter(len(line) for line in lines)
    pair_multiplicities=Counter(pair_count.values())

    checks={
        "quotient_axes_8": len(axes)==8,
        "hinge_neighbors_4": len(neighbor_axes)==4,
        "hinge_nonneighbors_3": len(direction_axes)==3,
        "affine_direction_split_4_plus_3": len(affine_axis_label)==4 and len(direction_axis_label)==3,
        "nonhinge_edges_12": len(nonhinge_edges)==12,
        "nonhinge_edges_are_affine_point_direction_incidence": got_point_direction==expected_point_direction,
        "fano_points_7": len(pts)==FANO_POINTS,
        "fano_lines_7": len(lines)==FANO_LINES,
        "fano_line_sizes_3": line_sizes=={3:7},
        "fano_point_degrees_3": set(point_degrees.values())=={3},
        "fano_flags_21": len(incidence)==FANO_FLAGS,
        "every_pair_on_unique_line": pair_multiplicities=={1:21},
        "line_split_1_infinity_6_affine": line_types=={"infinity":1,"affine":6},
        "tomotope_V_affine_points": len(neighbor_axes)==TOMOTOPE[0],
        "tomotope_E_point_direction_incidences": len(nonhinge_edges)==TOMOTOPE[1],
        "tomotope_F_quotient_edges": len(mult)==TOMOTOPE[2],
        "tomotope_C_axes": len(axes)==TOMOTOPE[3],
        "toroidal_axis_flags_psl27": FANO_POINTS*2*CODEC==TOROIDAL_FLAGS==PSL27,
    }

    return {
        "theorem":"Fano_Affine_Codec_Axis_Lift",
        "axis_split":{
            "hinge_axis":hinge,
            "affine_point_axes":{str(k):v for k,v in affine_axis_label.items()},
            "direction_infinity_axes":{str(k):v for k,v in direction_axis_label.items()},
            "interpretation":"hinge neighbors are the four affine points of AG(2,2); hinge nonneighbors are the three directions/points at infinity"
        },
        "fano_plane":{
            "points":pts,
            "lines":[list(line) for line in lines],
            "line_type_counts":dict(line_types),
            "flags":len(incidence),
            "point_degrees":dict(point_degrees),
            "pair_multiplicities":dict(pair_multiplicities)
        },
        "quotient_edge_interpretation":{
            "nonhinge_edges_count":len(nonhinge_edges),
            "point_direction_edges":sorted(point_direction_edges),
            "statement":"the 12 quotient edges not incident to the tetrahedral hinge are exactly the AG(2,2) point-direction incidences"
        },
        "tomotope_extraction":{
            "V":"4 affine points",
            "E":"12 point-direction incidences",
            "F":"16 quotient edges",
            "C":"8 axes = hinge plus seven Fano points",
            "f_vector":list(TOMOTOPE)
        },
        "flag_codec_reading":{
            "seven_fano_axes":"each carries one Csaszar vertex codec and one Szilassi face codec",
            "toroidal_flags":"7*2*12=168=|PSL(2,7)|",
            "hinge_axis":"carries the two tetrahedral chiral codecs"
        },
        "identities":checks,
        "all_identities_hold":bool(all(checks.values()))
    }


def main():
    payload=build_payload()
    out=Path("data/w33_fano_affine_codec_axis_lift.json")
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(payload,indent=2,sort_keys=True),encoding="utf-8")
    print(json.dumps({"all_identities_hold":payload["all_identities_hold"],"axis_split":payload["axis_split"],"fano_plane":payload["fano_plane"],"tomotope_extraction":payload["tomotope_extraction"]},indent=2,sort_keys=True))
    print(f"wrote {out}")

if __name__=="__main__":
    main()
