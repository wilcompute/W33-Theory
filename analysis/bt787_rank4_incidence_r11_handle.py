#!/usr/bin/env python3
"""
BT787 - Rank-4 incidence revision and the R11 handle octet.

BT784 gave a count-level rank-32/tomotope map.  BT786 sharpened the
face layer to R09 + R10.  This verifier recomputes the rank-32 suborbit
scheme without networkx/numpy, then checks the consequence:

    if faces = R09 + R10, the only remaining primitive size-8 packet is R11.

R11 is not another face sheet.  Its relation profile is off-base on both
lines ({one_side: 2}, overlap 2), while R09 and R10 each keep one base line
({equal: 1, one_side: 1}, overlap 5).  The quotient paths also separate the
live face-edge route from the shadow handle route.
"""
from __future__ import annotations

from collections import Counter, deque
from itertools import combinations
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def inv3(a: int) -> int:
    a %= 3
    if a in (1, 2):
        return a
    raise ZeroDivisionError


def canon(v):
    for x in v:
        if x % 3:
            c = inv3(x)
            return tuple((c * y) % 3 for y in v)
    raise ValueError


def points():
    return sorted({
        canon((a, b, c, d))
        for a in range(3) for b in range(3)
        for c in range(3) for d in range(3)
        if (a, b, c, d) != (0, 0, 0, 0)
    })


def symp(x, y) -> int:
    return (x[0] * y[2] - x[2] * y[0] + x[1] * y[3] - x[3] * y[1]) % 3


def compose(a, b):
    return tuple(a[b[i]] for i in range(len(a)))


def build_geometry():
    pts = points()
    pt_index = {p: i for i, p in enumerate(pts)}
    n = len(pts)
    adj = [[False] * n for _ in range(n)]
    for i, j in combinations(range(n), 2):
        if symp(pts[i], pts[j]) == 0:
            adj[i][j] = adj[j][i] = True

    lines = [
        frozenset(q)
        for q in combinations(range(n), 4)
        if all(adj[i][j] for i, j in combinations(q, 2))
    ]
    line_sets = [set(line) for line in lines]
    line_key_index = {tuple(sorted(line)): i for i, line in enumerate(lines)}
    skew = [
        (i, j)
        for i, j in combinations(range(40), 2)
        if not (line_sets[i] & line_sets[j])
    ]
    skew_index = {frozenset(pair): i for i, pair in enumerate(skew)}
    pair_to_skew = {}
    for i, (a, b) in enumerate(skew):
        pair_to_skew[(a, b)] = i
        pair_to_skew[(b, a)] = i

    assert len(pts) == 40
    assert len(lines) == 40
    assert len(skew) == 540
    return {
        "points": pts,
        "point_index": pt_index,
        "adj": adj,
        "lines": lines,
        "line_sets": line_sets,
        "line_key_index": line_key_index,
        "skew": skew,
        "skew_index": skew_index,
        "pair_to_skew": pair_to_skew,
    }


def transvection_perm(v, pts, pt_index):
    out = []
    for x in pts:
        w = symp(x, v)
        out.append(pt_index[canon(tuple((x[k] + w * v[k]) % 3 for k in range(4)))])
    return tuple(out)


def build_psp(pts, pt_index):
    seed_vectors = [
        canon((1, 0, 0, 0)), canon((0, 1, 0, 0)),
        canon((0, 0, 1, 0)), canon((0, 0, 0, 1)),
        canon((1, 1, 0, 0)), canon((1, 0, 1, 0)),
        canon((1, 0, 0, 1)), canon((0, 1, 1, 0)),
    ]
    gens = [transvection_perm(v, pts, pt_index) for v in seed_vectors]
    ident = tuple(range(len(pts)))
    group = {ident}
    frontier = [ident]
    while frontier:
        nxt = []
        for g in frontier:
            for h in gens:
                gh = compose(h, g)
                if gh not in group:
                    group.add(gh)
                    nxt.append(gh)
        frontier = nxt
    assert len(group) == 25920
    return list(group)


def line_perm(g, lines, line_key_index):
    return tuple(
        line_key_index[tuple(sorted(g[x] for x in line))]
        for line in lines
    )


def build_web(skew, skew_index, line_sets):
    web = [set() for _ in range(len(skew))]
    for i, j in skew:
        tv = [
            k for k in range(40)
            if k != i and k != j
            and line_sets[k] & line_sets[i]
            and line_sets[k] & line_sets[j]
        ]
        for a, b in combinations(tv, 2):
            if not (line_sets[a] & line_sets[b]):
                x = skew_index[frozenset((i, j))]
                y = skew_index[frozenset((a, b))]
                web[x].add(y)
                web[y].add(x)
    assert sum(len(nbs) for nbs in web) // 2 == 1620
    return web


