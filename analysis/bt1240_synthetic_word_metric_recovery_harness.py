#!/usr/bin/env python3
from __future__ import annotations

import argparse, json, math
from collections import Counter, deque
from pathlib import Path

MOD = 3
I4 = (1,0,0,0, 0,1,0,0, 0,0,1,0, 0,0,0,1)
BASE = [(0,0,0,2), (0,2,0,0), (0,0,2,2), (1,0,0,0)]
ALT = (1,1,1,1)
TOTAL = 51840
DIAM = 14
REF_SPHERE = [1,8,36,126,363,916,2052,4096,7396,12170,16916,7247,476,36,1]
REF_BALLS = {"B4": 534, "B8": 14994, "B12": 51803, "B14": 51840}


def mm(a, b):
    return tuple(sum(a[4*i+k] * b[4*k+j] for k in range(4)) % MOD for i in range(4) for j in range(4))


def tv(v):
    a,b,c,d = v
    jv = (c % MOD, d % MOD, (-a) % MOD, (-b) % MOD)
    outer = [(vi * wj) % MOD for vi in v for wj in jv]
    return tuple((I4[i] + outer[i]) % MOD for i in range(16))


def morder(g, limit=128):
    x = I4
    for n in range(1, limit + 1):
        x = mm(x, g)
        if x == I4:
            return n
    return None


def sym_gates(items):
    out = []
    for item in items:
        g = tv(item) if isinstance(item, tuple) and len(item) == 4 else item
        out.append(g)
        out.append(mm(g, g))
    uniq = []
    seen = set()
    for g in out:
        if g not in seen:
            seen.add(g)
            uniq.append(g)
    return uniq


def profile(items):
    raw = [tv(x) if isinstance(x, tuple) and len(x) == 4 else x for x in items]
    local_order3_ok = all(morder(g) == 3 for g in raw)
    gates = sym_gates(items)
    dist = {I4: 0}
    q = deque([I4])
    while q:
        x = q.popleft()
        for g in gates:
            y = mm(x, g)
            if y not in dist:
                dist[y] = dist[x] + 1
                q.append(y)
    hist = Counter(dist.values())
    sphere = [hist.get(i, 0) for i in range(max(hist) + 1)]
    balls = {f"B{k}": sum(c for d, c in hist.items() if d <= k) for k in [4,8,12,14]}
    return {"order": len(dist), "diameter": max(hist), "sphere": sphere, "balls": balls, "gate_count": len(gates), "local_order3_ok": local_order3_ok}


def tvdist(obs):
    n = max(len(obs), len(REF_SPHERE))
    a = obs + [0] * (n - len(obs))
    b = REF_SPHERE + [0] * (n - len(REF_SPHERE))
    return 0.5 * sum(abs(x / TOTAL - y / TOTAL) for x, y in zip(a, b))


def kld(obs):
    n = max(len(obs), len(REF_SPHERE))
    a = obs + [0] * (n - len(obs))
    b = REF_SPHERE + [0] * (n - len(REF_SPHERE))
    s = 0.0
    for x, y in zip(a, b):
        if x and y:
            s += (x / TOTAL) * math.log((x / TOTAL) / (y / TOTAL))
        elif x and not y:
            return float("inf")
    return s


def classify(p):
    errs = {k: abs(p["balls"][k] - REF_BALLS[k]) / REF_BALLS[k] for k in REF_BALLS}
    m = max(errs.values())
    t = tvdist(p["sphere"])
    if not p["local_order3_ok"] or p["order"] != TOTAL:
        band = "fail"
    elif p["diameter"] == DIAM and m <= 0.001 and t <= 0.0025:
        band = "pass"
    elif m <= 0.01 and t <= 0.02:
        band = "review"
    else:
        band = "fail"
    return {**p, "band": band, "checkpoint_max_rel_error": m, "sphere_tv": t, "sphere_kl": kld(p["sphere"])}


def build():
    cases = {
        "exact": BASE,
        "drop_last": BASE[:3],
        "swap_last": [BASE[0], BASE[1], BASE[2], ALT],
        "identity_last": [BASE[0], BASE[1], BASE[2], I4],
    }
    return {
        "bt": 1240,
        "title": "Synthetic word-metric recovery harness",
        "reference": {"order": TOTAL, "diameter": DIAM, "sphere": REF_SPHERE, "balls": REF_BALLS},
        "cases": {name: classify(profile(items)) for name, items in cases.items()},
        "interpretation": "The exact recovery passes. Missing a generator collapses to order 648. Swapping in a different transvection still reaches order 51840 but fails the word-metric fingerprint. Replacing a generator by identity fails the local order-three law and closure."
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=Path("data/bt1240_synthetic_word_metric_recovery_harness_summary.json"))
    ns = ap.parse_args()
    result = build()
    ns.out.parent.mkdir(parents=True, exist_ok=True)
    ns.out.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"bt": 1240, "bands": {k: v["band"] for k, v in result["cases"].items()}, "out": str(ns.out)}, indent=2))


if __name__ == "__main__":
    main()
