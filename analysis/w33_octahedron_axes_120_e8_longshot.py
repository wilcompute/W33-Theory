#!/usr/bin/env python3
"""Local octahedron axes: a canonical 120-set inside W(3,3).

Long shot #3:
  Each local pencil-octahedron O_p has three antipodal vertex pairs / axes.
  Across 40 W33 points this gives 40*3 = 120 local axes.

The repo has repeatedly seen 120 as:
  - E8 root pairs / root lines (240/2),
  - vertices of the 600-cell,
  - 40 points * 3 local axes.

This script does not claim an explicit E8 bijection.  It proves the exact W33
side of the long shot: the canonical 120-set exists intrinsically as local
pencil-octahedron axes, and quadrangle corners distribute uniformly over it.

For each point p, the four lines through p form K4.  The three octahedron axes
are the three perfect matchings / partitions of these four pencil-lines into two
opposite line-pairs.  Since each local octahedron vertex is incident with 27
quadrangle corners and each axis has two opposite vertices, each axis sees
54=2*q^q quadrangle corners:

  120 axes * 54 = 1620 quadrangles * 4 corners = 6480.
"""
from __future__ import annotations

import json
from collections import Counter, defaultdict
from itertools import combinations, product
from pathlib import Path

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


def main() -> int:
    points, edges, adjacency, lines, point_lines, edge_to_line = build_w33()
    # Local axis keys: (point, matching of four line labels through point).  Each
    # matching is a pair of opposite local octahedron vertices.
    axes=[]
    vertex_to_axis={}
    for p in range(len(points)):
        Ls=sorted(point_lines[p])
        for ax in matchings_of_four(Ls):
            key=(p, ax)
            axes.append(key)
            for vtx in ax:
                vertex_to_axis[(p, tuple(sorted(vtx)))] = key

    quads=ordinary_quadrangles(adjacency)
    corner_axis_count=Counter()
    corner_vertex_count=Counter()
    for cyc in quads:
        incident=defaultdict(list)
        for u,v in cyc:
            incident[u].append((u,v)); incident[v].append((u,v))
        for p,es in incident.items():
            lpair=tuple(sorted(edge_to_line[tuple(sorted(e))] for e in es))
            corner_vertex_count[(p,lpair)] += 1
            corner_axis_count[vertex_to_axis[(p,lpair)]] += 1

    checks={
        "w33_counts": len(points)==40 and len(lines)==40 and len(edges)==240,
        "axes_count_120": len(axes)==120 and len(set(axes))==120,
        "local_axes_per_point": Counter(p for p,_ in axes)==Counter({p:3 for p in range(40)}),
        "local_vertices_count_240": len(vertex_to_axis)==240,
        "quadrangles_count_1620": len(quads)==1620,
        "vertex_corner_uniform_27": Counter(corner_vertex_count.values())==Counter({27:240}),
        "axis_corner_uniform_54": Counter(corner_axis_count.values())==Counter({54:120}),
        "axis_corner_double_count": sum(corner_axis_count.values())==6480==120*54==1620*4,
    }
    payload={
        "theorem_name":"Local Octahedron Axis 120-Set Long-Shot Theorem",
        "summary":{
            "w33_points": len(points),
            "local_axes_per_point": 3,
            "global_local_octahedron_axes": len(axes),
            "local_octahedron_vertices": len(vertex_to_axis),
            "ordinary_quadrangles": len(quads),
            "quadrangle_corners_per_axis": 54,
            "total_quadrangle_corners": sum(corner_axis_count.values()),
            "all_checks_passed": all(checks.values()),
        },
        "checks": checks,
        "axis_corner_distribution": dict(Counter(corner_axis_count.values())),
        "vertex_corner_distribution": dict(Counter(corner_vertex_count.values())),
        "identities":{
            "canonical_120_set":"40 W33 points * 3 local octahedron axes = 120.",
            "e8_longshot":"120 is the count of E8 root pairs / 600-cell vertices; this script proves the intrinsic W33 120-set but not yet an explicit E8 bijection.",
            "quadrangle_axis_uniformity":"Each local axis sees 54=2*q^q quadrangle corners.",
            "corner_count":"120*54=1620*4=6480.",
            "physical_read":"If local octahedron axes are SU(2)-like gauge axes, the canonical 120-set is a plausible interface between W33 local gauge codec and E8/600-cell root-pair geometry.",
        },
    }
    root=Path(__file__).resolve().parents[1]
    out=root/"data"/"w33_octahedron_axes_120_e8_longshot.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, indent=2, sort_keys=True)+"\n", encoding="utf-8")
    print(json.dumps(payload["summary"], indent=2, sort_keys=True))
    return 0 if payload["summary"]["all_checks_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
