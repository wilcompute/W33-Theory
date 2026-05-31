#!/usr/bin/env python3
"""Ordered spread-transport orbit test.

The exact identity

    51840 = 40 * 36^2 = |Sp(4,3)|

suggests, but does not prove, that ordered triples

    (anchor, source spread, target spread)

form a single regular transport torsor.  This verifier tests the projective
version under PSp(4,3).

Result expected from the projective incidence action:
    PSp(4,3) has order 25920 and the 51840 ordered triples split into multiple
    orbit types.  Therefore 40*36^2 is a linear symplectic / Weyl lift count,
    not a single regular projective orbit unless extra sign/orientation data is
    added.
"""
from __future__ import annotations

import itertools
import json
from collections import Counter, deque
from pathlib import Path

q = 3


def inv3(x: int) -> int:
    x %= q
    if x == 1:
        return 1
    if x == 2:
        return 2
    raise ValueError("zero")


def normalize(v: tuple[int, ...]) -> tuple[int, ...]:
    v = tuple(x % q for x in v)
    i = next(i for i, x in enumerate(v) if x)
    inv = inv3(v[i])
    return tuple((inv * x) % q for x in v)


def symp(a: tuple[int, ...], b: tuple[int, ...]) -> int:
    return (a[0] * b[2] + a[1] * b[3] - a[2] * b[0] - a[3] * b[1]) % q


def points() -> list[tuple[int, ...]]:
    return sorted({normalize(v) for v in itertools.product(range(q), repeat=4) if any(v)})


def span_line(a: tuple[int, ...], b: tuple[int, ...]) -> tuple[tuple[int, ...], ...]:
    out = set()
    for x, y in itertools.product(range(q), repeat=2):
        v = tuple((x * a[i] + y * b[i]) % q for i in range(4))
        if any(v):
            out.add(normalize(v))
    return tuple(sorted(out))


def isotropic_lines(pts: list[tuple[int, ...]]) -> list[tuple[int, ...]]:
    pidx = {p: i for i, p in enumerate(pts)}
    raw = sorted({span_line(a, b) for a, b in itertools.combinations(pts, 2)})
    iso = [L for L in raw if all(symp(a, b) == 0 for a, b in itertools.combinations(L, 2))]
    return [tuple(sorted(pidx[p] for p in L)) for L in iso]


def spreads(lines: list[tuple[int, ...]], n_points: int = 40) -> list[tuple[int, ...]]:
    point_to_lines = {p: [] for p in range(n_points)}
    for i, line in enumerate(lines):
        for p in line:
            point_to_lines[p].append(i)
    out: list[tuple[int, ...]] = []

    def backtrack(remaining: set[int], chosen: list[int]) -> None:
        if not remaining:
            out.append(tuple(sorted(chosen)))
            return
        p = min(remaining, key=lambda x: sum(set(lines[i]).issubset(remaining) for i in point_to_lines[x]))
        for i in point_to_lines[p]:
            L = set(lines[i])
            if L.issubset(remaining):
                backtrack(remaining - L, chosen + [i])

    backtrack(set(range(n_points)), [])
    return sorted(set(out))


def transvection_perm(pts: list[tuple[int, ...]], v: tuple[int, ...]) -> tuple[int, ...]:
    pidx = {p: i for i, p in enumerate(pts)}
    image = []
    for x in pts:
        y = tuple((x[i] + symp(x, v) * v[i]) % q for i in range(4))
        image.append(pidx[normalize(y)])
    return tuple(image)


def compose(p: tuple[int, ...], g: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(p[g[i]] for i in range(len(g)))


def generate_psp(pts: list[tuple[int, ...]]) -> tuple[set[tuple[int, ...]], list[tuple[int, ...]]]:
    gens = list({transvection_perm(pts, v) for v in pts})
    ident = tuple(range(len(pts)))
    group = {ident}
    queue = deque([ident])
    while queue:
        g = queue.popleft()
        for s in gens:
            h = compose(s, g)
            if h not in group:
                group.add(h)
                queue.append(h)
    return group, gens


def build_payload() -> dict:
    pts = points()
    lines = isotropic_lines(pts)
    line_index = {L: i for i, L in enumerate(lines)}
    sps = spreads(lines)
    spread_index = {s: i for i, s in enumerate(sps)}
    psp, gens = generate_psp(pts)

    def apply_line(g: tuple[int, ...], li: int) -> int:
        return line_index[tuple(sorted(g[p] for p in lines[li]))]

    def apply_spread(g: tuple[int, ...], si: int) -> int:
        return spread_index[tuple(sorted(apply_line(g, li) for li in sps[si]))]

    def act(g: tuple[int, ...], triple: tuple[int, int, int]) -> tuple[int, int, int]:
        a, src, dst = triple
        return (g[a], apply_spread(g, src), apply_spread(g, dst))

    def anchor_line(anchor: int, si: int) -> int:
        hits = [li for li in sps[si] if anchor in lines[li]]
        assert len(hits) == 1
        return hits[0]

    def orbit(start: tuple[int, int, int]) -> set[tuple[int, int, int]]:
        seen = {start}
        queue = deque([start])
        while queue:
            x = queue.popleft()
            for g in gens:
                y = act(g, x)
                if y not in seen:
                    seen.add(y)
                    queue.append(y)
        return seen

    all_triples = {(a, s, t) for a in range(40) for s in range(36) for t in range(36)}
    remaining = set(all_triples)
    orbit_records = []
    while remaining:
        start = next(iter(remaining))
        orb = orbit(start)
        inv = Counter()
        for a, s, t in orb:
            same_sector = anchor_line(a, s) == anchor_line(a, t)
            spread_overlap = len(set(sps[s]) & set(sps[t]))
            inv[(same_sector, spread_overlap)] += 1
        orbit_records.append({"representative": start, "size": len(orb), "invariants": {str(k): v for k, v in inv.items()}})
        remaining -= orb

    orbit_size_distribution = Counter(r["size"] for r in orbit_records)
    identities = {
        "points_lines_spreads": len(pts) == 40 and len(lines) == 40 and len(sps) == 36,
        "projective_group_order": len(psp) == 25920,
        "triple_count": len(all_triples) == 40 * 36 * 36 == 51840,
        "sp_order_double_psp": 2 * len(psp) == 51840,
        "orbit_partition_complete": sum(r["size"] for r in orbit_records) == len(all_triples),
        "not_single_projective_regular_orbit": len(orbit_records) != 1,
    }
    return {
        "theorem": "ordered_spread_transport_orbits",
        "counts": {"points": len(pts), "lines": len(lines), "spreads": len(sps), "triples": len(all_triples), "PSp43": len(psp), "Sp43_lift": 2 * len(psp)},
        "orbit_structure_under_PSp43": {"orbit_count": len(orbit_records), "orbit_size_distribution": dict(orbit_size_distribution), "orbits": orbit_records},
        "interpretation": "40*36^2 equals |Sp(4,3)|, but the projective PSp(4,3) action splits ordered anchor/source/target spread triples into several orbit types. The equality is a linear symplectic/Weyl lift count, not a single regular projective transport orbit without extra orientation/sign data.",
        "identities": identities,
        "all_identities_hold": all(identities.values()),
    }


def main() -> None:
    payload = build_payload()
    out = Path("data/w33_ordered_spread_transport_orbits.json")
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
