#!/usr/bin/env python3
"""Analyze triangle phase as sum of pair-phase classes.

We classify each non-orthogonal pair by its overlap phase (rounded to pi/6 grid).
Then for each triangle we:
  - count how many pair phases lie in the odd pi/6 lattice
  - sum the three pair phases (wrapped) and compare to triangle phase
We test whether triangle phase is determined by the odd-count or by
the multiset of pair phase classes.
"""
from __future__ import annotations

import json
import itertools
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]


def construct_witting_40_rays():
    omega = np.exp(2j * np.pi / 3)
    sqrt3 = np.sqrt(3)
    rays = []
    for i in range(4):
        v = np.zeros(4, dtype=complex)
        v[i] = 1
        rays.append(v)
    for mu in range(3):
        for nu in range(3):
            rays.append(np.array([0, 1, -omega**mu, omega**nu]) / sqrt3)
            rays.append(np.array([1, 0, -omega**mu, -omega**nu]) / sqrt3)
            rays.append(np.array([1, -omega**mu, 0, omega**nu]) / sqrt3)
            rays.append(np.array([1, omega**mu, omega**nu, 0]) / sqrt3)
    return rays


def wrap_angle(a):
    return np.arctan2(np.sin(a), np.cos(a))


def phase_cluster(angle):
    a = wrap_angle(angle)
    targets = [np.pi/6, -np.pi/6, np.pi/2, -np.pi/2]
    nearest = min(targets, key=lambda t: abs(a - t))
    return round(float(nearest), 6)


def is_odd_lattice(angle):
    # odd multiples of pi/6: pi/6, pi/2, 5pi/6, ...
    k = round(angle / (np.pi / 6))
    return k % 2 != 0


def main():
    rays = construct_witting_40_rays()
    n = len(rays)

    pair_phase = {}
    for i in range(n):
        for j in range(i + 1, n):
            ip = np.vdot(rays[i], rays[j])
            if abs(ip) < 1e-8:
                continue
            pair_phase[(i, j)] = wrap_angle(np.angle(ip))

    # triangle analysis
    odd_count_table = defaultdict(Counter)
    multiset_table = defaultdict(Counter)
    sum_match = Counter()
    triples = 0

    for i, j, k in itertools.combinations(range(n), 3):
        p_ij = pair_phase.get((i, j))
        p_jk = pair_phase.get((j, k))
        p_ik = pair_phase.get((i, k))
        if p_ij is None or p_jk is None or p_ik is None:
            continue
        triples += 1
        tri_prod = np.vdot(rays[i], rays[j]) * np.vdot(rays[j], rays[k]) * np.vdot(rays[k], rays[i]).conjugate()
        tri_phase = wrap_angle(np.angle(tri_prod))
        tri_cluster = phase_cluster(tri_phase)

        phases = [p_ij, p_jk, p_ik]
        odd_count = sum(1 for p in phases if is_odd_lattice(p))
        odd_count_table[odd_count][tri_cluster] += 1

        # multiset of pair phase classes on pi/6 grid
        phase_classes = sorted(round(float(wrap_angle(p)), 6) for p in phases)
        multiset_table[tuple(phase_classes)][tri_cluster] += 1

        # check if triangle phase equals sum of pair phases (wrapped)
        s = wrap_angle(sum(phases))
        sum_match[phase_cluster(s) == tri_cluster] += 1

    out = {
        "triples": triples,
        "odd_count_table": {
            str(k): {str(c): n for c, n in sorted(v.items())}
            for k, v in odd_count_table.items()
        },
        "multiset_table_size": len(multiset_table),
        "sum_match": {str(k): v for k, v in sum_match.items()},
    }

    out_path = ROOT / "artifacts" / "witting_triangle_phase_word.json"
    out_path.write_text(json.dumps(out, indent=2), encoding="utf-8")

    md_path = ROOT / "docs" / "witting_triangle_phase_word.md"
    with md_path.open("w", encoding="utf-8") as f:
        f.write("# Triangle Phase vs Pair‑Phase Word\n\n")
        f.write(f"Non‑orthogonal triples analyzed: **{triples}**\n\n")
        f.write("## Odd‑lattice count -> triangle phase cluster\n\n")
        f.write("odd count | clusters\n")
        f.write("--- | ---\n")
        for k in sorted(odd_count_table.keys()):
            clusters = ", ".join(f"{c}:{n}" for c, n in sorted(odd_count_table[k].items()))
            f.write(f"{k} | {clusters}\n")
        f.write("\n## Pair‑phase multiset table size\n\n")
        f.write(f"{len(multiset_table)} unique multisets\n\n")
        f.write("## Triangle phase equals sum of pair phases?\n\n")
        f.write("match | count\n")
        f.write("--- | ---\n")
        for k, v in sorted(sum_match.items()):
            f.write(f"{k} | {v}\n")
    print(f"Wrote {out_path}")
    print(f"Wrote {md_path}")


if __name__ == "__main__":
    main()
