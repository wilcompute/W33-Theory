#!/usr/bin/env python3
"""Quadrangle-corner hypergraph spectrum for local W33 octahedra.

Long shot tested:
  If quadrangles glue the local pencil-octahedra through their corner states,
  then the 240 local-octahedron vertices versus 1620 quadrangles should form a
  meaningful incidence design, not just a double count.

Result:
  Let B be the 240 x 1620 unsigned incidence matrix whose rows are local
  octahedron corner states (point p plus two lines through p) and whose columns
  are ordinary quadrangles.  B[v,Q]=1 iff v is one of the four octahedral corner
  states of Q.

  B has full row rank 240.  Every row has degree 27=q^3, every column has weight 4,
  and the corner Gram spectrum is

    108^1, 60^24, 36^15, 30^60, 20^81, 18^44, 12^15.

The spectrum contains the W33 SRG multiplicities 1,24,15 and the Levi-cycle
multiplicity 81, suggesting the corner hypergraph is the transfer layer between
local octahedra, W33 adjacency, and the Levi homology frame.
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


def main() -> int:
    points, edges, adj, lines, point_lines, edge_to_line = build_geometry()
    local_vertices=sorted((p, tuple(sorted(pair))) for p in range(len(points)) for pair in combinations(sorted(point_lines[p]),2))
    lv_idx={v:i for i,v in enumerate(local_vertices)}
    quads=ordinary_quadrangles(adj)
    B=np.zeros((len(local_vertices), len(quads)), dtype=np.int8)
    for qi,cyc in enumerate(quads):
        inc=defaultdict(list)
        for u,v in cyc:
            inc[u].append((u,v)); inc[v].append((u,v))
        for p,es in inc.items():
            lpair=tuple(sorted(edge_to_line[tuple(sorted(e))] for e in es))
            B[lv_idx[(p,lpair)], qi]=1

    G=B@B.T
    eigs=np.linalg.eigvalsh(G.astype(float))
    eig_counter=Counter(int(round(x)) for x in eigs)
    off_counter=Counter(int(x) for x in G[np.triu_indices(G.shape[0],1)].tolist())
    rank=int(np.linalg.matrix_rank(B.astype(float)))
    checks={
        "geometry_counts": len(points)==40 and len(lines)==40 and len(edges)==240 and len(local_vertices)==240 and len(quads)==1620,
        "row_degree_27": Counter(int(x) for x in B.sum(axis=1)) == Counter({27:240}),
        "column_weight_4": Counter(int(x) for x in B.sum(axis=0)) == Counter({4:1620}),
        "total_incidence": int(B.sum()) == 6480 == 240*27 == 1620*4,
        "full_row_rank_240": rank == 240,
        "gram_diag_27": Counter(int(x) for x in np.diag(G)) == Counter({27:240}),
        "off_values_0_1_3": set(off_counter) == {0,1,3},
        "spectrum_closed": eig_counter == Counter({108:1,60:24,36:15,30:60,20:81,18:44,12:15}),
    }
    payload={
        "theorem_name": "Octahedron Corner Hypergraph Spectrum Theorem",
        "summary": {
            "local_octahedron_corner_states": len(local_vertices),
            "ordinary_quadrangles": len(quads),
            "matrix_shape": [int(x) for x in B.shape],
            "rank": rank,
            "row_degree": 27,
            "column_weight": 4,
            "total_incidence": int(B.sum()),
            "all_checks_passed": all(checks.values()),
        },
        "checks": checks,
        "corner_gram_off_diagonal_distribution": dict(sorted(off_counter.items())),
        "corner_gram_spectrum": dict(sorted(eig_counter.items())),
        "identities": {
            "incidence": "240*27 = 1620*4 = 6480",
            "spectrum": "Spec(BB^T)=108^1+60^24+36^15+30^60+20^81+18^44+12^15",
            "physics_long_shot": "The spectrum contains W33 adjacency multiplicities 1,24,15 and Levi-cycle multiplicity 81, suggesting a transfer layer from local gauge codec corners to protected homology.",
        },
    }
    root=Path(__file__).resolve().parents[1]
    out=root/"data"/"w33_octahedron_corner_hypergraph_spectrum.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, indent=2, sort_keys=True)+"\n", encoding="utf-8")
    print(json.dumps(payload["summary"], indent=2, sort_keys=True))
    return 0 if payload["summary"]["all_checks_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
