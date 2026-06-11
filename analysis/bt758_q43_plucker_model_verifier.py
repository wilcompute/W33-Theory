#!/usr/bin/env python3
"""BT758 — executable Q(4,3) Pluecker-dual model verifier.

This converts the BT755 program note into a concrete finite-geometric model.
It builds the parabolic quadric Q(4,3) inside PG(4,3), enumerates its totally
singular projective lines, and verifies the dual generalized-quadrangle
incidence parameters.  The intended bridge is:

    Q(4,3) = dual polar generalized quadrangle of W(3,3)

For q=3, Q(4,3) and W(3,3) are dual but not point-line self-dual.  Therefore
this script verifies the model and polarity/dual incidence substrate, but it
does not claim that the BT750 duo half-turn r^6 has already been identified
with a Pluecker polarity.
"""
from __future__ import annotations

import itertools
import json
from collections import Counter, defaultdict
from pathlib import Path

MOD = 3
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "bt758_q43_plucker_model_summary.json"


def inv(a: int) -> int:
    a %= MOD
    if a == 1:
        return 1
    if a == 2:
        return 2
    raise ZeroDivisionError(a)


def norm(v):
    v = tuple(x % MOD for x in v)
    for x in v:
        if x % MOD:
            s = inv(x)
            return tuple((s * y) % MOD for y in v)
    raise ValueError("zero vector")


def add(u, v):
    return tuple((a + b) % MOD for a, b in zip(u, v))


def smul(a, v):
    return tuple((a * x) % MOD for x in v)


def qform(v):
    # Nondegenerate parabolic form over F_3.
    x0, x1, x2, x3, x4 = v
    return (x0 * x1 + x2 * x3 + x4 * x4) % MOD


def bform(u, v):
    # Polar form of qform: Q(u+v)-Q(u)-Q(v).
    return (u[0] * v[1] + u[1] * v[0] + u[2] * v[3] + u[3] * v[2] + 2 * u[4] * v[4]) % MOD


def projective_points(dim):
    pts = set()
    for v in itertools.product(range(MOD), repeat=dim):
        if any(v):
            pts.add(norm(v))
    return sorted(pts)


def projective_line(p, q):
    pts = {p, q}
    for a in range(MOD):
        for b in range(MOD):
            if a or b:
                pts.add(norm(add(smul(a, p), smul(b, q))))
    return frozenset(pts)


def build_q43():
    pg4 = projective_points(5)
    qpts = [p for p in pg4 if qform(p) == 0]
    qset = set(qpts)
    lines = set()
    for p, q in itertools.combinations(qpts, 2):
        L = projective_line(p, q)
        if len(L) == 4 and L <= qset:
            lines.add(L)
    lines = sorted(lines, key=lambda L: sorted(L))
    return qpts, lines


def collinearity(qpts, lines):
    idx = {p: i for i, p in enumerate(qpts)}
    adj = [[False] * len(qpts) for _ in qpts]
    point_lines = defaultdict(list)
    for li, L in enumerate(lines):
        Ls = list(L)
        for p in Ls:
            point_lines[p].append(li)
        for a, b in itertools.combinations(Ls, 2):
            i, j = idx[a], idx[b]
            adj[i][j] = adj[j][i] = True
    degrees = [sum(row) for row in adj]
    lambdas = Counter()
    mus = Counter()
    for i, j in itertools.combinations(range(len(qpts)), 2):
        cn = sum(adj[i][k] and adj[j][k] for k in range(len(qpts)))
        if adj[i][j]:
            lambdas[cn] += 1
        else:
            mus[cn] += 1
    return degrees, lambdas, mus, point_lines


def dual_line_graph(lines):
    # Lines of Q(4,3) are points of the dual W(3,3). Two are adjacent if they meet.
    n = len(lines)
    adj = [[False] * n for _ in range(n)]
    for i, j in itertools.combinations(range(n), 2):
        if lines[i] & lines[j]:
            adj[i][j] = adj[j][i] = True
    degrees = [sum(row) for row in adj]
    lambdas = Counter()
    mus = Counter()
    for i, j in itertools.combinations(range(n), 2):
        cn = sum(adj[i][k] and adj[j][k] for k in range(n))
        if adj[i][j]:
            lambdas[cn] += 1
        else:
            mus[cn] += 1
    return degrees, lambdas, mus


def main():
    qpts, lines = build_q43()
    degrees, lambdas, mus, point_lines = collinearity(qpts, lines)
    ddeg, dlambda, dmu = dual_line_graph(lines)

    checks = {
        "Q43_point_count_40": len(qpts) == 40,
        "Q43_line_count_40": len(lines) == 40,
        "each_line_has_4_points": sorted({len(L) for L in lines}) == [4],
        "each_point_on_4_lines": sorted(Counter(len(point_lines[p]) for p in qpts).items()) == [(4, 40)],
        "point_collinearity_SRG_40_12_2_4": sorted(set(degrees)) == [12] and lambdas == Counter({2: 240}) and mus == Counter({4: 540}),
        "dual_line_graph_SRG_40_12_2_4": sorted(set(ddeg)) == [12] and dlambda == Counter({2: 240}) and dmu == Counter({4: 540}),
    }
    summary = {
        "theorem": "BT758 executable Q(4,3) Pluecker model verifier",
        "field": "F_3",
        "quadratic_form": "x0*x1 + x2*x3 + x4^2",
        "point_count": len(qpts),
        "line_count": len(lines),
        "line_sizes": sorted(Counter(len(L) for L in lines).items()),
        "point_line_degrees": sorted(Counter(len(point_lines[p]) for p in qpts).items()),
        "point_collinearity_degrees": sorted(Counter(degrees).items()),
        "point_collinearity_lambda_counter": dict(lambdas),
        "point_collinearity_mu_counter": dict(mus),
        "dual_line_graph_degrees": sorted(Counter(ddeg).items()),
        "dual_line_graph_lambda_counter": dict(dlambda),
        "dual_line_graph_mu_counter": dict(dmu),
        "checks": checks,
        "all_checks_pass": all(checks.values()),
        "boundary": "This verifies Q(4,3) and its dual W33 incidence substrate. It does not yet identify the BT750 duo half-turn r^6 with a Pluecker polarity or transported dual-apartment orientation.",
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))
    if not summary["all_checks_pass"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
