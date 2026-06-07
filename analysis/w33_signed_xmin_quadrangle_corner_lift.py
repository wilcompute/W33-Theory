#!/usr/bin/env python3
"""BT511: Signed-Xmin Quadrangle-Corner Lift Theorem.

Existing repo theorem w33_octahedron_corner_hypergraph_spectrum.py proves:
  * 240 local octahedron corner states;
  * 1620 ordinary quadrangles;
  * every corner state is incident with 27=q^3 quadrangle corners;
  * total corner incidences = 240*27 = 1620*4 = 6480.

BT509-BT510 identify the 8 signed faces of each local octahedron with signed
X_min states and the face-adjacency cube.  In an octahedron, every vertex is
incident with exactly 4 triangular faces.  Therefore every quadrangle corner
lifts canonically to four signed face incidences.

This theorem verifies the lifted uniformity:
  * 320 signed local faces receive exactly 81 lifted quadrangle-corner hits;
  * 160 antipodal/projective face pairs receive exactly 162 hits;
  * total lifted incidences = 6480*4 = 320*81 = 160*162 = 25920.

Thus the Levi homology multiplicity 81 appears as the exact signed-Xmin
quadrangle-corner lift degree.
"""
from __future__ import annotations

import json
from collections import Counter, defaultdict
from itertools import combinations, product
from pathlib import Path

import numpy as np

P = 3
Vec = tuple[int, int, int, int]


def canonical(v) -> Vec:
    vv = tuple(int(x) % P for x in v)
    if vv == (0, 0, 0, 0):
        raise ValueError("zero vector")
    for x in vv:
        if x:
            inv = 1 if x == 1 else 2
            return tuple((inv * y) % P for y in vv)  # type: ignore[return-value]
    raise AssertionError


def omega(u: Vec, v: Vec) -> int:
    return (u[0]*v[2] - u[2]*v[0] + u[1]*v[3] - u[3]*v[1]) % P


def build_geometry():
    points=[]; seen=set()
    for raw in product(range(P), repeat=4):
        if raw == (0,0,0,0):
            continue
        c=canonical(raw)
        if c not in seen:
            seen.add(c); points.append(c)
    pidx={p:i for i,p in enumerate(points)}
    edges=[(i,j) for i,j in combinations(range(len(points)),2) if omega(points[i],points[j])==0]
    adj=[[False]*len(points) for _ in points]
    for i,j in edges:
        adj[i][j]=adj[j][i]=True
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
    point_lines=defaultdict(list); edge_to_line={}
    for li,L in enumerate(lines):
        for p in L:
            point_lines[p].append(li)
        for e in combinations(L,2):
            edge_to_line[tuple(sorted(e))]=li
    return points, edges, adj, lines, point_lines, edge_to_line


def ordinary_quadrangles(adj):
    quads=[]; seen=set()
    for a,b in combinations(range(len(adj)),2):
        if adj[a][b]:
            continue
        common=[x for x in range(len(adj)) if adj[a][x] and adj[b][x]]
        for c,d in combinations(common,2):
            cyc=tuple(sorted(tuple(sorted(e)) for e in ((a,c),(c,b),(b,d),(d,a))))
            if cyc not in seen:
                seen.add(cyc); quads.append(cyc)
    return quads


def local_signed_faces(p:int, Ls:list[int]):
    """Return signed faces and incidence of local octahedron vertices to faces.

    Local octahedron vertices are 2-subsets of the four lines through p.
    Faces are star(L) and opposite(L) for each line L.
    """
    Ls=sorted(Ls)
    faces=[]
    vertex_to_faces=defaultdict(list)
    pair_of_face={}
    for L in Ls:
        others=[x for x in Ls if x!=L]
        star=tuple(sorted(tuple(sorted((L,M))) for M in others))
        opp=tuple(sorted(tuple(sorted(pair)) for pair in combinations(others,2)))
        f_star=(p,L,+1)
        f_opp=(p,L,-1)
        faces.extend([f_star,f_opp])
        pair_of_face[f_star]=(p,L)
        pair_of_face[f_opp]=(p,L)
        for v in star:
            vertex_to_faces[(p,v)].append(f_star)
        for v in opp:
            vertex_to_faces[(p,v)].append(f_opp)
    return faces, vertex_to_faces, pair_of_face


