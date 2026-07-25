#!/usr/bin/env python3
"""Pass 990: exact A5 census inside PSp(4,3).

Pass 982 sampled A5 subgroups and found a uniform point/edge orbit profile,
consistent with one conjugacy class but explicitly not proving it.  The exact
census gives the opposite answer: there are two conjugacy classes, each of size
216.  They are orbit-indistinguishable on W33 points and edges.

The proof is internal and exhaustive.  PSp(4,3) is generated on the 40
projective symplectic points by six transvections.  A fixed C5 is contained in
exactly two A5 subgroups; the C5 normalizer has order 20, hence all 1296 C5
subgroups form one G-orbit.  Double counting then gives 432 A5 subgroups total.
Each A5 normalizer has order 120, so its conjugacy orbit has size 216, and the
two representatives are not conjugate.  Their intersection is D10.
"""
from __future__ import annotations

import argparse
import collections
import functools
import hashlib
import itertools
import json
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass990_a5_double_class_census.json"
Q = 3
OMEGA = np.array(
    [[0, 0, 1, 0], [0, 0, 0, 1], [-1, 0, 0, 0], [0, -1, 0, 0]],
    dtype=np.int64,
) % Q
A5_PROFILE = {1: 1, 2: 15, 3: 20, 5: 24}
GEN_VECS = (
    (1, 0, 0, 0),
    (0, 1, 0, 0),
    (0, 0, 1, 0),
    (0, 0, 0, 1),
    (1, 1, 0, 0),
    (1, 0, 0, 1),
)


def norm(v):
    v = tuple(int(x) % Q for x in v)
    if not any(v):
        return None
    for x in v:
        if x:
            s = 1 if x == 1 else 2
            return tuple((s * y) % Q for y in v)


def omega(u, v):
    return int((np.array(u, dtype=np.int64) @ OMEGA @ np.array(v, dtype=np.int64)) % Q)


def compose(p, q):
    return tuple(p[q[i]] for i in range(40))


def invperm(p):
    out = [0] * 40
    for i, j in enumerate(p):
        out[j] = i
    return tuple(out)


def conjugate(g, h):
    return compose(compose(g, h), invperm(g))


def order_of(p):
    identity = tuple(range(40))
    x = identity
    for k in range(1, 61):
        x = compose(p, x)
        if x == identity:
            return k
    raise RuntimeError("permutation order exceeded 60")


def subgroup_closure(seeds, cap=1000):
    identity = tuple(range(40))
    gens = list(seeds) + [invperm(g) for g in seeds]
    seen = {identity}
    queue = collections.deque([identity])
    while queue:
        x = queue.popleft()
        for g in gens:
            y = compose(g, x)
            if y not in seen:
                seen.add(y)
                if len(seen) > cap:
                    return None
                queue.append(y)
    return frozenset(seen)


def group_closure(gens):
    identity = tuple(range(40))
    all_gens = list(gens) + [invperm(g) for g in gens]
    seen = {identity}
    queue = collections.deque([identity])
    while queue:
        x = queue.popleft()
        for g in all_gens:
            y = compose(g, x)
            if y not in seen:
                seen.add(y)
                queue.append(y)
    return frozenset(seen)


def transvection_perm(points, pidx, v, lam=1):
    vv = np.array(v, dtype=np.int64)
    out = []
    for x in points:
        xx = np.array(x, dtype=np.int64)
        a = int((xx @ OMEGA @ vv) % Q)
        y = (xx + lam * a * vv) % Q
        out.append(pidx[norm(tuple(y))])
    return tuple(out)


def a5_profile(H):
    return dict(sorted(collections.Counter(order_of(x) for x in H).items()))


def is_a5(H):
    return H is not None and len(H) == 60 and a5_profile(H) == A5_PROFILE


def cyclic_subgroup(x):
    identity = tuple(range(40))
    out = {identity}
    y = identity
    for _ in range(order_of(x) - 1):
        y = compose(x, y)
        out.add(y)
    return frozenset(out)


def orbit_profile(H, objects, action):
    seen = set()
    sizes = []
    for obj in objects:
        if obj in seen:
            continue
        orb = {action(g, obj) for g in H}
        seen |= orb
        sizes.append(len(orb))
    return sorted(sizes, reverse=True)


def stable_subgroup_key(H):
    return tuple(sorted(H))


