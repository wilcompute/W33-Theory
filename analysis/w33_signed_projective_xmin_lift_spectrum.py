#!/usr/bin/env python3
"""BT512: Signed/Projective Xmin Lift Spectrum Theorem.

BT511 lifted ordinary W33 quadrangle corners from local octahedron vertices
onto the 320 signed X_min faces of the Richter/W33 octahedra.

This theorem computes the exact spectral split of that lift.

Let M be the 320 x 1620 signed-face/quadrangle lift matrix:
  M[f,Q]=1 iff quadrangle Q, through one of its four corners, touches signed
  octahedron face f.

Then:
  row degree = 81,
  column weight = 16,
  rank(M)=160,
  Spec(MM^T)=1296^1 + 464^24 + 144^30 + 112^24 + 80^81 + 0^160.

Now quotient signed faces into their 160 antipodal/projective X_min pairs and
let P be the 160 x 1620 pair/quadrangle matrix.  Then:
  row degree = 162,
  column weight = 16,
  rank(P)=40,
  Spec(PP^T)=2592^1 + 792^24 + 288^15 + 0^120.

Thus the projective quotient sees the W33 SRG multiplicities 1,24,15, while
the signed lift adds the protected 81-sector.
"""
from __future__ import annotations

import json
from collections import Counter, defaultdict
from itertools import combinations, product
from pathlib import Path

import numpy as np

P_FIELD = 3
Vec = tuple[int, int, int, int]


def canonical(v) -> Vec:
    vv = tuple(int(x) % P_FIELD for x in v)
    if vv == (0, 0, 0, 0):
        raise ValueError("zero vector")
    for x in vv:
        if x:
            inv = 1 if x == 1 else 2
            return tuple((inv * y) % P_FIELD for y in vv)  # type: ignore[return-value]
    raise AssertionError


def omega(u: Vec, v: Vec) -> int:
    return (u[0]*v[2] - u[2]*v[0] + u[1]*v[3] - u[3]*v[1]) % P_FIELD


def build_geometry():
    points=[]; seen=set()
    for raw in product(range(P_FIELD), repeat=4):
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
        for a,b in product(range(P_FIELD), repeat=2):
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
    Ls=sorted(Ls)
    faces=[]; v2f=defaultdict(list); f2pair={}
    for L in Ls:
        others=[x for x in Ls if x!=L]
        star=tuple(sorted(tuple(sorted((L,M))) for M in others))
        opp=tuple(sorted(tuple(sorted(pair)) for pair in combinations(others,2)))
        f_star=(p,L,+1)
        f_opp=(p,L,-1)
        faces.extend([f_star,f_opp])
        f2pair[f_star]=(p,L); f2pair[f_opp]=(p,L)
        for v in star:
            v2f[(p,v)].append(f_star)
        for v in opp:
            v2f[(p,v)].append(f_opp)
    return faces, v2f, f2pair