def main() -> dict:
    points, edges, adj, lines, point_lines, edge_to_line = build_geometry()
    quads=ordinary_quadrangles(adj)
    assert len(points)==40 and len(lines)==40 and len(edges)==240 and len(quads)==1620

    signed_faces=[]
    projective_pairs=set()
    local_vertex_to_faces={}
    signed_to_pair={}
    for p in range(len(points)):
        faces, v2f, f2pair = local_signed_faces(p, point_lines[p])
        signed_faces.extend(faces)
        projective_pairs.update(f2pair.values())
        local_vertex_to_faces.update(v2f)
        signed_to_pair.update(f2pair)
    signed_faces=sorted(signed_faces)
    projective_pairs=sorted(projective_pairs)
    sf_idx={f:i for i,f in enumerate(signed_faces)}
    pair_idx={pair:i for i,pair in enumerate(projective_pairs)}
    assert len(signed_faces)==320
    assert len(projective_pairs)==160

    signed_hit=Counter()
    pair_hit=Counter()
    corner_hit=Counter()
    # Also build signed-face by quadrangle incidence matrix with multiplicities.
    M=np.zeros((len(signed_faces), len(quads)), dtype=np.int16)
    for qi,cyc in enumerate(quads):
        inc=defaultdict(list)
        for u,v in cyc:
            inc[u].append((u,v)); inc[v].append((u,v))
        assert len(inc)==4
        for p,es in inc.items():
            lpair=tuple(sorted(edge_to_line[tuple(sorted(e))] for e in es))
            vertex=(p,lpair)
            corner_hit[vertex]+=1
            faces=local_vertex_to_faces[vertex]
            assert len(faces)==4
            for f in faces:
                signed_hit[f]+=1
                pair_hit[signed_to_pair[f]]+=1
                M[sf_idx[f], qi]+=1

    checks={
        "corner_uniform_27": Counter(corner_hit.values())==Counter({27:240}),
        "signed_faces_320": len(signed_faces)==320,
        "projective_pairs_160": len(projective_pairs)==160,
        "signed_lift_uniform_81": Counter(signed_hit.values())==Counter({81:320}),
        "projective_pair_uniform_162": Counter(pair_hit.values())==Counter({162:160}),
        "total_lifted_incidence": sum(signed_hit.values())==25920==6480*4==320*81==160*162,
        "matrix_shape": M.shape==(320,1620),
        "row_sum_81": Counter(int(x) for x in M.sum(axis=1))==Counter({81:320}),
        "col_sum_16": Counter(int(x) for x in M.sum(axis=0))==Counter({16:1620}),
        "entries_are_0_or_1_or_2": set(int(x) for x in M.flatten()) <= {0,1,2},
    }

    # Some quadrangles can hit two corners lifting to the same signed face, hence entries may be 2.
    entry_dist=Counter(int(x) for x in M.flatten())
    rank=int(np.linalg.matrix_rank(M.astype(float)))
    gram=np.linalg.eigvalsh((M@M.T).astype(float))
    eig_counter=Counter(int(round(x)) for x in gram)

    results={
        "theorem":"BT511 Signed-Xmin Quadrangle-Corner Lift Theorem",
        "summary":{
            "local_octahedron_corner_states":240,
            "ordinary_quadrangles":len(quads),
            "signed_Xmin_faces":len(signed_faces),
            "projective_Xmin_pairs":len(projective_pairs),
            "lift_matrix_shape":[int(x) for x in M.shape],
            "rank":rank,
            "all_checks_passed":all(checks.values()),
        },
        "checks":checks,
        "degree_identities":{
            "corner_layer":"240*27 = 1620*4 = 6480",
            "signed_face_lift":"320*81 = 6480*4 = 25920",
            "projective_pair_lift":"160*162 = 25920",
            "column_weight":"each quadrangle has 4 corners, each corner touches 4 signed faces, so column weight 16",
        },
        "lift_distributions":{
            "corner_hits":dict(Counter(corner_hit.values())),
            "signed_face_hits":dict(Counter(signed_hit.values())),
            "projective_pair_hits":dict(Counter(pair_hit.values())),
            "matrix_entry_distribution":dict(sorted(entry_dist.items())),
        },
        "signed_face_gram_spectrum_rounded":dict(sorted(eig_counter.items())),
        "interpretation":{
            "BT509":"signed local octahedron faces are signed Xmin states",
            "BT511":"quadrangle corners lift uniformly to signed Xmin faces with degree 81",
            "homology_bridge":"the recurring Levi H1 multiplicity 81 is the signed-face lift degree of the local octahedral corner hypergraph",
        },
        "substrate_reading":{
            "27":"q^3 quadrangle corners per local octahedron vertex",
            "4":"four signed faces incident to each octahedron vertex",
            "81":"3*27 signed-face lift degree; Levi homology multiplicity",
            "162":"projective face-pair lift degree = 2*81",
            "25920":"total signed quadrangle-corner lift incidences",
        },
    }
    out=Path("data/PART_BT511_SIGNED_XMIN_QUADRANGLE_CORNER_LIFT_results.json")
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(results,indent=2),encoding="utf-8")
    print(json.dumps(results,indent=2))
    return results

if __name__=="__main__":
    main()