def bfs_distances(web, base):
    dist = {base: 0}
    q = deque([base])
    while q:
        x = q.popleft()
        for y in web[x]:
            if y not in dist:
                dist[y] = dist[x] + 1
                q.append(y)
    return dist


def relation_to_base(t, base_a, base_b, line_sets):
    if t == base_a or t == base_b:
        return "equal"
    ma = bool(line_sets[t] & line_sets[base_a])
    mb = bool(line_sets[t] & line_sets[base_b])
    if ma and mb:
        return "transversal2"
    if ma or mb:
        return "one_side"
    return "zero_side"


def compute_rank32():
    geom = build_geometry()
    pts = geom["points"]
    psp = build_psp(pts, geom["point_index"])
    skew = geom["skew"]
    line_sets = geom["line_sets"]
    lines = geom["lines"]
    base = 0
    base_a, base_b = skew[base]
    web = build_web(skew, geom["skew_index"], line_sets)
    dist = bfs_distances(web, base)

    stabilizer_line_perms = []
    stabilizer_point_perms = []
    for g in psp:
        lp = line_perm(g, lines, geom["line_key_index"])
        if {lp[base_a], lp[base_b]} == {base_a, base_b}:
            stabilizer_line_perms.append(lp)
            stabilizer_point_perms.append(g)
    assert len(stabilizer_line_perms) == 48

    stab_skew_perms = []
    pair_to_skew = geom["pair_to_skew"]
    for lp in stabilizer_line_perms:
        stab_skew_perms.append(tuple(pair_to_skew[(lp[i], lp[j])] for i, j in skew))

    seen = set()
    orbits = []
    for s in range(len(skew)):
        if s in seen:
            continue
        q = deque([s])
        seen.add(s)
        orbit = []
        while q:
            x = q.popleft()
            orbit.append(x)
            for perm in stab_skew_perms:
                y = perm[x]
                if y not in seen:
                    seen.add(y)
                    q.append(y)
        orbits.append(sorted(orbit))

    orbits.sort(key=lambda o: (0 if base in o else 1, min(dist[x] for x in o), len(o), min(o)))
    orbit_id = {x: i for i, orbit in enumerate(orbits) for x in orbit}

    quotient = []
    rows = []
    base_union = line_sets[base_a] | line_sets[base_b]
    for oi, orbit in enumerate(orbits):
        rep = orbit[0]
        row = [0] * len(orbits)
        for nb in web[rep]:
            row[orbit_id[nb]] += 1
        quotient.append(row)
        ra, rb = skew[rep]
        rel_counter = Counter([
            relation_to_base(ra, base_a, base_b, line_sets),
            relation_to_base(rb, base_a, base_b, line_sets),
        ])
        target_union = line_sets[ra] | line_sets[rb]
        rows.append({
            "orbit": oi,
            "size": len(orbit),
            "representative_skew_pair": [int(ra), int(rb)],
            "web_distance_profile_from_base": {
                str(k): v for k, v in sorted(Counter(dist[x] for x in orbit).items())
            },
            "line_relation_multiset_to_base": dict(sorted(rel_counter.items())),
            "base_target_point_overlap": len(base_union & target_union),
            "web_neighbor_counts_to_orbits": {
                str(j): c for j, c in enumerate(row) if c
            },
        })

    assert len(orbits) == 32
    assert [len(o) for o in orbits] == [
        1, 6, 6, 24, 3, 24, 24, 24, 24, 8, 8, 8,
        12, 12, 12, 12, 12, 48, 48, 48, 4, 4,
        12, 12, 12, 12, 12, 12, 24, 24, 24, 24,
    ]
    return {
        "geometry": geom,
        "psp": psp,
        "stabilizer_point_perms": stabilizer_point_perms,
        "web": web,
        "orbits": orbits,
        "orbit_rows": rows,
        "quotient_matrix": quotient,
        "orbit_id": orbit_id,
    }


def quotient_path(quotient, start, stop):
    q = deque([(start, [start])])
    seen = {start}
    while q:
        x, path = q.popleft()
        if x == stop:
            return path
        for y, c in enumerate(quotient[x]):
            if c and y not in seen:
                seen.add(y)
                q.append((y, path + [y]))
    raise AssertionError(f"no quotient path from R{start:02d} to R{stop:02d}")


