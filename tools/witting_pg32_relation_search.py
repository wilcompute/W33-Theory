#!/usr/bin/env python3
"""Search for PG(3,2) trace-image relations that reproduce W33 adjacency.

We compute trace-image sets for each Witting ray under scalars {1, ω, ω^2},
then classify ray pairs by intersection/union sizes. We test whether any
single class or union of classes reproduces the W33 adjacency.

Outputs:
- artifacts/witting_pg32_relation_search.json
- artifacts/witting_pg32_relation_search.md
"""
from __future__ import annotations

import json
from itertools import combinations, product
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT_JSON = ROOT / "artifacts" / "witting_pg32_relation_search.json"
OUT_MD = ROOT / "artifacts" / "witting_pg32_relation_search.md"

# GF(4) arithmetic
def gf4_add(a: int, b: int) -> int:
    return a ^ b

def gf4_mul(a: int, b: int) -> int:
    if a == 0 or b == 0:
        return 0
    a0, a1 = a & 1, (a >> 1) & 1
    b0, b1 = b & 1, (b >> 1) & 1
    c0 = a0 * b0
    c1 = a0 * b1 + a1 * b0
    c2 = a1 * b1
    c0 = (c0 + c2) % 2
    c1 = (c1 + c2) % 2
    return (c1 << 1) | c0

def gf4_square(a: int) -> int:
    return gf4_mul(a, a)

def gf4_trace(a: int) -> int:
    return gf4_add(a, gf4_square(a)) & 1

def gf4_inv(a: int) -> int:
    if a == 0:
        raise ZeroDivisionError
    for b in [1, 2, 3]:
        if gf4_mul(a, b) == 1:
            return b
    raise ZeroDivisionError

omega = 2
omega2 = 3
omega_powers = [1, omega, omega2]

def build_base_states():
    states = []
    for i in range(4):
        v = [0, 0, 0, 0]
        v[i] = 1
        states.append(tuple(v))
    for mu, nu in product(range(3), repeat=2):
        w_mu = omega_powers[mu]
        w_nu = omega_powers[nu]
        states.append((0, 1, w_mu, w_nu))
        states.append((1, 0, w_mu, w_nu))
        states.append((1, w_mu, 0, w_nu))
        states.append((1, w_mu, w_nu, 0))
    return states

def normalize_projective(v):
    for x in v:
        if x != 0:
            inv = gf4_inv(x)
            return tuple(gf4_mul(inv, xi) for xi in v)
    return None

def hermitian(u, v):
    s = 0
    for a, b in zip(u, v):
        s = gf4_add(s, gf4_mul(a, gf4_square(b)))
    return s

def trace_map(v):
    return tuple(gf4_trace(x) for x in v)

def main():
    base_states = [normalize_projective(s) for s in build_base_states()]
    base_states = list(dict.fromkeys(base_states))
    if len(base_states) != 40:
        raise SystemExit(f"Expected 40 projective states, got {len(base_states)}")

    # W33 adjacency
    n = len(base_states)
    adj = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            if hermitian(base_states[i], base_states[j]) == 0:
                adj[i][j] = 1
                adj[j][i] = 1

    # trace images under scalars {1, ω, ω^2}
    scalars = [1, omega, omega2]
    images = []
    for s in base_states:
        imgs = set()
        for c in scalars:
            scaled = tuple(gf4_mul(c, x) for x in s)
            p = trace_map(scaled)
            if p != (0, 0, 0, 0):
                imgs.add(p)
        images.append(imgs)

    # classify pairs
    class_map = {}
    pair_classes = {}
    for i in range(n):
        for j in range(i + 1, n):
            A = images[i]
            B = images[j]
            inter = len(A & B)
            union = len(A | B)
            key = (len(A), len(B), inter, union)
            class_map.setdefault(key, []).append((i, j))
            pair_classes[(i, j)] = key

    class_keys = sorted(class_map.keys())

    # test each class and unions
    matches = []
    for mask in range(1, 1 << len(class_keys)):
        selected = {class_keys[i] for i in range(len(class_keys)) if (mask >> i) & 1}
        # build adjacency
        ok = True
        for i in range(n):
            for j in range(i + 1, n):
                in_sel = pair_classes[(i, j)] in selected
                if in_sel != bool(adj[i][j]):
                    ok = False
                    break
            if not ok:
                break
        if ok:
            matches.append([str(k) for k in selected])

    summary = {
        "class_count": len(class_keys),
        "class_sizes": {str(k): len(class_map[k]) for k in class_keys},
        "w33_matches": matches,
    }

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(summary, indent=2), encoding="utf-8")

    lines = []
    lines.append("# Witting PG(3,2) Relation Search")
    lines.append("")
    lines.append(f"- relation classes: {summary['class_count']}")
    lines.append("## Class sizes")
    for k in class_keys:
        lines.append(f"- {k}: {len(class_map[k])}")
    lines.append("")
    lines.append("## W33 adjacency matches")
    if matches:
        for m in matches:
            lines.append(f"- {m}")
    else:
        lines.append("- none")

    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {OUT_JSON}")
    print(f"Wrote {OUT_MD}")

if __name__ == "__main__":
    main()
