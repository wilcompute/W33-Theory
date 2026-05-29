#!/usr/bin/env python3
"""PG(3,3) phase-space spread bridge.

This continues the Q4/Fano chain-complex homology theorem.

Key correction:
    The 40 W33 anchors should not be read as 40 independent copies of a local
    4-mode qutrit fiber.  Instead, the four qutrit modes form one global vector
    space F3^4, and the 40 anchors are exactly its projective nonzero directions:

        |PG(3,3)_points| = (3^4 - 1)/(3 - 1) = 40.

Thus:
    81 = |F3^4| is the global qutrit phase-state count.
    40 = |PG(3,3)| is the projectivized anchor count.
    160 = 40*(3+1) = 10*16 links the projective line size 4, W33 degree 10,
          and Q4 router states 16.

The verifier also constructs a line spread of PG(3,3): 10 disjoint projective
lines, each with q+1=4 points, partitioning the 40 anchors.  This identifies

    E1 = 10 = number of spread lines,
    chi = 4 = points per spread line,
    v = 40 = spread lines * line size,
    X_min rays = 160 = spread lines * Q4 vertices.

Finally, the 81x81 additive character table of F3^4 has full rank 81, giving the
correct phase-frame state space before projectivization.
"""
from __future__ import annotations

import itertools
import json
from collections import Counter
from pathlib import Path

import numpy as np

q=3
D=4
H1=81
v=40
E1=10
chi=4
Q4_VERTICES=16
X_RAYS=160
Z_RAYS=1620
WE6=51_840


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
    if not any(v):
        raise ValueError("zero vector has no projective normalization")
    i=next(i for i,x in enumerate(v) if x%q)
    inv=pow(v[i],-1,q)
    return tuple((x*inv)%q for x in v)


def pg_points():
    return sorted({normalize(v) for v in nonzero_vectors()})


def span_line(a,b):
    pts=set()
    for x in range(q):
        for y in range(q):
            v=tuple((x*a[i]+y*b[i])%q for i in range(D))
            if any(v):
                pts.add(normalize(v))
    return tuple(sorted(pts))


def pg_lines(points):
    lines=set()
    for a,b in itertools.combinations(points,2):
        L=span_line(a,b)
        if len(L)==q+1:
            lines.add(L)
    return sorted(lines)


def pg_planes(points):
    planes=set()
    for a,b,c in itertools.combinations(points,3):
        # span of three point representatives; if dimension 3, projective plane has q^2+q+1=13 points.
        rows=np.array([a,b,c], dtype=int)
        if rank_modp(rows) != 3:
            continue
        pts=set()
        for x,y,z in itertools.product(range(q), repeat=3):
            v=tuple((x*a[i]+y*b[i]+z*c[i])%q for i in range(D))
            if any(v): pts.add(normalize(v))
        if len(pts)==q*q+q+1:
            planes.add(tuple(sorted(pts)))
    return sorted(planes)


def find_line_spread(points, lines):
    point_to_lines={p:[] for p in points}
    for idx,L in enumerate(lines):
        for p in L:
            point_to_lines[p].append(idx)
    def backtrack(remaining, chosen):
        if not remaining:
            return chosen
        p=min(remaining, key=lambda x: sum(set(lines[i]).issubset(remaining) for i in point_to_lines[x]))
        for i in point_to_lines[p]:
            L=set(lines[i])
            if L.issubset(remaining):
                got=backtrack(remaining-L, chosen+[i])
                if got is not None:
                    return got
        return None
    sol=backtrack(set(points), [])
    if sol is None:
        raise RuntimeError("no spread found")
    return [lines[i] for i in sol]


def dot(a,b):
    return sum(x*y for x,y in zip(a,b))%q


def additive_character_exponent_table(vecs):
    # Exponent table E[a,b]=a dot b over F3. Complex character table omega^E has same rank over C.
    return np.array([[dot(a,b) for b in vecs] for a in vecs], dtype=int)


def complex_character_rank(vecs):
    omega=np.exp(2j*np.pi/q)
    E=additive_character_exponent_table(vecs)
    M=omega**E
    return int(np.linalg.matrix_rank(M, tol=1e-9))


