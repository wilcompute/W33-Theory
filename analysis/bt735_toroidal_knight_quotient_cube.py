#!/usr/bin/env python3
"""BT735 -- Toroidal Knight Quotient Cube Theorem.

This verifier continues the CCCCXIII toroidal-knight / Q4 packet result.
CCCCXIII proved that the 4x4 toroidal knight graph is Q4 and that the
chosen knight tour is a Gray-code Hamilton cycle.  BT735 pushes that clock
through the antipodal axis quotient

    Q4 -> Q4/{+-} ~= K_{4,4}.

The surprise is that the projected Gray clock does not fill all 16 quotient
edges.  Its unique quotient-edge support has exactly 12 edges and the four
missing quotient edges form a perfect matching.  Therefore the projected
support is

    K_{4,4} minus a perfect matching ~= Q3.

This is the first exact bridge from the 4-bit codec clock to a 3-cube
lambda-cube-style quotient: Q4 carries the full codec state, while its
antipodal Gray trace selects a Q3 support plus one missing duality/hinge
matching.
"""
from __future__ import annotations

from collections import Counter, deque
import itertools
import json
from pathlib import Path
from typing import Dict, Iterable, List, Sequence, Set, Tuple

ROOT = Path(__file__).resolve().parents[1]
Bit4 = Tuple[int, int, int, int]
Bit3 = Tuple[int, int, int]
Edge3 = Tuple[Bit3, Bit3]

# Same explicit map and tour used by CCCCXIII.  Keeping this verifier
# self-contained makes BT735 an independent certificate of the quotient layer.
KNIGHT_TO_Q4: Dict[Tuple[int, int], Bit4] = {
    (0, 0): (0, 0, 0, 0), (2, 3): (0, 0, 0, 1),
    (3, 2): (0, 0, 1, 0), (1, 1): (0, 0, 1, 1),
    (1, 2): (0, 1, 0, 0), (3, 1): (0, 1, 0, 1),
    (2, 0): (0, 1, 1, 0), (0, 3): (0, 1, 1, 1),
    (2, 1): (1, 0, 0, 0), (0, 2): (1, 0, 0, 1),
    (1, 3): (1, 0, 1, 0), (3, 0): (1, 0, 1, 1),
    (3, 3): (1, 1, 0, 0), (1, 0): (1, 1, 0, 1),
    (0, 1): (1, 1, 1, 0), (2, 2): (1, 1, 1, 1),
}

KNIGHT_TOUR: List[Tuple[int, int]] = [
    (0, 0), (1, 2), (2, 0), (3, 2),
    (1, 1), (0, 3), (3, 1), (2, 3),
    (0, 2), (1, 0), (2, 2), (3, 0),
    (1, 3), (0, 1), (3, 3), (2, 1),
]

# In the Fano-labeled quotient used in the codec-chain files, an antipodal
# axis is labelled by p in F_2^3 via axis(p)={(0,p),(1,1-p)}.
GENS: Tuple[Bit3, ...] = ((1, 0, 0), (0, 1, 0), (0, 0, 1), (1, 1, 1))


def bitstr(v: Sequence[int]) -> str:
    return "".join(str(x) for x in v)


def f2_add(a: Sequence[int], b: Sequence[int]) -> Tuple[int, ...]:
    return tuple((x ^ y) for x, y in zip(a, b))


def axis_label(q4: Bit4) -> Bit3:
    """Return p for the antipodal axis {(0,p),(1,1-p)}."""
    first, rest = q4[0], q4[1:]
    if first == 0:
        return rest  # type: ignore[return-value]
    return tuple(1 - x for x in rest)  # type: ignore[return-value]


def parity(p: Bit3) -> int:
    return sum(p) % 2


def sorted_edge(a: Bit3, b: Bit3) -> Edge3:
    return tuple(sorted((a, b)))  # type: ignore[return-value]


def q4_tour() -> List[Bit4]:
    return [KNIGHT_TO_Q4[v] for v in KNIGHT_TOUR]


def axis_sequence() -> List[Bit3]:
    return [axis_label(x) for x in q4_tour()]


def quotient_vertices() -> List[Bit3]:
    return list(itertools.product((0, 1), repeat=3))  # type: ignore[return-value]


def quotient_k44_edges() -> Set[Edge3]:
    even = [p for p in quotient_vertices() if parity(p) == 0]
    edges: Set[Edge3] = set()
    for p in even:
        for g in GENS:
            edges.add(sorted_edge(p, f2_add(p, g)))  # type: ignore[arg-type]
    return edges


def quotient_edges_by_generator() -> Dict[Bit3, Set[Edge3]]:
    even = [p for p in quotient_vertices() if parity(p) == 0]
    return {
        g: {sorted_edge(p, f2_add(p, g)) for p in even}  # type: ignore[arg-type]
        for g in GENS
    }


def projected_walk_edges() -> List[Edge3]:
    seq = axis_sequence()
    return [sorted_edge(seq[i], seq[(i + 1) % len(seq)]) for i in range(len(seq))]


def projected_generators() -> List[Bit3]:
    seq = axis_sequence()
    return [f2_add(seq[i], seq[(i + 1) % len(seq)]) for i in range(len(seq))]  # type: ignore[list-item]


