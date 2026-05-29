#!/usr/bin/env python3
"""PG(3,3) symplectic generalized-quadrangle anchor graph theorem.

This is the exact next step after the PG(3,3) phase-space bridge.

The 40 W33 anchors are not merely the points of PG(3,3).  W(3,3) is the
symplectic generalized quadrangle inside PG(3,3): points are all projective
points of PG(3,3), and lines are the totally isotropic projective lines for a
nondegenerate alternating form on F3^4.

For q=3, every point is isotropic because the form is alternating, but not every
projective line is isotropic.  The isotropic lines give the W(3,3) incidence
geometry.

Verified here:
    points = 40
    isotropic lines = 40
    points per line = 4
    lines per point = 4
    collinearity graph vertices = 40
    degree = 12
    edges = 240
    strongly regular parameters = (40,12,2,4)
    spectrum = 12^1 + 2^24 + (-4)^15

This identifies the W33 anchor graph as the collinearity graph of the
symplectic GQ W(3,3), while the previous theorem identified the 81 phase states
as F3^4 itself.
"""
from __future__ import annotations

import itertools
import json
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np

q=3
D=4
V=40
LINES_W33=40
PTS_PER_LINE=4
LINES_PER_POINT=4
DEGREE=12
EDGES=240
H1=81
Q4_VERTICES=16
WE6=51_840
X_RAYS=160


def rank_modp(M: np.ndarray, p:int=q)->int:
    A=[[int(x)%p for x in row] for row in M.tolist()]
    if not A: return 0
    m=len(A); n=len(A[0]); rank=0; col=0
    while rank<m and col<n:
        piv=next((i for i in range(rank,m) if A[i][col]%p), None)
        if piv is None:
            col+=1; continue
        A[rank],A[piv]=A[piv],A[rank]
        inv=pow(A[rank][col],-1,p)
        A[rank]=[(x*inv)%p for x in A[rank]]
        for i in range(m):
            if i!=rank and A[i][col]%p:
                fac=A[i][col]%p
                A[i]=[(x-fac*y)%p for x,y in zip(A[i],A[rank])]
        rank+=1; col+=1
    return rank


def vectors():
    return list(itertools.product(range(q), repeat=D))


def nonzero_vectors():
    return [x for x in vectors() if any(x)]


def normalize(v):
    v=tuple(x%q for x in v)
    if not any(v): raise ValueError("zero")
    i=next(i for i,x in enumerate(v) if x%q)
    inv=pow(v[i],-1,q)
    return tuple((x*inv)%q for x in v)


def pg_points():
    return sorted({normalize(v) for v in nonzero_vectors()})


def symp(a,b):
    # Standard alternating form with matrix [[0,I],[-I,0]].
    return (a[0]*b[2] + a[1]*b[3] - a[2]*b[0] - a[3]*b[1]) % q


def span_line(a,b):
    pts=set()
    for x,y in itertools.product(range(q), repeat=2):
        v=tuple((x*a[i]+y*b[i])%q for i in range(D))
        if any(v): pts.add(normalize(v))
    return tuple(sorted(pts))


def all_pg_lines(points):
    lines=set()
    for a,b in itertools.combinations(points,2):
        L=span_line(a,b)
        if len(L)==q+1: lines.add(L)
    return sorted(lines)


def isotropic_lines(points):
    lines=[]
    for L in all_pg_lines(points):
        ok=True
        for a,b in itertools.combinations(L,2):
            if symp(a,b)!=0:
                ok=False; break
        if ok: lines.append(L)
    return lines


def collinearity_graph(points, lines):
    pidx={p:i for i,p in enumerate(points)}
    A=np.zeros((len(points),len(points)), dtype=int)
    for L in lines:
        for a,b in itertools.combinations(L,2):
            i,j=pidx[a],pidx[b]
            A[i,j]=A[j,i]=1
    return A


def common_neighbor_counts(A):
    n=A.shape[0]
    adjacent=[]; nonadj=[]
    for i,j in itertools.combinations(range(n),2):
        c=int(np.dot(A[i],A[j]))
        if A[i,j]: adjacent.append(c)
        else: nonadj.append(c)
    return Counter(adjacent),Counter(nonadj)


def find_isotropic_spread(points, lines):
    point_to_lines={p:[] for p in points}
    for i,L in enumerate(lines):
        for p in L: point_to_lines[p].append(i)
    def backtrack(remaining, chosen):
        if not remaining: return chosen
        p=min(remaining, key=lambda x: sum(set(lines[i]).issubset(remaining) for i in point_to_lines[x]))
        for i in point_to_lines[p]:
            L=set(lines[i])
            if L.issubset(remaining):
                got=backtrack(remaining-L, chosen+[i])
                if got is not None: return got
        return None
    sol=backtrack(set(points), [])
    if sol is None: raise RuntimeError("no spread")
    return [lines[i] for i in sol]


def line_intersection_counts(lines):
    counts=Counter()
    for a,b in itertools.combinations(lines,2):
        counts[len(set(a)&set(b))]+=1
    return counts