def main() -> dict:
    points, edges, adj, lines, point_lines, edge_to_line = build_geometry()
    quads=ordinary_quadrangles(adj)
    assert len(points)==40 and len(lines)==40 and len(edges)==240 and len(quads)==1620

    signed_faces=[]; local_vertex_to_faces={}; signed_to_pair={}
    for p in range(len(points)):
        faces, v2f, f2pair = local_signed_faces(p, point_lines[p])
        signed_faces.extend(faces)
        local_vertex_to_faces.update(v2f)
        signed_to_pair.update(f2pair)
    signed_faces=sorted(signed_faces)
    projective_pairs=sorted(set(signed_to_pair.values()))
    sf_idx={f:i for i,f in enumerate(signed_faces)}
    pp_idx={pair:i for i,pair in enumerate(projective_pairs)}
    assert len(signed_faces)==320
    assert len(projective_pairs)==160

    M=np.zeros((len(signed_faces), len(quads)), dtype=np.int16)
    for qi,cyc in enumerate(quads):
        inc=defaultdict(list)
        for u,v in cyc:
            inc[u].append((u,v)); inc[v].append((u,v))
        for p,es in inc.items():
            lpair=tuple(sorted(edge_to_line[tuple(sorted(e))] for e in es))
            for f in local_vertex_to_faces[(p,lpair)]:
                M[sf_idx[f], qi] += 1

    # Projective quotient sums the two signed rows in each antipodal pair.
    Q=np.zeros((len(projective_pairs), len(quads)), dtype=np.int16)
    for f in signed_faces:
        Q[pp_idx[signed_to_pair[f]]] += M[sf_idx[f]]

    signed_rank=int(np.linalg.matrix_rank(M.astype(float)))
    projective_rank=int(np.linalg.matrix_rank(Q.astype(float)))
    signed_eigs=Counter(int(round(x)) for x in np.linalg.eigvalsh((M@M.T).astype(float)))
    projective_eigs=Counter(int(round(x)) for x in np.linalg.eigvalsh((Q@Q.T).astype(float)))

    checks={
        "signed_shape": M.shape==(320,1620),
        "projective_shape": Q.shape==(160,1620),
        "signed_row_degree_81": Counter(int(x) for x in M.sum(axis=1))==Counter({81:320}),
        "signed_column_weight_16": Counter(int(x) for x in M.sum(axis=0))==Counter({16:1620}),
        "projective_row_degree_162": Counter(int(x) for x in Q.sum(axis=1))==Counter({162:160}),
        "projective_column_weight_16": Counter(int(x) for x in Q.sum(axis=0))==Counter({16:1620}),
        "signed_entries_binary": set(int(x) for x in M.flatten())=={0,1},
        "projective_entries_binary": set(int(x) for x in Q.flatten())=={0,1},
        "signed_rank_160": signed_rank==160,
        "projective_rank_40": projective_rank==40,
        "signed_spectrum_closed": signed_eigs==Counter({0:160,80:81,112:24,144:30,464:24,1296:1}),
        "projective_spectrum_closed": projective_eigs==Counter({0:120,288:15,792:24,2592:1}),
    }

    results={
        "theorem":"BT512 Signed/Projective Xmin Lift Spectrum Theorem",
        "summary":{
            "ordinary_quadrangles":len(quads),
            "signed_faces":len(signed_faces),
            "projective_pairs":len(projective_pairs),
            "signed_matrix_shape":[int(x) for x in M.shape],
            "projective_matrix_shape":[int(x) for x in Q.shape],
            "signed_rank":signed_rank,
            "projective_rank":projective_rank,
            "all_checks_passed":all(checks.values()),
        },
        "checks":checks,
        "degree_data":{
            "signed_row_degree":81,
            "signed_column_weight":16,
            "projective_row_degree":162,
            "projective_column_weight":16,
            "signed_total_incidence":int(M.sum()),
            "projective_total_incidence":int(Q.sum()),
        },
        "spectra":{
            "signed_MMt":dict(sorted(signed_eigs.items())),
            "projective_QQt":dict(sorted(projective_eigs.items())),
        },
        "multiplicity_reading":{
            "projective_nonzero_multiplicities":"1,24,15 recover W33 SRG spectral multiplicities",
            "signed_extra_sector":"signed lift adds 81 plus a 30-dimensional split sector and another 24-dimensional sector",
            "nullities":"signed nullity 160 equals projective pair count; projective nullity 120 equals E8 root-pair count",
        },
        "substrate_reading":{
            "81":"signed Xmin lift degree and protected Levi/W33 H1 multiplicity",
            "160":"rank of signed lift and count of projective Xmin pairs",
            "40":"rank of projective quotient and count of W33 points/lines",
            "120":"projective nullity and E8 root-pair / 600-cell vertex count",
            "1296":"16*81 top signed eigenvalue = column weight times signed row degree",
            "2592":"16*162 top projective eigenvalue = column weight times projective row degree",
        },
    }
    out=Path("data/PART_BT512_SIGNED_PROJECTIVE_XMIN_LIFT_SPECTRUM_results.json")
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(results,indent=2),encoding="utf-8")
    print(json.dumps(results,indent=2))
    return results

if __name__=="__main__":
    main()
