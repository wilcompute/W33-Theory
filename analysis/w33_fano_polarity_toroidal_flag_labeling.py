#!/usr/bin/env python3
"""Explicit Fano polarity labeling of the 84 toroidal flag codec.

Previous theorem proved the abstract shared decomposition

    Fano 84 = 7 chart axes * 12 directed K4-edge states
             = Csaszar 7 vertex axes * 12 local vertex flags
             = Szilassi 7 face axes * 12 local face flags.

This verifier adds an explicit seven-axis labeling using Fano polarity.

Work in the Fano plane PG(2,2), represented by nonzero vectors of F2^3.  Lines
are triples {a,b,a+b}.  Use the polarity

    point n  <->  line n^perp = {x != 0 : n·x = 0}.

A Fano chart state is:

    L = chosen line at infinity,
    p = affine anchor in PG(2,2) \ L,
    d = direction in L,
    q = p+d,
    M = line(p,q) = {p,q,d}.

Since M != L, each state is equivalently

    (L, M, orientation of the two affine points M\L).

This gives 7*6*2 = 84 states.

Szilassi labeling:
    face axis = L,
    adjacent face = M,
    side/orientation = ordered affine pair p->q.

Csaszar labeling via polarity:
    vertex axis = polar(L),
    adjacent vertex = polar(M),
    side/orientation = ordered affine pair p->q.

The verifier checks both maps are bijections onto 84 labeled flag states.
"""
from __future__ import annotations

import itertools
import json
from collections import Counter
from pathlib import Path

Vec3 = tuple[int, int, int]
Line = tuple[Vec3, Vec3, Vec3]


def add(a: Vec3, b: Vec3) -> Vec3:
    return tuple((x + y) % 2 for x, y in zip(a, b))  # type: ignore[return-value]


def dot(a: Vec3, b: Vec3) -> int:
    return sum(x * y for x, y in zip(a, b)) % 2


def points() -> list[Vec3]:
    return sorted(v for v in itertools.product(range(2), repeat=3) if any(v))


def line_from_pair(a: Vec3, b: Vec3) -> Line:
    return tuple(sorted((a, b, add(a, b))))  # type: ignore[return-value]


def lines(P: list[Vec3]) -> list[Line]:
    return sorted({line_from_pair(a, b) for a, b in itertools.combinations(P, 2)})


def polar_line(n: Vec3, P: list[Vec3]) -> Line:
    return tuple(sorted(x for x in P if dot(n, x) == 0))  # type: ignore[return-value]


def polarity_maps(P: list[Vec3], Ls: list[Line]):
    point_to_line = {p: polar_line(p, P) for p in P}
    line_to_point = {L: p for p, L in point_to_line.items()}
    return point_to_line, line_to_point


def fano_chart_states(P: list[Vec3], Ls: list[Line]):
    states = []
    for L in Ls:
        infinity = set(L)
        affine = sorted(set(P) - infinity)
        for p in affine:
            for d in L:
                q = add(p, d)
                assert q in affine and q != p
                M = line_from_pair(p, q)
                assert M != L and d in M
                states.append({"infinity_line": L, "anchor": p, "direction": d, "target": q, "affine_line": M})
    return states