def main():
    rank32 = compute_rank32()
    rows = rank32["orbit_rows"]
    quotient = rank32["quotient_matrix"]
    sizes = [row["size"] for row in rows]

    size8_orbits = [row["orbit"] for row in rows if row["size"] == 8]
    face_orbits = [
        row["orbit"] for row in rows
        if row["size"] == 8
        and row["line_relation_multiset_to_base"] == {"equal": 1, "one_side": 1}
        and row["base_target_point_overlap"] == 5
    ]
    remaining_octets = [i for i in size8_orbits if i not in face_orbits]
    r11 = remaining_octets[0]

    size4_orbits = [row["orbit"] for row in rows if row["size"] == 4]
    primitive_edge_orbits = [row["orbit"] for row in rows if row["size"] == 12]
    live_edge_packet = 12
    shadow_edge_packet = 13

    paths = {
        "R11_to_R09_face_sheet": quotient_path(quotient, r11, 9),
        "R11_to_R10_face_sheet": quotient_path(quotient, r11, 10),
        "R11_to_live_edge_R12": quotient_path(quotient, r11, live_edge_packet),
        "R09_to_live_edge_R12": quotient_path(quotient, 9, live_edge_packet),
        "R10_to_live_edge_R12": quotient_path(quotient, 10, live_edge_packet),
    }

    checks = {
        "three_primitive_octets": size8_orbits == [9, 10, 11],
        "face_layer_is_R09_plus_R10": face_orbits == [9, 10],
        "R11_is_only_remaining_primitive_octet": remaining_octets == [11],
        "R11_has_handle_relation_profile": rows[11]["line_relation_multiset_to_base"] == {"one_side": 2},
        "R11_has_overlap_two": rows[11]["base_target_point_overlap"] == 2,
        "face_octets_have_overlap_five": all(rows[i]["base_target_point_overlap"] == 5 for i in face_orbits),
        "no_primitive_16_face_orbit": 16 not in sizes,
        "vertex_sheets_are_two_chiral_size4_packets": size4_orbits == [20, 21],
        "R11_reaches_live_edge_through_shadow_edge_route": paths["R11_to_live_edge_R12"] == [11, 13, 8, 12],
        "faces_reach_live_edge_through_R24_R26": paths["R09_to_live_edge_R12"] == [9, 24, 12] and paths["R10_to_live_edge_R12"] == [10, 26, 12],
    }
    for name, ok in checks.items():
        if not ok:
            raise AssertionError(f"BT787 check failed: {name}")

    out = {
        "theorem": "BT787 rank-4 incidence revision and R11 handle octet",
        "rank32_suborbit_sizes": sizes,
        "size8_orbits": size8_orbits,
        "rank4_revision": {
            "faces": {
                "orbits": face_orbits,
                "sizes": [sizes[i] for i in face_orbits],
                "count": sum(sizes[i] for i in face_orbits),
                "signature": "anchored phase sheets: {equal:1, one_side:1}, overlap 5",
            },
            "cell_or_handle_octet": {
                "orbits": remaining_octets,
                "sizes": [sizes[i] for i in remaining_octets],
                "count": sum(sizes[i] for i in remaining_octets),
                "signature": "off-base transfer: {one_side:2}, overlap 2",
            },
            "vertices": {
                "orbits": size4_orbits,
                "interpretation": "two chiral vertex sheets; choose one sheet for a 4-vertex local chart",
            },
            "edges": {
                "live_edge_packet": live_edge_packet,
                "shadow_edge_packet_for_R11": shadow_edge_packet,
                "all_primitive_size12_orbits": primitive_edge_orbits,
            },
        },
        "quotient_paths": paths,
        "rows_for_octets": {f"R{i:02d}": rows[i] for i in size8_orbits},
        "interpretation": {
            "BT784_status": "BT784's cell=R09 choice was count-level only; BT786/BT787 refines R09+R10 into faces.",
            "R11_status": "R11 is the forced primitive octet left after the face layer; it is best read as the handle/cell transfer packet.",
            "incidence_boundary": "This reconstructs the rank-4 packet assignment and connector routes, not a full geometric tomotope realization."
        },
        "checks": checks,
    }

    path = ROOT / "data" / "bt787_rank4_incidence_r11_handle.json"
    path.parent.mkdir(exist_ok=True)
    with path.open("w") as f:
        json.dump(out, f, indent=2)

    print("BT787 rank-4 incidence revision / R11 handle octet")
    print(json.dumps(out, indent=2))
    print(f"wrote {path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