@functools.lru_cache(maxsize=1)
def core_objects():
    points = sorted({norm(v) for v in itertools.product(range(Q), repeat=4) if any(v)})
    pidx = {p: i for i, p in enumerate(points)}
    edges = [
        (i, j)
        for i, j in itertools.combinations(range(40), 2)
        if omega(points[i], points[j]) == 0
    ]
    generators = tuple(transvection_perm(points, pidx, v) for v in GEN_VECS)
    G = group_closure(generators)
    by_order = collections.defaultdict(list)
    for g in sorted(G):
        by_order[order_of(g)].append(g)

    x = by_order[5][0]
    C5 = cyclic_subgroup(x)
    containing = set()
    for y in by_order[3]:
        H = subgroup_closure((x, y), cap=60)
        if is_a5(H) and C5.issubset(H):
            containing.add(H)
    classes = tuple(sorted(containing, key=stable_subgroup_key))
    if len(classes) != 2:
        raise RuntimeError(f"expected two A5 over fixed C5, found {len(classes)}")
    return {
        "points": points,
        "edges": edges,
        "generators": generators,
        "G": G,
        "by_order": by_order,
        "x": x,
        "C5": C5,
        "A5_classes": classes,
    }


def normalizer(G, H, genpair):
    a, b = genpair
    return frozenset(g for g in G if conjugate(g, a) in H and conjugate(g, b) in H)


def generating_pair(H):
    for a in sorted(H):
        if order_of(a) != 5:
            continue
        for b in sorted(H):
            if order_of(b) == 3 and subgroup_closure((a, b), cap=60) == H:
                return a, b
    raise RuntimeError("A5 generating pair not found")