def build_payload() -> dict:
    P = points()
    Ls = lines(P)
    p2l, l2p = polarity_maps(P, Ls)
    states = fano_chart_states(P, Ls)

    # State as ordered pair of distinct Fano lines plus orientation on their unique non-infinity pair.
    linepair_oriented = []
    sz_flags = []
    cs_flags = []
    for s in states:
        L = s["infinity_line"]
        M = s["affine_line"]
        p = s["anchor"]
        q = s["target"]
        orientation = (p, q)
        linepair_oriented.append((L, M, orientation))
        sz_flags.append((L, M, orientation))
        cs_flags.append((l2p[L], l2p[M], orientation))

    unique_linepair = set(linepair_oriented)
    unique_sz = set(sz_flags)
    unique_cs = set(cs_flags)

    # Check each ordered distinct line pair has exactly two orientations.
    linepair_counts = Counter((L, M) for L, M, _o in linepair_oriented)
    cs_vertex_neighbor_counts = Counter((v, w) for v, w, _o in cs_flags)
    sz_face_neighbor_counts = Counter((f, g) for f, g, _o in sz_flags)

    # Axis distributions.
    cs_axis_counts = Counter(v for v, _w, _o in cs_flags)
    sz_axis_counts = Counter(f for f, _g, _o in sz_flags)
    cs_neighbor_counts_per_axis = {v: len({w for vv, w, _o in cs_flags if vv == v}) for v in P}
    sz_neighbor_counts_per_axis = {L: len({M for LL, M, _o in sz_flags if LL == L}) for L in Ls}

    identities = {
        "fano_points_lines_7_7": len(P) == 7 and len(Ls) == 7,
        "polarity_bijection": len(p2l) == 7 and len(l2p) == 7 and all(l2p[p2l[p]] == p for p in P),
        "fano_chart_states_84": len(states) == 84,
        "states_equiv_ordered_distinct_line_pair_times_orientation": len(unique_linepair) == 84 and linepair_counts and set(linepair_counts.values()) == {2} and len(linepair_counts) == 42,
        "szilassi_flag_labels_84": len(unique_sz) == 84,
        "csaszar_flag_labels_84": len(unique_cs) == 84,
        "szilassi_axes_7_each_12": set(sz_axis_counts.values()) == {12} and len(sz_axis_counts) == 7,
        "csaszar_axes_7_each_12": set(cs_axis_counts.values()) == {12} and len(cs_axis_counts) == 7,
        "szilassi_each_face_has_6_neighbors_each_two_sides": set(sz_neighbor_counts_per_axis.values()) == {6} and set(sz_face_neighbor_counts.values()) == {2},
        "csaszar_each_vertex_has_6_neighbors_each_two_sides": set(cs_neighbor_counts_per_axis.values()) == {6} and set(cs_vertex_neighbor_counts.values()) == {2},
    }
    return {
        "theorem": "fano_polarity_toroidal_flag_labeling",
        "polarity": {
            "definition": "point n maps to line n^perp={x!=0:n·x=0}; lines map back to their polar point",
            "point_to_line": {str(k): v for k, v in p2l.items()},
            "line_to_point": {str(k): v for k, v in l2p.items()},
        },
        "state_equivalence": {
            "fano_chart_state": "(infinity line L, affine anchor p, direction d, target q=p+d)",
            "line_pair_state": "(ordered distinct Fano lines L,M=line(p,q), orientation p->q on M\\L)",
            "count": len(unique_linepair),
        },
        "szilassi_labeling": {
            "rule": "face axis=L, adjacent face=M, side/orientation=p->q",
            "flag_count": len(unique_sz),
            "axis_count_distribution": dict(Counter(sz_axis_counts.values())),
            "neighbor_count_distribution": dict(Counter(sz_neighbor_counts_per_axis.values())),
        },
        "csaszar_labeling": {
            "rule": "vertex axis=polar(L), adjacent vertex=polar(M), side/orientation=p->q",
            "flag_count": len(unique_cs),
            "axis_count_distribution": dict(Counter(cs_axis_counts.values())),
            "neighbor_count_distribution": dict(Counter(cs_neighbor_counts_per_axis.values())),
        },
        "interpretation": {
            "proved": "A Fano chart state is equivalently an ordered pair of distinct Fano lines with a two-valued orientation. Via polarity, this is also an ordered pair of distinct Fano points with orientation, matching the Csaszar K7 vertex flag model. Without polarity, it matches the Szilassi complete face-adjacency flag model.",
            "duality": "Szilassi uses line/face axes directly; Csaszar uses polar point/vertex axes. This realizes the vertex-face duality by Fano polarity.",
            "boundary": "This is a canonical Fano incidence labeling of the abstract 84 flags. Matching a specific geometric drawing of Csaszar/Szilassi still requires choosing its seven vertices/faces to be these Fano axes.",
        },
        "sample_states": states[:8],
        "sample_cs_flags": cs_flags[:8],
        "sample_sz_flags": sz_flags[:8],
        "identities": identities,
        "all_identities_hold": all(identities.values()),
    }


def main() -> None:
    payload = build_payload()
    out = Path("data/w33_fano_polarity_toroidal_flag_labeling.json")
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
