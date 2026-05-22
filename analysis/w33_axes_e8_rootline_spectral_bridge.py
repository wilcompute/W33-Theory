#!/usr/bin/env python3
"""W33 local octahedron axes vs E8 root-line orthogonality graph.

This attacks the next target from the octahedral synthesis report:
  Can the canonical 120 local axes of W(3,3) carry the same structure as the
  120 E8 root lines / 600-cell vertices?

Honest result:
  The W33 local-axis graph is strongly regular with parameters
      SRG(120,63,30,36)
  and spectrum
      63^1 + 3^84 + (-9)^35.

  The E8 root-line orthogonality graph, built directly from the 240 E8 roots
  modulo antipodal pairs, has the same parameters and spectrum:
      SRG(120,63,30,36), spectrum 63^1 + 3^84 + (-9)^35.

Construction of the W33 graph:
  - each W33 point p has a local pencil-octahedron O_p;
  - O_p has 3 axes, giving 40*3=120 local axes;
  - two local axes are adjacent if they occur together as axis-corners of at
    least one ordinary quadrangle.

The weighted axis-quadrangle corner incidence matrix C has row degree 54 and
column weight 4.  Its Gram has off-diagonal values 0,2,3 and spectrum
      216^1 + 66^24 + 60^60 + 36^20 + 24^15.
The unweighted nonzero-overlap graph is the SRG above.

This proves an exact spectral bridge, not an explicit isomorphism/bijection.
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


def build_w33():
    points=[]; seen=set()
    for raw in product(range(P), repeat=4):
        if raw == (0,0,0,0):
            continue
        c=canonical(raw)
        if c not in seen:
            seen.add(c); points.append(c)
    pidx={p:i for i,p in enumerate(points)}
    edges=[(i,j) for i,j in combinations(range(len(points)),2) if omega(points[i],points[j]) == 0]
    adjacency=[[False]*len(points) for _ in points]
    for i,j in edges:
        adjacency[i][j]=adjacency[j][i]=True
    lines=set()
    for i,j in edges:
        u,v=points[i],points[j]
        line=set()
        for a,b in product(range(P), repeat=2):
            if a==0 and b==0:
                continue
            line.add(pidx[canonical((a*u[t] + b*v[t] for t in range(4)))])
        lines.add(tuple(sorted(line)))
    lines=sorted(lines)
    point_lines=defaultdict(list); edge_to_line={}
    for li,L in enumerate(lines):
        for p in L:
            point_lines[p].append(li)
        for e in combinations(L,2):
            edge_to_line[tuple(sorted(e))]=li
    return points, edges, adjacency, lines, point_lines, edge_to_line


def matchings_of_four(items):
    a,b,c,d=items
    return [
        tuple(sorted((tuple(sorted((a,b))), tuple(sorted((c,d)))))),
        tuple(sorted((tuple(sorted((a,c))), tuple(sorted((b,d)))))),
        tuple(sorted((tuple(sorted((a,d))), tuple(sorted((b,c)))))),
    ]


def ordinary_quadrangles(adjacency):
    quads=[]; seen=set()
    for a,b in combinations(range(len(adjacency)),2):
        if adjacency[a][b]:
            continue
        common=[x for x in range(len(adjacency)) if adjacency[a][x] and adjacency[b][x]]
        for c,d in combinations(common,2):
            cycle_edges=tuple(sorted(tuple(sorted(e)) for e in ((a,c),(c,b),(b,d),(d,a))))
            if cycle_edges not in seen:
                seen.add(cycle_edges); quads.append(cycle_edges)
    return quads


def w33_axis_incidence():
    points, edges, adjacency, lines, point_lines, edge_to_line = build_w33()
    axes=[]; vertex_to_axis={}
    for p in range(len(points)):
        Ls=sorted(point_lines[p])
        for ax in matchings_of_four(Ls):
            key=(p,ax); axes.append(key)
            for vtx in ax:
                vertex_to_axis[(p, tuple(sorted(vtx)))] = key
    axis_idx={a:i for i,a in enumerate(axes)}
    quads=ordinary_quadrangles(adjacency)
    C=np.zeros((len(axes), len(quads)), dtype=np.int8)
    for qi,cyc in enumerate(quads):
        incident=defaultdict(list)
        for u,v in cyc:
            incident[u].append((u,v)); incident[v].append((u,v))
        for p,es in incident.items():
            lpair=tuple(sorted(edge_to_line[tuple(sorted(e))] for e in es))
            C[axis_idx[vertex_to_axis[(p,lpair)]], qi]=1
    return C, len(points), len(lines), len(edges), len(quads), len(axes)


def build_e8_roots():
    roots=[]
    for i in range(8):
        for j in range(i+1,8):
            for si in (1,-1):
                for sj in (1,-1):
                    r=[0]*8; r[i]=si; r[j]=sj
                    roots.append(tuple(r))
    for signs in product((1,-1), repeat=8):
        if sum(1 for s in signs if s == -1) % 2 == 0:
            roots.append(tuple(s/2 for s in signs))
    return np.array(roots, dtype=float)


def e8_root_lines():
    roots=build_e8_roots()
    used=set(); reps=[]
    for i in range(len(roots)):
        if i in used:
            continue
        for j in range(i+1, len(roots)):
            if j in used:
                continue
            if np.allclose(roots[i] + roots[j], 0):
                used.add(i); used.add(j); reps.append(roots[i])
                break
    return np.array(reps), roots


def srg_params(A: np.ndarray):
    n=A.shape[0]
    deg=Counter(int(x) for x in A.sum(axis=1))
    lambdas=Counter(); mus=Counter()
    for i,j in combinations(range(n),2):
        common=int(A[i] @ A[j])
        if A[i,j]:
            lambdas[common]+=1
        else:
            mus[common]+=1
    eig=Counter(int(round(x)) for x in np.linalg.eigvalsh(A.astype(float)))
    return deg, lambdas, mus, eig


def main() -> int:
    C, npoints, nlines, nedges, nquads, naxes = w33_axis_incidence()
    G=C@C.T
    A_w33=(G>0).astype(int)
    np.fill_diagonal(A_w33, 0)
    w_deg,w_lam,w_mu,w_eig=srg_params(A_w33)
    wg_eig=Counter(int(round(x)) for x in np.linalg.eigvalsh(G.astype(float)))
    wg_off=Counter(int(x) for x in G[np.triu_indices(G.shape[0],1)])

    line_reps, roots=e8_root_lines()
    dots=np.abs(line_reps @ line_reps.T)
    A_e8=np.isclose(dots,0).astype(int)
    np.fill_diagonal(A_e8,0)
    e_deg,e_lam,e_mu,e_eig=srg_params(A_e8)
    absdot_counts=Counter(float(x) for x in np.round(dots[np.triu_indices(120,1)],6))

    checks={
        "w33_geometry_counts": npoints==40 and nlines==40 and nedges==240 and nquads==1620 and naxes==120,
        "axis_incidence_counts": Counter(int(x) for x in C.sum(axis=1)) == Counter({54:120}) and Counter(int(x) for x in C.sum(axis=0)) == Counter({4:1620}),
        "axis_graph_srg": w_deg==Counter({63:120}) and w_lam==Counter({30:3780}) and w_mu==Counter({36:3360}),
        "e8_root_lines": len(roots)==240 and len(line_reps)==120,
        "e8_orthogonality_srg": e_deg==Counter({63:120}) and e_lam==Counter({30:3780}) and e_mu==Counter({36:3360}),
        "spectra_match": w_eig==e_eig==Counter({-9:35,3:84,63:1}),
        "weighted_axis_gram_spectrum": wg_eig==Counter({24:15,36:20,60:60,66:24,216:1}),
    }
    payload={
        "theorem_name":"W33 Axis / E8 Root-Line Spectral Bridge Theorem",
        "summary":{
            "w33_local_axes":naxes,
            "e8_root_lines":len(line_reps),
            "w33_axis_graph_parameters":"SRG(120,63,30,36)",
            "e8_rootline_orthogonality_parameters":"SRG(120,63,30,36)",
            "shared_spectrum":"63^1 + 3^84 + (-9)^35",
            "axis_quadrangle_incidence_shape":[int(x) for x in C.shape],
            "axis_row_degree":54,
            "quadrangle_column_weight":4,
            "all_checks_passed":all(checks.values()),
        },
        "checks":checks,
        "w33_axis_graph":{
            "degree_distribution":dict(w_deg),
            "lambda_distribution":dict(w_lam),
            "mu_distribution":dict(w_mu),
            "spectrum":dict(w_eig),
        },
        "e8_rootline_orthogonality_graph":{
            "degree_distribution":dict(e_deg),
            "lambda_distribution":dict(e_lam),
            "mu_distribution":dict(e_mu),
            "spectrum":dict(e_eig),
            "absolute_dot_products_unordered":dict(absdot_counts),
        },
        "weighted_w33_axis_quadrangle_gram":{
            "off_diagonal_distribution":dict(wg_off),
            "spectrum":dict(wg_eig),
        },
        "identities":{
            "w33_axis_set":"40 local octahedra * 3 axes = 120.",
            "axis_quadrangle_count":"120*54=1620*4=6480.",
            "spectral_bridge":"The W33 axis adjacency graph has the same SRG parameters and spectrum as the E8 root-line orthogonality graph.",
            "honesty_boundary":"This proves a spectral/SRG-parameter bridge, not an explicit labeled bijection or E8 coordinate embedding of the axes.",
        },
    }
    root=Path(__file__).resolve().parents[1]
    out=root/"data"/"w33_axes_e8_rootline_spectral_bridge.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, indent=2, sort_keys=True)+"\n", encoding="utf-8")
    print(json.dumps(payload["summary"], indent=2, sort_keys=True))
    return 0 if payload["summary"]["all_checks_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
