#!/usr/bin/env python3
"""
TINKER + TEST: finite word metrics for selected two-generator alphabets.

Two selected abstract symplectic generators can generate Sp(4,3), so every
group element has a word in that alphabet.  This file computes the Cayley-graph
diameter and mean word length for four such selected pairs.  The resulting
metric is a property of the chosen abstract generating set.  It is not a
device-level compilation, a braid construction, or evidence that a particular
physical machine topology has that cost.
"""
from __future__ import annotations

import json
from collections import deque

F = 3


def mm(A, B):
    return tuple(tuple(sum(A[i][k] * B[k][j] for k in range(4)) % F
                       for j in range(4)) for i in range(4))


def inv(M):
    # brute inverse over F_3 (group element, finite order): M^(order-1)
    I4 = ((1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1))
    P, k = M, 1
    while P != I4:
        P = mm(P, M); k += 1
    return mm(M, M) if k == 1 else _pow(M, k - 1)


def _pow(M, e):
    I4 = ((1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1))
    R = I4
    for _ in range(e):
        R = mm(R, M)
    return R


def cayley_bfs(gens):
    """BFS from identity over the symmetric generating set; return (n, diameter,
    mean distance)."""
    I4 = ((1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1))
    moves = list(gens) + [inv(g) for g in gens]
    dist = {I4: 0}
    dq = deque([I4])
    total = 0
    diam = 0
    while dq:
        M = dq.popleft()
        d = dist[M]
        for g in moves:
            N = mm(M, g)
            if N not in dist:
                dist[N] = d + 1
                total += d + 1
                diam = max(diam, d + 1)
                dq.append(N)
    return len(dist), diam, total / len(dist)


def main():
    lib = {
        "F1": ((0, 0, 1, 0), (0, 1, 0, 0), (2, 0, 0, 0), (0, 0, 0, 1)),
        "F2": ((1, 0, 0, 0), (0, 0, 0, 1), (0, 0, 1, 0), (0, 2, 0, 0)),
        "S1": ((1, 0, 0, 0), (0, 1, 0, 0), (1, 0, 1, 0), (0, 0, 0, 1)),
        "S2": ((1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 1, 0), (0, 1, 0, 1)),
        "CZ": ((1, 0, 0, 0), (0, 1, 0, 0), (0, 1, 1, 0), (1, 0, 0, 1)),
        "SUM": ((1, 0, 0, 0), (1, 1, 0, 0), (0, 0, 1, 2), (0, 0, 0, 1)),
    }
    F1CZ = mm(lib["F1"], lib["CZ"])
    F1SUM = mm(lib["F1"], lib["SUM"])
    # generating pairs (each verified to give Sp(4,3) in w33_two_switch_generation)
    pairs = {
        "<F2, F1.CZ>": [lib["F2"], F1CZ],
        "<SUM, F1.CZ>": [lib["SUM"], F1CZ],
        "<F2, F1.SUM>": [lib["F2"], F1SUM],
        "<CZ, F1.SUM>": [lib["CZ"], F1SUM],
    }

    print("[Cayley-graph diameter of Sp(4,3) per abstract switch pair]")
    print("  pair (two switches)        | group size | DIAMETER | mean word len")
    out_pairs = {}
    best = None
    for name, gens in pairs.items():
        n, diam, mean = cayley_bfs(gens)
        out_pairs[name] = {"size": n, "diameter": diam, "mean_word_len": round(mean, 3)}
        print(f"  {name:26s} | {n:10d} | {diam:8d} | {mean:.3f}")
        assert n == 51840
        if best is None or diam < best[1]:
            best = (name, diam, mean)

    print(f"\n  best selected pair (shortest worst-case sequence): {best[0]} "
          f"diameter={best[1]}")
    print("  => every one of the 51840 gates is reachable in at most "
          f"{best[1]} switch-flips on that pair; mean ~{best[2]:.1f}.")
    print("  The calculation compares abstract generator alphabets only; a physical")
    print("  topology or braid embedding needs a separate compiler and device model.")

    out = {
        "result": "Cayley word metrics of Sp(4,3) for four selected abstract "
                  "two-generator alphabets",
        "per_hardware": out_pairs,
        "best_hardware": {"pair": best[0], "diameter": best[1],
                          "mean_word_len": round(best[2], 3)},
        "interpretation": ("Each selected pair provides an abstract binary word "
                           "alphabet. The recorded diameter is a finite Cayley "
                           "word-metric bound for that alphabet, not a physical "
                           "latency or optical-switch-depth prediction."),
        "hardware_boundary": ("No braid, photon/electron implementation, loss "
                              "model, or layout follows from this group-theoretic "
                              "word-metric calculation."),
        "sources": ["Cayley graph / word metric (geometric group theory)",
                    "Majorana braiding TQC (Nature Commun. 14, 2023)"],
    }
    with open("data/w33_hardware_compilation.json", "w") as f:
        json.dump(out, f, indent=2)
    print("\nwrote data/w33_hardware_compilation.json")


if __name__ == "__main__":
    main()
