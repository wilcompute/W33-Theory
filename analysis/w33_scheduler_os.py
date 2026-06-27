#!/usr/bin/env python3
"""
The scheduler: the wires partition into 40 four-way buses, the links run on a 12-slot conflict-free
frame, and the readout contexts provably DO NOT parallelize -- contextuality, seen by the scheduler.
The missing layer above the datapath is resource management: who uses which wire, and when. The
substrate answers it from its own geometry, and the answers include an honest negative that is the
contextuality of Pass 37 showing up as a scheduling obstruction. Three results. (1) THE BUS MAP: the
240 links partition EXACTLY into the 40 lines of GQ(3,3), each a 4-clique (every edge lies on a unique
line), so the wiring is 40 four-way buses, not 240 independent point links -- the natural
communication primitive is a line-local 4-way exchange. (2) THE LINK SCHEDULE: the collinearity graph
is 1-FACTORABLE -- it decomposes into 12 perfect matchings (computed here) -- so a conflict-free
point-to-point schedule needs exactly 12 time slots, in each of which every node drives exactly one of
its 12 ports; the frame length is the radix, 12, the minimum possible, and load is perfectly balanced
because the graph is vertex- and edge-transitive (no node or link waits longer than another). (3) THE
READOUT SCHEDULE AND ITS OBSTRUCTION: a SPREAD -- 10 pairwise-disjoint lines covering all 40 nodes --
exists, so 10 readout contexts can be measured in parallel in one slot; but the 40 contexts do NOT
resolve into 4 parallel spreads (a backtracking search proves no such partition exists), so the full
readout cannot be scheduled in 4 conflict-free rounds. That non-resolvability is exactly measurement
incompatibility -- the contextuality that fuels the magic -- appearing as a hard scheduling
constraint: the contexts overlap in a way no parallel schedule can untangle. And fairness is free: the
W(E6) automorphism group acts transitively on nodes, links, and contexts, so any schedule symmetrizes
to a hot-spot-free one. So the OS layer is: 40 four-way buses, a 12-slot conflict-free link frame,
parallel readout up to a spread of 10 but provably not fully parallelizable, and symmetry-guaranteed
fairness -- the resource manager read off the geometry, contextuality included.

This builds the scheduling / resource-management layer on GQ(3,3): the bus decomposition, the 12-slot
1-factorization link schedule, the spread-based readout schedule and its provable non-resolvability,
and the symmetry fairness.

THE SCHEDULER.
    bus map        240 links partition into the 40 lines (4-cliques); every edge on a unique line ->
                   40 four-way buses; the primitive is a line-local 4-way exchange.
    link schedule  collinearity graph is 1-factorable = 12 perfect matchings (computed) -> 12-slot
                   conflict-free point-to-point frame (each node drives 1 of its 12 ports/slot); minimal.
    readout        a spread (10 disjoint lines covering all 40 nodes) exists -> 10 contexts in parallel;
                   but the 40 contexts do NOT resolve into 4 spreads (proven by search) -> readout is
                   NOT fully parallelizable = measurement incompatibility / contextuality as a schedule.
    fairness       W(E6) transitive on nodes/links/contexts -> any schedule symmetrizes, hot-spot-free.
    frame          the beat-30 clock (Pass 35) provides the slot boundaries of the 12-slot frame.

Honest scope: the bus decomposition (40 lines, each edge unique), the 1-factorization into 12 perfect
matchings, the existence of a spread, and the NON-existence of a resolution into 4 spreads are all
computed here (the last by exhaustive backtracking). The reading -- bus = line, link slot = 1-factor,
readout slot = spread, non-resolvability = contextuality -- is the scheduling dictionary applied to the
geometry; the fairness argument uses the (standard) W(E6) transitivity. So: a quantified scheduler with
a computed contextuality obstruction.

Verifies the 40-line bus decomposition, the 12-perfect-matching 1-factorization, a spread, and the
non-resolvability of the 40 contexts into 4 spreads.
"""
from __future__ import annotations

import itertools
import json
import random

import networkx as nx
import numpy as np


def build_gq33():
    inv = {1: 1, 2: 2}

    def norm(v):
        for c in v:
            if c != 0:
                return tuple((x * inv[c]) % 3 for x in v)

    pts = sorted({norm(v) for v in itertools.product(range(3), repeat=4) if any(v)})

    def B(x, y):
        return (x[0] * y[1] - x[1] * y[0] + x[2] * y[3] - x[3] * y[2]) % 3

    return pts, norm, B


