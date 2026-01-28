#!/usr/bin/env python3
"""Compare Witting polytope vertices (realified C^4) with E8 roots in R^8.

We test whether the 240 Witting vertices (from the standard complex 4D model)
match E8 root inner-product structure after realification.

Outputs:
- artifacts/e8_witting_compare.json
- artifacts/e8_witting_compare.md
"""

from __future__ import annotations

import json
from itertools import product
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT_JSON = ROOT / "artifacts" / "e8_witting_compare.json"
OUT_MD = ROOT / "artifacts" / "e8_witting_compare.md"

omega = np.exp(2j * np.pi / 3)


def build_witting_vertices():
    # 40 base rays in C^4
    base_states = []

    # 4 basis states
    for i in range(4):
        s = np.zeros(4, dtype=complex)
        s[i] = 1
        base_states.append(s)

    omega_powers = [omega**k for k in range(3)]
    for mu in range(3):
        for nu in range(3):
            w_mu = omega_powers[mu]
            w_nu = omega_powers[nu]
            base_states.append(
                np.array([0, 1, -w_mu, w_nu], dtype=complex) / np.sqrt(3)
            )
            base_states.append(
                np.array([1, 0, -w_mu, -w_nu], dtype=complex) / np.sqrt(3)
            )
            base_states.append(
                np.array([1, -w_mu, 0, w_nu], dtype=complex) / np.sqrt(3)
            )
            base_states.append(np.array([1, w_mu, w_nu, 0], dtype=complex) / np.sqrt(3))

    # multiply by 6 phases
    phases = [1, omega, omega**2, -1, -omega, -(omega**2)]
    vertices = []
    for state in base_states:
        for phase in phases:
            vertices.append(phase * state)

    return np.array(vertices, dtype=complex)


def realify(vecs: np.ndarray) -> np.ndarray:
    # C^4 -> R^8
    return np.hstack([vecs.real, vecs.imag])


def build_e8_roots():
    roots = []
    # type 1: (±1, ±1, 0,...)
    for i in range(8):
        for j in range(i + 1, 8):
            for s1 in [1, -1]:
                for s2 in [1, -1]:
                    v = np.zeros(8)
                    v[i] = s1
                    v[j] = s2
                    roots.append(v)
    # type 2: (±1/2)^8 with even number of minus signs
    for signs in product([1, -1], repeat=8):
        if sum(1 for s in signs if s == -1) % 2 == 0:
            roots.append(np.array(signs) / 2.0)
    return np.array(roots, dtype=float)


def unique_rows(vecs: np.ndarray, tol: float = 1e-9):
    # de-duplicate via rounding
    rounded = np.round(vecs / tol) * tol
    uniq = np.unique(rounded, axis=0)
    return uniq


def dot_distribution(mat: np.ndarray, tol: float = 1e-6):
    # mat is (n, d) with normalized roots (norm^2 = 2)
    G = mat @ mat.T
    n = G.shape[0]
    # upper triangle excluding diagonal
    vals = []
    for i in range(n):
        for j in range(i + 1, n):
            vals.append(G[i, j])
    vals = np.array(vals)
    rounded = np.round(vals / tol) * tol
    unique, counts = np.unique(rounded, return_counts=True)
    dist = {float(u): int(c) for u, c in zip(unique, counts)}
    return dist, G


def neighbor_counts(G: np.ndarray, target: float, tol: float = 1e-6):
    n = G.shape[0]
    counts = []
    for i in range(n):
        cnt = int(np.sum(np.abs(G[i] - target) < tol)) - 1  # exclude self
        counts.append(cnt)
    return sorted(set(counts))


def normalize_to_sqrt2(vecs: np.ndarray):
    norms = np.linalg.norm(vecs, axis=1)
    # target norm = sqrt(2)
    return vecs * (np.sqrt(2.0) / norms)[:, None]


def main():
    witting_c = build_witting_vertices()
    witting_c = unique_rows(witting_c)
    witting_r = realify(witting_c)
    witting_r = normalize_to_sqrt2(witting_r)

    e8 = build_e8_roots()
    e8 = unique_rows(e8)
    e8 = normalize_to_sqrt2(e8)

    w_dist, wG = dot_distribution(witting_r)
    e_dist, eG = dot_distribution(e8)

    summary = {
        "witting_count": int(witting_r.shape[0]),
        "e8_count": int(e8.shape[0]),
        "witting_norms_sq": [
            float(x) for x in np.unique(np.round(np.sum(witting_r**2, axis=1), 6))
        ],
        "e8_norms_sq": [
            float(x) for x in np.unique(np.round(np.sum(e8**2, axis=1), 6))
        ],
        "witting_dot_distribution": w_dist,
        "e8_dot_distribution": e_dist,
        "witting_neighbor_counts_ip1": neighbor_counts(wG, 1.0),
        "e8_neighbor_counts_ip1": neighbor_counts(eG, 1.0),
        "witting_neighbor_counts_ip0": neighbor_counts(wG, 0.0),
        "e8_neighbor_counts_ip0": neighbor_counts(eG, 0.0),
        "witting_neighbor_counts_ip-1": neighbor_counts(wG, -1.0),
        "e8_neighbor_counts_ip-1": neighbor_counts(eG, -1.0),
    }

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(summary, indent=2), encoding="utf-8")

    lines = []
    lines.append("# E8 vs Witting (Realified) Comparison")
    lines.append("")
    lines.append(f"- Witting vertices (unique): {summary['witting_count']}")
    lines.append(f"- E8 roots (unique): {summary['e8_count']}")
    lines.append(f"- Witting norms^2: {summary['witting_norms_sq']}")
    lines.append(f"- E8 norms^2: {summary['e8_norms_sq']}")
    lines.append("")
    lines.append("## Inner-Product Distributions (distinct pairs)")
    lines.append("")
    lines.append("Witting:")
    for k in sorted(summary["witting_dot_distribution"].keys()):
        lines.append(f"- {k}: {summary['witting_dot_distribution'][k]}")
    lines.append("")
    lines.append("E8:")
    for k in sorted(summary["e8_dot_distribution"].keys()):
        lines.append(f"- {k}: {summary['e8_dot_distribution'][k]}")
    lines.append("")
    lines.append("## Neighbor Count Sets (per vertex)")
    lines.append("")
    lines.append(f"- Witting ip=1 counts: {summary['witting_neighbor_counts_ip1']}")
    lines.append(f"- E8 ip=1 counts: {summary['e8_neighbor_counts_ip1']}")
    lines.append(f"- Witting ip=0 counts: {summary['witting_neighbor_counts_ip0']}")
    lines.append(f"- E8 ip=0 counts: {summary['e8_neighbor_counts_ip0']}")
    lines.append(f"- Witting ip=-1 counts: {summary['witting_neighbor_counts_ip-1']}")
    lines.append(f"- E8 ip=-1 counts: {summary['e8_neighbor_counts_ip-1']}")

    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"Wrote {OUT_JSON}")
    print(f"Wrote {OUT_MD}")


if __name__ == "__main__":
    main()