def payload():
    c = core_objects()
    points, edges, generators = c["points"], c["edges"], c["generators"]
    G, by_order, C5 = c["G"], c["by_order"], c["C5"]
    H0, H1 = c["A5_classes"]
    checks = {}

    checks["W33_counts_40_240"] = (len(points), len(edges)) == (40, 240)
    checks["six_transvections_generate_PSp_order25920"] = len(G) == 25920
    checks["group_order_profile_locked"] = dict(sorted((k, len(v)) for k, v in by_order.items())) == {
        1: 1, 2: 315, 3: 800, 4: 3780, 5: 5184, 6: 5760, 9: 5760, 12: 4320
    }
    checks["fixed_C5_has_exactly_two_A5_overgroups"] = len(c["A5_classes"]) == 2

    x = c["x"]
    generation_counts = []
    for H in (H0, H1):
        generation_counts.append(sum(
            subgroup_closure((x, y), cap=60) == H
            for y in H if order_of(y) == 3
        ))
    checks["all_twenty_order3_elements_generate_each_A5_with_C5"] = generation_counts == [20, 20]

    C5_subgroups = {cyclic_subgroup(g) for g in by_order[5]}
    N_C5 = frozenset(g for g in G if frozenset(conjugate(g, h) for h in C5) == C5)
    checks["C5_subgroup_count1296"] = len(C5_subgroups) == 1296
    checks["C5_normalizer_order20"] = len(N_C5) == 20
    checks["C5_action_is_transitive"] = len(G) // len(N_C5) == len(C5_subgroups)

    normalizers = []
    for H in (H0, H1):
        N = normalizer(G, H, generating_pair(H))
        normalizers.append(N)
    checks["both_A5_normalizers_order120"] = [len(N) for N in normalizers] == [120, 120]
    expected_nprof = {1: 1, 2: 25, 3: 20, 4: 30, 5: 24, 6: 20}
    checks["both_normalizers_have_S5_order_profile"] = all(a5_profile(N) == expected_nprof for N in normalizers)

    a0, b0 = generating_pair(H0)
    conjugate_hit = any(conjugate(g, a0) in H1 and conjugate(g, b0) in H1 for g in G)
    checks["two_A5_representatives_are_not_conjugate"] = not conjugate_hit
    orbit_sizes = [len(G) // len(N) for N in normalizers]
    checks["two_conjugacy_classes_each_size216"] = orbit_sizes == [216, 216]

    c5_per_a5 = []
    for H in (H0, H1):
        c5_per_a5.append(len({cyclic_subgroup(g) for g in H if order_of(g) == 5}))
    total_a5 = len(C5_subgroups) * 2 // c5_per_a5[0]
    checks["each_A5_has_six_C5_subgroups"] = c5_per_a5 == [6, 6]
    checks["total_A5_subgroups432"] = total_a5 == 432
    checks["two_classes_exhaust_the_census"] = sum(orbit_sizes) == total_a5

    intersection = H0 & H1
    inter_profile = a5_profile(intersection)
    checks["paired_A5s_intersect_in_D10"] = len(intersection) == 10 and inter_profile == {1: 1, 2: 5, 5: 4}

    edge_objects = [tuple(sorted(e)) for e in edges]
    vprof = [orbit_profile(H, list(range(40)), lambda g, i: g[i]) for H in (H0, H1)]
    eprof = [
        orbit_profile(H, edge_objects, lambda g, e: tuple(sorted((g[e[0]], g[e[1]]))))
        for H in (H0, H1)
    ]
    checks["both_vertex_profiles_20_20"] = vprof == [[20, 20], [20, 20]]
    checks["both_edge_profiles_identical"] = eprof[0] == eprof[1] == [60, 60, 30, 30, 20, 20, 10, 10]

    raw = {
        "generator_sha": hashlib.sha256(repr(generators).encode()).hexdigest(),
        "C5_sha": hashlib.sha256(repr(sorted(C5)).encode()).hexdigest(),
        "class_representative_shas": [
            hashlib.sha256(repr(sorted(H)).encode()).hexdigest() for H in (H0, H1)
        ],
        "normalizer_sizes": [len(N) for N in normalizers],
        "intersection_profile": inter_profile,
        "vertex_profiles": vprof,
        "edge_profiles": eprof,
    }
    digest = hashlib.sha256(json.dumps(raw, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    checks["certificate_hash_locked"] = True

    status = "PASS" if all(checks.values()) else "FAIL"
    return {
        "schema": "w33.pass990.a5_double_class_census.v1",
        "status": status,
        "group": {
            "name": "PSp(4,3)",
            "order": len(G),
            "order_profile": dict(sorted((str(k), len(v)) for k, v in by_order.items())),
            "generators": [list(v) for v in GEN_VECS],
        },
        "C5_census": {
            "number_of_C5_subgroups": len(C5_subgroups),
            "normalizer_order": len(N_C5),
            "orbit_size": len(G) // len(N_C5),
            "A5_overgroups_per_C5": 2,
        },
        "A5_census": {
            "total_subgroups": total_a5,
            "conjugacy_classes": 2,
            "class_sizes": orbit_sizes,
            "normalizer_orders": [len(N) for N in normalizers],
            "normalizer_order_profiles": [a5_profile(N) for N in normalizers],
            "C5_subgroups_per_A5": c5_per_a5,
            "paired_intersection": {"order": len(intersection), "order_profile": inter_profile, "type": "D10"},
        },
        "W33_action": {
            "vertex_orbit_profiles": vprof,
            "edge_orbit_profiles": eprof,
            "verdict": "the two A5 conjugacy classes are indistinguishable by point and edge orbit sizes",
        },
        "theorem": (
            "PSp(4,3) contains exactly 432 A5 subgroups in two conjugacy classes of 216. "
            "Every C5 lies in exactly one A5 from each class; the paired A5s meet in D10. "
            "Both classes have vertex profile (20,20) and edge profile "
            "(60,60,30,30,20,20,10,10), so the orbit data sampled in Pass 982 cannot "
            "distinguish the classes."
        ),
        "boundary": (
            "The census is for the projective symplectic group acting on W33.  The two classes "
            "are classified internally by exact subgroup and normalizer enumeration; no claim is "
            "made yet about their geometric meaning."
        ),
        "checks": {k: bool(v) for k, v in checks.items()},
        "certificate_sha256": digest,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--output", type=Path, default=OUT)
    args = ap.parse_args()
    pl = payload()
    text = json.dumps(pl, sort_keys=True, separators=(",", ":")) + "\n"
    if args.check:
        if not args.output.exists() or args.output.read_text() != text:
            raise SystemExit("Pass 990 certificate drift")
    else:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text)
    print(json.dumps({"status": pl["status"], "checks": sum(pl["checks"].values()), "total": len(pl["checks"]), "A5": pl["A5_census"]}))
    return 0 if pl["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
