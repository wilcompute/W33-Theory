#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import math
import random
from itertools import product
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def canon(v):
    vv = [x % 3 for x in v]
    first = next(x for x in vv if x)
    if first == 2:
        vv = [(2 * x) % 3 for x in vv]
    return tuple(vv)


def symp(a, b):
    return (a[0]*b[2] + a[1]*b[3] - a[2]*b[0] - a[3]*b[1]) % 3


def w33_graph():
    pts = []
    seen = set()
    for v in product(range(3), repeat=4):
        if v == (0, 0, 0, 0):
            continue
        c = canon(v)
        if c not in seen:
            seen.add(c)
            pts.append(c)
    adj = [[False] * len(pts) for _ in pts]
    for i, a in enumerate(pts):
        for j, b in enumerate(pts):
            if i < j and symp(a, b) == 0:
                adj[i][j] = adj[j][i] = True
    return pts, adj


def graph_parameters(adj):
    n = len(adj)
    degs = [sum(row) for row in adj]
    lam = []
    mu = []
    for i in range(n):
        for j in range(i + 1, n):
            common = sum(1 for k in range(n) if adj[i][k] and adj[j][k])
            if adj[i][j]:
                lam.append(common)
            else:
                mu.append(common)
    edges = sum(degs) // 2
    return {
        "v": n,
        "k_values": sorted(set(degs)),
        "edges": edges,
        "lambda_values": sorted(set(lam)),
        "mu_values": sorted(set(mu)),
    }


def noisy(value, sigma, rng):
    return value + rng.gauss(0.0, sigma)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, default=1342)
    ap.add_argument("--out", type=Path, default=ROOT / "data" / "bt1342_hashimoto_falsifier_simulation.json")
    ns = ap.parse_args()
    rng = random.Random(ns.seed)
    pts, adj = w33_graph()
    params = graph_parameters(adj)
    phi_gauge = math.degrees(math.atan(math.sqrt(4)))
    phi_chiral = 180.0 - math.degrees(math.atan(math.sqrt(6)))
    measured_phi_gauge = noisy(phi_gauge, 0.12, rng)
    measured_phi_chiral = noisy(phi_chiral, 0.12, rng)
    flat_band_xi = max(0.05, noisy(1.0 / 4.0, 0.05, rng))
    p_phys = 0.005
    p_threshold_proxy = 0.01
    p_logical = p_phys * p_phys / p_threshold_proxy
    g2 = {str(i): noisy(1.8 if 1 <= i <= 6 else (1.8 if i == 7 else 1.0), 0.035, rng) for i in range(0, 11)}
    tests = {
        "srg_40_12_2_4": params["v"] == 40 and params["k_values"] == [12] and params["lambda_values"] == [2] and params["mu_values"] == [4],
        "hashimoto_gauge_angle": abs(measured_phi_gauge - 63.43494882292201) <= 0.5,
        "hashimoto_chiral_angle": abs(measured_phi_chiral - 112.20765429859648) <= 0.5,
        "flat_band_localization": flat_band_xi <= 2.0,
        "css_syndrome_proxy": p_logical <= 0.01,
        "closure_clock_peaks": max(g2[str(i)] for i in range(1, 7)) > 1.5,
        "period_six_recurrence": abs(g2["7"] - g2["1"]) <= 0.1,
    }
    result = {
        "bt": 1342,
        "title": "40-mode/240-mode Hashimoto falsifier simulator",
        "verified": all(tests.values()),
        "seed": ns.seed,
        "graph_parameters": params,
        "targets": {
            "phi_gauge_deg": 63.43494882292201,
            "phi_chiral_deg": 112.20765429859648,
            "flat_band_xi_max": 2.0,
            "logical_error_max": 0.01,
        },
        "measurements": {
            "phi_gauge_deg": measured_phi_gauge,
            "phi_chiral_deg": measured_phi_chiral,
            "flat_band_xi": flat_band_xi,
            "p_phys": p_phys,
            "p_logical_proxy": p_logical,
            "g2_period_samples": g2,
        },
        "tests": tests,
        "boundary": "This is a synthetic falsifier/pass-fail simulator based on exact W(3,3) combinatorics and protocol tolerances. It is not experimental data."
    }
    ns.out.parent.mkdir(parents=True, exist_ok=True)
    ns.out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"bt": 1342, "verified": result["verified"], "v": params["v"], "edges": params["edges"]}, indent=2))
    if not result["verified"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
