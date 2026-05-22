#!/usr/bin/env python3
"""Local octahedron faces are the signed X_min vectors.

Long shot tested:
  The recent octahedron commits say every W33 point carries one local
  octahedron O_p with 8 faces.  The minimal-logical theorem says there are
  320 signed X_min vectors and 160 projective X_min flags.

Result:
  At each point p, the four lines through p form a K4 pencil.  O_p=L(K4).
  Its 8 faces split into 4 antipodal pairs.  Each antipodal pair corresponds
  to one flag (p,L), hence one projective X_min ray.  The two oriented faces
  in the pair correspond to the two nonzero F3 scalar representatives.

Counts:
  40 * 8 = 320 signed X_min vectors
  40 * 4 = 160 projective X_min flags

The edge-face incidence of the 40 local octahedra gives a 480 x 320 codec
matrix: local octahedron edges versus signed X faces.  It has rank 280=40*7
and nullity 40, one face-sum relation per local octahedron.
"""
from __future__ import annotations

import json
from collections import Counter, defaultdict
from itertools import combinations, product
from pathlib import Path

import numpy as np

P=3
Vec=tuple[int,int,int,int]


def canonical(v)->Vec:
    vv=tuple(int(x)%P for x in v)
    if vv==(0,0,0,0):
        raise ValueError("zero vector")
    for x in vv:
        if x:
            inv=1 if x==1 else 2
            return tuple((inv*y)%P for y in vv)  # type: ignore[return-value]
    raise AssertionError


def omega(u:Vec,v:Vec)->int:
    return (u[0]*v[2]-u[2]*v[0]+u[1]*v[3]-u[3]*v[1])%P


def build_w33():
    points=[]; seen=set()
    for raw in product(range(P), repeat=4):
        if raw==(0,0,0,0):
            continue
        c=canonical(raw)
        if c not in seen:
            seen.add(c); points.append(c)
    pidx={p:i for i,p in enumerate(points)}
    edges=[(i,j) for i,j in combinations(range(len(points)),2) if omega(points[i],points[j])==0]
    lines=set()
    for i,j in edges:
        u,v=points[i],points[j]
        line=set()
        for a,b in product(range(P), repeat=2):
            if a==0 and b==0:
                continue
            line.add(pidx[canonical((a*u[t]+b*v[t] for t in range(4)))])
        lines.add(tuple(sorted(line)))
    lines=sorted(lines)
    point_lines=defaultdict(list)
    for li,L in enumerate(lines):
        for p in L:
            point_lines[p].append(li)
    return points, edges, lines, point_lines


def local_octahedron_faces_for_point(p:int, Ls:list[int]):
    """Return signed faces and projective antipodal face pairs for one K4 pencil.

    K4 vertices are the four lines through p.  Vertices of O=L(K4) are pairs
    of lines.  The 8 triangular faces come in antipodal pairs indexed by one
    line L: star at L versus triangle on the three complementary lines.
    """
    Ls=sorted(Ls)
    faces=[]
    pairs=[]
    for L in Ls:
        others=[x for x in Ls if x!=L]
        star=tuple(sorted(tuple(sorted((L,M))) for M in others))
        opp=tuple(sorted(tuple(sorted(pair)) for pair in combinations(others,2)))
        faces.append((p,L,"star",star))
        faces.append((p,L,"opposite",opp))
        pairs.append((p,L,star,opp))
    return faces,pairs


def edge_face_codec_one_octahedron():
    # O=L(K4) with K4 vertices 0..3.
    oct_vertices=list(combinations(range(4),2))
    oct_edges=[(i,j) for i,j in combinations(range(6),2) if set(oct_vertices[i]) & set(oct_vertices[j])]
    faces=[]
    for L in range(4):
        incident=[i for i,e in enumerate(oct_vertices) if L in e]
        opposite=[i for i,e in enumerate(oct_vertices) if L not in e]
        faces.append(tuple(sorted(incident)))
        faces.append(tuple(sorted(opposite)))
    edge_index={tuple(sorted(e)):i for i,e in enumerate(oct_edges)}
    M=np.zeros((len(oct_edges), len(faces)), dtype=int)
    for j,tri in enumerate(faces):
        for e in combinations(tri,2):
            M[edge_index[tuple(sorted(e))], j]=1
    return M


