#!/usr/bin/env python3
from __future__ import annotations

import argparse, json
from collections import Counter, deque
from itertools import combinations, product
from pathlib import Path

MOD = 3
I4 = (1,0,0,0, 0,1,0,0, 0,0,1,0, 0,0,0,1)
BASE = [(0,0,0,2), (0,2,0,0), (0,0,2,2), (1,0,0,0)]
REF_SPHERE = (1,8,36,126,363,916,2052,4096,7396,12170,16916,7247,476,36,1)


def mm(a,b):
    return tuple(sum(a[4*i+k]*b[4*k+j] for k in range(4)) % MOD for i in range(4) for j in range(4))


def canon(v):
    vv = list(v)
    first = next(x for x in vv if x % MOD)
    if first == 2:
        vv = [(2*x) % MOD for x in vv]
    else:
        vv = [x % MOD for x in vv]
    return tuple(vv)


def vecs40():
    seen, out = set(), []
    for v in product(range(MOD), repeat=4):
        if v == (0,0,0,0):
            continue
        c = canon(v)
        if c not in seen:
            seen.add(c); out.append(c)
    return out


def tv(v):
    a,b,c,d = v
    jv = (c % MOD, d % MOD, (-a) % MOD, (-b) % MOD)
    outer = [(vi * wj) % MOD for vi in v for wj in jv]
    return tuple((I4[i] + outer[i]) % MOD for i in range(16))


def mv(m,v):
    return tuple(sum(m[4*i+j] * v[j] for j in range(4)) % MOD for i in range(4))


def group_from(gens):
    sym = []
    for g in gens:
        sym.append(g); sym.append(mm(g,g))
    seen, q = {I4}, deque([I4])
    while q:
        x = q.popleft()
        for g in sym:
            y = mm(x,g)
            if y not in seen:
                seen.add(y); q.append(y)
    return seen


def profile(gens):
    sym, seen_g = [], set()
    for g in gens:
        for h in (g, mm(g,g)):
            if h not in seen_g:
                seen_g.add(h); sym.append(h)
    dist, q = {I4:0}, deque([I4])
    while q:
        x = q.popleft(); nd = dist[x] + 1
        for g in sym:
            y = mm(x,g)
            if y not in dist:
                dist[y] = nd; q.append(y)
    hist = Counter(dist.values())
    return len(dist), max(hist), tuple(hist.get(i,0) for i in range(max(hist)+1))


def build():
    vecs = vecs40(); vi = {v:i for i,v in enumerate(vecs)}; mats = [tv(v) for v in vecs]
    full = group_from([tv(v) for v in BASE])
    perms, stab = [], []
    for g in full:
        p = tuple(vi[canon(mv(g,v))] for v in vecs)
        perms.append(p)
        if p[0] == 0:
            stab.append(p)
    unseen = set(combinations(range(1,40),3))
    reps = []
    while unseen:
        rep = next(iter(unseen))
        orb = {tuple(sorted((p[rep[0]], p[rep[1]], p[rep[2]]))) for p in stab}
        unseen -= orb
        reps.append((rep, len(orb)))
    fixed_counts = Counter()
    sample = {}
    for rep, osize in reps:
        inds = (0,) + rep
        key = profile([mats[i] for i in inds])
        fixed_counts[key] += osize
        sample.setdefault(key, inds)
    global_counts = {key: val * 10 for key, val in fixed_counts.items()}
    by_order_diam = Counter()
    by_order = Counter()
    for (order, diam, hist), count in global_counts.items():
        by_order_diam[f"{order}:diam{diam}"] += count
        by_order[str(order)] += count
    bt_key = (51840, 14, REF_SPHERE)
    return {
        "bt": 1242,
        "title": "Four-transvection word-metric regime classifier",
        "projective_transvections": 40,
        "all_four_sets": 91390,
        "fixed_point_representatives": 9139,
        "stabilizer_orbit_representatives": len(reps),
        "unique_word_metric_profiles": len(global_counts),
        "global_counts_by_order": dict(sorted(by_order.items(), key=lambda kv: int(kv[0]))),
        "global_counts_by_order_and_diameter": dict(sorted(by_order_diam.items())),
        "full_order_sets": by_order["51840"],
        "bt1228_profile_global_count": global_counts.get(bt_key, 0),
        "bt1228_profile_fraction_all_four_sets": global_counts.get(bt_key,0) / 91390,
        "bt1228_profile_fraction_full_order_sets": global_counts.get(bt_key,0) / by_order["51840"],
        "interpretation": "Among all four-projective-transvection sets, 61560 generate the full group. Full-order sets split into diameter 10, 12, and 14 word-metric regimes; the BT1228 diameter-14 fingerprint occurs in 12960 sets, so closure order alone is not a sufficient recovery invariant."
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=Path("data/bt1242_four_transvection_regime_classifier_summary.json"))
    ns = ap.parse_args()
    result = build()
    ns.out.parent.mkdir(parents=True, exist_ok=True)
    ns.out.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"bt":1242, "profiles":result["unique_word_metric_profiles"], "full_order_sets":result["full_order_sets"], "out":str(ns.out)}, indent=2))


if __name__ == "__main__":
    main()