def build_payload():
    V=vectors(); NZ=nonzero_vectors(); PTS=pg_points(); LNS=pg_lines(PTS); PLN=pg_planes(PTS)
    spread=find_line_spread(PTS,LNS)
    spread_points=[p for L in spread for p in L]
    point_line_degrees=Counter()
    for L in LNS:
        for p in L: point_line_degrees[p]+=1
    line_plane_degrees=Counter()
    for i,L in enumerate(LNS):
        s=set(L)
        for plane in PLN:
            if s.issubset(set(plane)):
                line_plane_degrees[i]+=1
    plane_point_sizes=Counter(len(P) for P in PLN)
    line_sizes=Counter(len(L) for L in LNS)
    spread_line_sizes=Counter(len(L) for L in spread)
    exponent_table=additive_character_exponent_table(V)
    char_rank=complex_character_rank(V)

    checks={
        "F3_4_has_81_phase_states": len(V)==H1==q**D,
        "nonzero_vectors_80": len(NZ)==80,
        "projective_points_40": len(PTS)==v==(q**D-1)//(q-1),
        "projective_lines_130": len(LNS)==130,
        "projective_planes_40": len(PLN)==40,
        "line_size_4": line_sizes=={q+1:len(LNS)},
        "plane_size_13": plane_point_sizes=={q*q+q+1:len(PLN)},
        "lines_through_each_point_13": set(point_line_degrees.values())=={13},
        "planes_through_each_line_4": set(line_plane_degrees.values())=={q+1},
        "spread_has_10_lines": len(spread)==E1,
        "spread_lines_are_disjoint_and_cover_40_points": len(set(spread_points))==v and len(spread_points)==v,
        "spread_line_size_4": spread_line_sizes=={chi:E1},
        "v_equals_E1_times_chi": v==E1*chi,
        "X_rays_equals_v_times_chi": X_RAYS==v*chi,
        "X_rays_equals_E1_times_Q4_vertices": X_RAYS==E1*Q4_VERTICES,
        "Z_rays_equals_40_times_40_plus_20": Z_RAYS==v*v+20,
        "character_table_rank_81": char_rank==H1,
        "projective_anchor_count_plus_phase_state_count": v+H1==121,
        "WE6_factorization_still": WE6==v*Q4_VERTICES*H1,
    }
    return {
        "theorem":"PG33_Phase_Space_Spread_Bridge",
        "phase_space":{
            "vector_space":"F3^4",
            "phase_states":len(V),
            "nonzero_vectors":len(NZ),
            "projective_points":len(PTS),
            "formula":"|PG(3,3)_points|=(3^4-1)/(3-1)=40",
            "character_table_rank":char_rank,
            "interpretation":"81 is the full affine qutrit phase-state count; 40 is its projectivized nonzero direction count."
        },
        "projective_geometry":{
            "points":len(PTS),
            "lines":len(LNS),
            "planes":len(PLN),
            "line_size":q+1,
            "plane_size":q*q+q+1,
            "lines_through_point":13,
            "planes_through_line":q+1
        },
        "spread_bridge":{
            "spread_lines":len(spread),
            "points_per_spread_line":q+1,
            "spread_partition":"10 disjoint projective lines partition the 40 anchors",
            "spread_lines_labeled":[[list(p) for p in L] for L in spread],
            "identities":["40=10*4", "160=40*4=10*16"]
        },
        "minimal_surface_bridge":{
            "X_min_rays":X_RAYS,
            "X_rays_as_v_times_chi":"160=40*4",
            "X_rays_as_E1_times_Q4":"160=10*16",
            "phase_frame_rank":"81=3^4 additive character states of F3^4",
            "WE6":"51840=40*16*81"
        },
        "honest_interpretation":"Do not fiber four independent qutrit modes over all 40 anchors. The four qutrit modes define F3^4 globally; the 40 W33 anchors are the projective directions of that same space. A PG(3,3) line spread then explains 40=10*4 and 160=10*16.",
        "identities":checks,
        "all_identities_hold":bool(all(checks.values()))
    }


def main():
    payload=build_payload()
    out=Path("data/w33_pg33_phase_space_spread_bridge.json")
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(payload,indent=2,sort_keys=True),encoding="utf-8")
    print(json.dumps({"all_identities_hold":payload["all_identities_hold"],"phase_space":payload["phase_space"],"projective_geometry":payload["projective_geometry"],"spread_bridge":payload["spread_bridge"],"minimal_surface_bridge":payload["minimal_surface_bridge"]},indent=2,sort_keys=True))
    print(f"wrote {out}")

if __name__=="__main__":
    main()