def main():
    out = {}
    pts, norm, B = build_gq33()
    n = len(pts)
    pidx = {p: i for i, p in enumerate(pts)}
    edges = [
        (i, j) for i in range(n) for j in range(i + 1, n) if B(pts[i], pts[j]) == 0
    ]
    k = 2 * len(edges) // n
    print(
        "== the scheduler: 40 four-way buses, a 12-slot link frame, readout NOT fully parallelizable =="
    )

    # (1) bus map: edges -> 40 lines (4-cliques), each edge unique
    def span(p, q):
        S = set()
        for a in range(3):
            for b in range(3):
                v = tuple((a * p[i] + b * q[i]) % 3 for i in range(4))
                if any(v):
                    S.add(norm(v))
        return frozenset(pidx[x] for x in S)

    lines = list({span(pts[i], pts[j]) for (i, j) in edges})
    lines = [tuple(sorted(L)) for L in lines]
    edge_cover = {}
    for L in lines:
        for a in range(4):
            for b in range(a + 1, 4):
                e = (L[a], L[b])
                edge_cover[e] = edge_cover.get(e, 0) + 1
    each_edge_unique = all(v == 1 for v in edge_cover.values())
    print(
        f"\n[bus map]  {len(edges)} links partition into {len(lines)} lines (4-cliques); each edge on a unique line: {each_edge_unique}"
    )
    assert len(lines) == 40 and each_edge_unique and len(edge_cover) == 240
    out["bus_map"] = {
        "links": len(edges),
        "buses": len(lines),
        "bus_size": 4,
        "each_edge_unique": each_edge_unique,
        "primitive": "line-local 4-way exchange",
    }

    # (2) link schedule: 1-factorization into 12 perfect matchings
    best = 0
    factors_found = None
    for _ in range(80):
        H = nx.Graph()
        H.add_nodes_from(range(n))
        for i, j in edges:
            H.add_edge(i, j, weight=random.random())
        factors = []
        for _ in range(k):
            m = nx.max_weight_matching(H, maxcardinality=True)
            if len(m) != n // 2:
                break
            factors.append(m)
            H.remove_edges_from(m)
        if len(factors) > best:
            best = len(factors)
            factors_found = factors
        if best == k:
            break
    print(
        f"\n[link schedule]  collinearity graph 1-factorable into {best} perfect matchings -> {best}-slot conflict-free frame"
    )
    print(
        f"  each node drives 1 of its {k} ports per slot; frame length = radix {k} (minimal); vertex/edge-transitive -> balanced"
    )
    assert best == 12
    # sanity: factors are disjoint perfect matchings covering all edges
    covered = set()
    for f in factors_found:
        for a, b in f:
            covered.add((min(a, b), max(a, b)))
    out["link_schedule"] = {
        "one_factorable": True,
        "perfect_matchings": best,
        "frame_slots": best,
        "edges_covered": len(covered),
        "reading": "12-slot conflict-free point-to-point frame; each node uses 1 of 12 ports/slot",
    }

    # (3) readout schedule: spread exists, but no resolution into 4 spreads
    lines_through = [[li for li, L in enumerate(lines) if p in L] for p in range(n)]

    # find one spread (10 disjoint lines covering all 40 points) by backtracking
    def find_spread():
        sol = []

        def bt(covered):
            if len(covered) == n:
                return True
            pt = next(p for p in range(n) if p not in covered)
            for li in lines_through[pt]:
                if set(lines[li]).isdisjoint(covered):
                    sol.append(li)
                    if bt(covered | set(lines[li])):
                        return True
                    sol.pop()
            return False

        return sol if bt(set()) else None

    spread = find_spread()
    spread_ok = spread is not None and sorted(
        p for li in spread for p in lines[li]
    ) == list(range(n))
    print(
        f"\n[readout schedule]  a spread of {len(spread)} disjoint lines covers all {n} nodes: {spread_ok} -> 10 contexts in parallel"
    )

    # resolution into 4 spreads: proper 4-coloring with each point's 4 lines rainbow
    def resolve_into_4_spreads():
        color = [-1] * len(lines)
        order = sorted(range(len(lines)), key=lambda li: -len(lines[li]))

        def ok(li, c):
            for p in lines[li]:
                for lj in lines_through[p]:
                    if lj != li and color[lj] == c:
                        return False
            return True

        def bt(idx):
            if idx == len(order):
                return True
            li = order[idx]
            for c in range(4):
                if ok(li, c):
                    color[li] = c
                    if bt(idx + 1):
                        return True
                    color[li] = -1
            return False

        return color if bt(0) else None

    resolution = resolve_into_4_spreads()
    print(
        f"  resolution of the 40 contexts into 4 parallel spreads: {'EXISTS' if resolution else 'DOES NOT EXIST'}"
    )
    print(
        f"  -> readout is NOT fully parallelizable = measurement incompatibility / contextuality as a schedule"
    )
    assert spread_ok and resolution is None
    out["readout_schedule"] = {
        "spread_size": len(spread),
        "spread_covers_all_nodes": spread_ok,
        "resolves_into_4_spreads": False,
        "interpretation": "readout NOT fully parallelizable: the contexts overlap as measurement incompatibility (contextuality) -- a hard scheduling obstruction",
    }

    # (4) fairness
    print(
        f"\n[fairness]  W(E6) transitive on nodes/links/contexts -> any schedule symmetrizes, hot-spot-free"
    )
    print(
        f"[frame]  the beat-30 clock (Pass 35) provides the slot boundaries of the 12-slot frame"
    )
    out["fairness"] = (
        "W(E6) vertex/edge/line-transitive -> schedules symmetrize to hot-spot-free"
    )
    out["frame"] = "beat-30 clock provides the slot boundaries; 12-slot link frame"

    print(
        "\nRESULT: the OS / resource-management layer is read off the geometry, contextuality included."
    )
    print(
        "  (1) Bus map: the 240 links partition exactly into the 40 lines, each a 4-clique (every edge"
    )
    print(
        "  on a unique line), so the wiring is 40 four-way buses and the communication primitive is a"
    )
    print(
        "  line-local 4-way exchange. (2) Link schedule: the collinearity graph is 1-factorable into"
    )
    print(
        "  12 perfect matchings (computed), so a conflict-free point-to-point schedule needs exactly"
    )
    print(
        "  12 slots, each node driving one of its 12 ports per slot -- the frame length is the radix"
    )
    print(
        "  12, minimal, and perfectly balanced by vertex/edge-transitivity. (3) Readout schedule and"
    )
    print(
        "  its obstruction: a spread of 10 disjoint lines covers all 40 nodes (so 10 contexts measure"
    )
    print(
        "  in parallel), but the 40 contexts do NOT resolve into 4 parallel spreads (proven by search)"
    )
    print(
        "  -- so the readout is not fully parallelizable, and that non-resolvability IS measurement"
    )
    print(
        "  incompatibility, the contextuality that fuels the magic, showing up as a hard scheduling"
    )
    print(
        "  constraint. Fairness is free: W(E6) acts transitively on nodes, links, and contexts, so"
    )
    print(
        "  any schedule symmetrizes to a hot-spot-free one. So the scheduler is 40 four-way buses, a"
    )
    print(
        "  12-slot conflict-free link frame, parallel readout up to a spread of 10 but provably not"
    )
    print(
        "  fully parallel, and symmetry-guaranteed fairness. Honest: the bus decomposition, the 12"
    )
    print(
        "  matchings, the spread, and the non-resolvability are all computed (the last by backtracking)."
    )

    out["summary"] = (
        "the scheduler: the wires partition into 40 four-way buses, the links run on a 12-slot "
        "conflict-free frame, and the readout contexts provably do NOT parallelize -- contextuality "
        "seen by the scheduler. (1) Bus map: the 240 links partition EXACTLY into the 40 lines of "
        "GQ(3,3), each a 4-clique (every edge on a unique line) -> 40 four-way buses; the primitive is a "
        "line-local 4-way exchange. (2) Link schedule: the collinearity graph is 1-FACTORABLE into 12 "
        "perfect matchings (computed) -> a 12-slot conflict-free point-to-point frame (each node drives "
        "1 of its 12 ports/slot), frame length = radix 12 (minimal), perfectly balanced by vertex/"
        "edge-transitivity. (3) Readout: a spread (10 disjoint lines covering all 40 nodes) exists -> 10 "
        "contexts in parallel, but the 40 contexts do NOT resolve into 4 spreads (proven by backtracking "
        "search) -> readout is NOT fully parallelizable = measurement incompatibility / contextuality as "
        "a hard scheduling obstruction. Fairness: W(E6) transitive on nodes/links/contexts -> schedules "
        "symmetrize, hot-spot-free; the beat-30 clock provides slot boundaries. So: 40 four-way buses, a "
        "12-slot link frame, parallel readout up to a spread of 10 but provably not fully parallel, and "
        "symmetry-guaranteed fairness. HONEST: the bus decomposition (40 lines, each edge unique), the "
        "1-factorization (12 perfect matchings), the spread, and the non-resolvability into 4 spreads "
        "are all computed here (the last by exhaustive backtracking); the scheduling reading (bus=line, "
        "link slot=1-factor, readout slot=spread, non-resolvability=contextuality) is the standard "
        "dictionary; the fairness uses W(E6) transitivity."
    )
    out["sources"] = [
        "GQ(3,3) line geometry (240 edges = 40 lines, each edge unique); 1-factorization / perfect "
        "matchings (computed via networkx max-cardinality matching); spreads and resolutions of "
        "generalized quadrangles; W(3,3) spread existence; W(E6) = Aut(GQ(3,3)) transitivity; "
        "edge-coloring = conflict-free link scheduling (standard NoC dictionary); beat-30 clock (Pass 35)."
    ]
    with open("data/w33_scheduler_os.json", "w") as fh:
        json.dump(out, fh, indent=2)
    print("\nwrote data/w33_scheduler_os.json")


if __name__ == "__main__":
    main()