def build_payload():
    pts=pg_points()
    all_lines=all_pg_lines(pts)
    iso=isotropic_lines(pts)
    A=collinearity_graph(pts,iso)
    degrees=Counter(A.sum(axis=1).astype(int).tolist())
    edge_count=int(A.sum()//2)
    adj_cn,nonadj_cn=common_neighbor_counts(A)
    eig=np.linalg.eigvalsh(A)
    eig_counts=Counter(round(float(x),8) for x in eig)
    point_line_count=Counter(p for L in iso for p in L)
    spread=find_isotropic_spread(pts,iso)
    spread_points=[p for L in spread for p in L]
    line_intersections=line_intersection_counts(iso)

    # Symplectic polar hyperplanes: each point is collinear with 1+self+12 = 13 projective points in polar plane.
    polar_sizes=[]
    for p in pts:
        polar=[x for x in pts if symp(p,x)==0]
        polar_sizes.append(len(polar))

    checks={
        "phase_space_81": len(vectors())==H1,
        "projective_points_40": len(pts)==V,
        "all_PG33_lines_130": len(all_lines)==130,
        "isotropic_lines_40": len(iso)==LINES_W33,
        "each_isotropic_line_has_4_points": all(len(L)==PTS_PER_LINE for L in iso),
        "each_point_on_4_isotropic_lines": set(point_line_count.values())=={LINES_PER_POINT},
        "line_intersections_0_or_1": set(line_intersections.keys())=={0,1},
        "collinearity_vertices_40": A.shape==(V,V),
        "collinearity_degree_12": degrees=={DEGREE:V},
        "collinearity_edges_240": edge_count==EDGES,
        "strongly_regular_adjacent_lambda_2": adj_cn=={2:EDGES},
        "strongly_regular_nonadjacent_mu_4": nonadj_cn=={4:(V*(V-1)//2)-EDGES},
        "spectrum_12_2_minus4": eig_counts=={-4.0:15,2.0:24,12.0:1},
        "isotropic_spread_10_lines": len(spread)==10,
        "spread_partitions_40_points": len(set(spread_points))==V and len(spread_points)==V,
        "X_rays_as_spread_lines_times_Q4": X_RAYS==len(spread)*Q4_VERTICES,
        "X_rays_as_points_times_lines_per_point": X_RAYS==V*LINES_PER_POINT,
        "polar_plane_size_13": set(polar_sizes)=={13},
        "WE6_factorization": WE6==V*Q4_VERTICES*H1,
    }
    return {
        "theorem":"PG33_Symplectic_GQ_W33_Anchor_Graph",
        "phase_projective_layer":{
            "F3_4_phase_states":len(vectors()),
            "PG33_points":len(pts),
            "all_PG33_lines":len(all_lines),
            "interpretation":"W33 anchors are PG(3,3) points, i.e. nonzero F3^4 phase vectors modulo ±1."
        },
        "symplectic_GQ_W33":{
            "form":"<x,y>=x0*y2+x1*y3-x2*y0-x3*y1 mod 3",
            "points":len(pts),
            "totally_isotropic_lines":len(iso),
            "points_per_line":PTS_PER_LINE,
            "lines_per_point":LINES_PER_POINT,
            "polar_plane_size_per_point":sorted(set(polar_sizes)),
            "line_intersection_distribution":dict(line_intersections),
            "interpretation":"W(3,3) is the incidence geometry of PG(3,3) points and totally isotropic lines."
        },
        "collinearity_graph":{
            "vertices":A.shape[0],
            "degree_distribution":dict(degrees),
            "edges":edge_count,
            "strongly_regular_parameters":"(40,12,2,4)",
            "adjacent_common_neighbors":dict(adj_cn),
            "nonadjacent_common_neighbors":dict(nonadj_cn),
            "spectrum":dict(eig_counts)
        },
        "spread_router_bridge":{
            "isotropic_spread_lines":len(spread),
            "spread_line_size":PTS_PER_LINE,
            "spread_partitions_points":len(set(spread_points))==V,
            "X_rays":"160=10*16=40*4",
            "spread_lines":[[list(p) for p in L] for L in spread]
        },
        "global_factorization":{
            "WE6":"51840=40*16*81",
            "meaning":"symplectic PG(3,3) anchors * Q4 router states * F3^4 phase states"
        },
        "honest_interpretation":"The W33 graph itself is the collinearity graph of the symplectic generalized quadrangle W(3,3). This upgrades the previous PG(3,3) projective-anchor bridge by adding the correct symplectic incidence relation that yields 240 edges and degree 12.",
        "identities":checks,
        "all_identities_hold":bool(all(checks.values()))
    }


def main():
    payload=build_payload()
    out=Path("data/w33_pg33_symplectic_gq_anchor_graph.json")
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(payload,indent=2,sort_keys=True),encoding="utf-8")
    print(json.dumps({"all_identities_hold":payload["all_identities_hold"],"phase_projective_layer":payload["phase_projective_layer"],"symplectic_GQ_W33":payload["symplectic_GQ_W33"],"collinearity_graph":payload["collinearity_graph"],"spread_router_bridge":payload["spread_router_bridge"]},indent=2,sort_keys=True))
    print(f"wrote {out}")

if __name__=="__main__":
    main()