def main()->int:
    points, w33_edges, lines, point_lines=build_w33()
    signed_faces=[]; projective_pairs=[]
    for p in range(len(points)):
        faces,pairs=local_octahedron_faces_for_point(p, point_lines[p])
        signed_faces.extend(faces)
        projective_pairs.extend(pairs)
    M1=edge_face_codec_one_octahedron()
    # block diagonal rank/degree facts for 40 identical local octahedra
    rank_one=int(np.linalg.matrix_rank(M1.astype(float)))
    row_degrees=Counter(int(x) for x in M1.sum(axis=1))
    col_degrees=Counter(int(x) for x in M1.sum(axis=0))
    edge_gram_eigs=Counter(int(round(x)) for x in np.linalg.eigvalsh((M1@M1.T).astype(float)))
    face_gram_eigs=Counter(int(round(x)) for x in np.linalg.eigvalsh((M1.T@M1).astype(float)))

    checks={
        "w33_counts": len(points)==40 and len(lines)==40 and len(w33_edges)==240,
        "each_point_has_four_lines": Counter(len(v) for v in point_lines.values())==Counter({4:40}),
        "signed_faces_count": len(signed_faces)==320,
        "projective_face_pairs_count": len(projective_pairs)==160,
        "two_faces_per_projective_flag": Counter((p,L) for p,L,_,_ in signed_faces) == Counter({(p,L):2 for p,L,_,_ in projective_pairs}),
        "codec_shape_one": M1.shape == (12,8),
        "edge_face_degrees": row_degrees==Counter({2:12}) and col_degrees==Counter({3:8}),
        "rank_one_7": rank_one==7,
        "global_rank_280": 40*rank_one==280,
        "global_nullity_40": 320-40*rank_one==40,
        "spectrum_one": edge_gram_eigs==Counter({0:5,2:3,4:3,6:1}) and face_gram_eigs==Counter({0:1,2:3,4:3,6:1}),
    }
    payload={
        "theorem_name":"Local Octahedron Faces = Signed Xmin Theorem",
        "summary":{
            "local_octahedra":40,
            "signed_octahedron_faces":len(signed_faces),
            "projective_antipodal_face_pairs":len(projective_pairs),
            "edge_face_codec_shape_per_point":[12,8],
            "edge_face_codec_global_shape":[480,320],
            "rank_per_octahedron":rank_one,
            "global_rank":40*rank_one,
            "global_nullity":320-40*rank_one,
            "all_checks_passed":all(checks.values()),
        },
        "checks":checks,
        "one_octahedron_edge_face_row_degrees":dict(row_degrees),
        "one_octahedron_edge_face_col_degrees":dict(col_degrees),
        "one_octahedron_edge_gram_spectrum":dict(edge_gram_eigs),
        "one_octahedron_face_gram_spectrum":dict(face_gram_eigs),
        "identities":{
            "signed_Xmin":"40*8=320 signed local octahedron faces = |X_min^{F3}|.",
            "projective_Xmin":"40*4=160 antipodal face-pairs = |X_min|.",
            "directed_carrier_codec":"40*12=480 local octahedron edge slots.",
            "local_face_relation":"rank(edge-face incidence of O)=7, so each local octahedron has one face-sum null relation.",
        },
    }
    root=Path(__file__).resolve().parents[1]
    out=root/"data"/"w33_octahedron_faces_are_signed_xmin.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, indent=2, sort_keys=True)+"\n", encoding="utf-8")
    print(json.dumps(payload["summary"], indent=2, sort_keys=True))
    return 0 if payload["summary"]["all_checks_passed"] else 1

if __name__=="__main__":
    raise SystemExit(main())