def graph_adjacency(edges: Iterable[Edge3]) -> Dict[Bit3, Set[Bit3]]:
    adj = {v: set() for v in quotient_vertices()}
    for a, b in edges:
        adj[a].add(b)
        adj[b].add(a)
    return adj


def degree_profile(edges: Iterable[Edge3]) -> Dict[str, int]:
    deg = Counter()
    for a, b in edges:
        deg[a] += 1
        deg[b] += 1
    return {bitstr(k): deg[k] for k in sorted(deg)}


def distance_profile(adj: Dict[Bit3, Set[Bit3]], start: Bit3) -> List[int]:
    seen = {start: 0}
    q: deque[Bit3] = deque([start])
    while q:
        u = q.popleft()
        for w in adj[u]:
            if w not in seen:
                seen[w] = seen[u] + 1
                q.append(w)
    if len(seen) != len(adj):
        return []
    return [sum(1 for d in seen.values() if d == i) for i in range(max(seen.values()) + 1)]


def is_q3_support(edges: Set[Edge3]) -> bool:
    adj = graph_adjacency(edges)
    return (
        len(edges) == 12
        and sorted(len(adj[v]) for v in adj) == [3] * 8
        and all(distance_profile(adj, v) == [1, 3, 3, 1] for v in adj)
    )


def missing_edges() -> Set[Edge3]:
    return quotient_k44_edges() - set(projected_walk_edges())


def build_results() -> dict:
    seq = axis_sequence()
    support = set(projected_walk_edges())
    full = quotient_k44_edges()
    missing = missing_edges()
    by_g = quotient_edges_by_generator()
    gen_counts = Counter(projected_generators())

    checks = [
        ("Q4 tour has 16 distinct states", len(set(q4_tour())) == 16),
        ("axis quotient has 8 distinct axes", len(set(seq)) == 8),
        ("first half visits all 8 axes", len(set(seq[:8])) == 8),
        ("second half visits all 8 axes", len(set(seq[8:])) == 8),
        ("quotient graph is K4,4", len(full) == 16),
        ("all projected steps use K4,4 generators", set(projected_generators()) <= set(GENS)),
        ("projected support has 12 unique edges", len(support) == 12),
        ("missing quotient edges have count 4", len(missing) == 4),
        ("missing edges form perfect matching", set(degree_profile(missing).values()) == {1} and len(degree_profile(missing)) == 8),
        ("support is Q3", is_q3_support(support)),
    ]

    return {
        "part": "BT735",
        "title": "Toroidal Knight Quotient Cube Theorem",
        "verified": all(ok for _, ok in checks),
        "checks_passed": sum(1 for _, ok in checks if ok),
        "checks_total": len(checks),
        "checks": [{"name": name, "passed": ok} for name, ok in checks],
        "q4_tour_bits": [bitstr(x) for x in q4_tour()],
        "axis_sequence": [bitstr(x) for x in seq],
        "axis_unique_count": len(set(seq)),
        "first_half_axes": [bitstr(x) for x in seq[:8]],
        "second_half_axes": [bitstr(x) for x in seq[8:]],
        "axis_generators": [bitstr(g) for g in projected_generators()],
        "generator_step_counts": {bitstr(g): gen_counts[g] for g in GENS},
        "generator_unique_support_counts": {bitstr(g): len(support & by_g[g]) for g in GENS},
        "quotient_graph": {"vertices": 8, "edges": len(full), "is_k44": len(full) == 16},
        "trace_support": {
            "unique_edges": len(support),
            "edges": [[bitstr(a), bitstr(b)] for a, b in sorted(support)],
            "is_q3": is_q3_support(support),
            "distance_profiles": {bitstr(v): distance_profile(graph_adjacency(support), v) for v in sorted(quotient_vertices())},
        },
        "missing_matching": {
            "count": len(missing),
            "edges": [[bitstr(a), bitstr(b)] for a, b in sorted(missing)],
            "is_perfect_matching": set(degree_profile(missing).values()) == {1} and len(degree_profile(missing)) == 8,
            "by_generator": {bitstr(g): [[bitstr(a), bitstr(b)] for a, b in sorted(by_g[g] - support)] for g in GENS},
        },
        "theorem": (
            "The CCCCXIII 16-step toroidal knight Gray cycle on Q4 descends under the "
            "antipodal axis quotient to an 8-axis K4,4 walk whose unique quotient-edge "
            "support is K4,4 minus a perfect matching, hence a Q3 cube with 8 vertices "
            "and 12 edges."
        ),
        "bridge": (
            "Q4 codec clock -> antipodal K4,4 axis quotient -> Q3 lambda-cube support "
            "+ one missing perfect matching. The missing matching records the duality/hinge "
            "closure not contained in the projected Gray trace."
        ),
        "honesty_boundary": (
            "This proves the graph/clock/quotient support theorem. It does not claim the "
            "projected Q3 alone is the full Levi H1 selector; the rank-81 selector still "
            "requires the BT714/BT724 hinge sheets."
        ),
    }


def main() -> None:
    results = build_results()
    out = ROOT / "data" / "PART_BT735_TOROIDAL_KNIGHT_QUOTIENT_CUBE_summary.json"
    out.write_text(json.dumps(results, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "part": results["part"],
        "verified": results["verified"],
        "checks_passed": results["checks_passed"],
        "checks_total": results["checks_total"],
        "out_path": str(out),
    }, indent=2))


if __name__ == "__main__":
    main()
