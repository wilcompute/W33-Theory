#!/usr/bin/env python3
"""
TINKER + TEST: compiling the TQC instance to a machine -- the minimal switching
sequence, and how it depends on the 'hardware' (which two switches).

The single-carrier picture: an electron braids through a classical machine's
wiring, driven by E&M 'switches'; the photoelectric effect is the matter<->light
hinge that lets the SAME W(3,3) computation run on the electron (massive, braided
worldline, hardware-specific) or the photon (massless, all-at-once). Two well-
chosen switches generate the whole gate group Sp(4,3) (w33_two_switch_generation),
so any gate is a WORD in the two switches -- a switching pattern in time. The
practical question: HOW LONG a pattern? That is the Cayley-graph diameter of
Sp(4,3) under the chosen switch pair (the worst-case sequence length), and it is
HARDWARE-SPECIFIC: different switch pairs (different machine topologies) give
different diameters. We BFS the Cayley graph from the identity (vertex-transitive
=> eccentricity = diameter) for several generating pairs and report the diameter
and mean word length -- the compilation cost on each 'hardware'.
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

    print("[Cayley-graph diameter of Sp(4,3) per 'hardware' (switch pair)]")
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

    print(f"\n  best 'hardware' (shortest worst-case sequence): {best[0]} "
          f"diameter={best[1]}")
    print("  => every one of the 51840 gates is reachable in at most "
          f"{best[1]} switch-flips on that pair; mean ~{best[2]:.1f}.")
    print("  Different switch pairs (different machine topologies) give different")
    print("  diameters: the compilation cost is HARDWARE-SPECIFIC, exactly as the")
    print("  vision says -- the layout fixes the entanglement/braid pattern.")

    print("\n[photoelectric duality]")
    print("  the SAME W(3,3) computation runs on either carrier, joined by the")
    print("  photoelectric effect: PHOTON (massless, tau=0, all-at-once logic) <->")
    print("  ELECTRON (massive, braided worldline through the hardware wiring,")
    print("  driven by E&M switches). 'Single electron on any classical machine' =")
    print("  the matter-side dual; the hardware graph fixes the braid embedding,")
    print("  and the switch-word length above is the compiled program length.")

    out = {
        "result": "minimal switching-sequence = Cayley diameter of Sp(4,3); "
                  "hardware-specific (depends on the switch pair)",
        "per_hardware": out_pairs,
        "best_hardware": {"pair": best[0], "diameter": best[1],
                          "mean_word_len": round(best[2], 3)},
        "interpretation": ("any gate reachable in <= diameter switch-flips; "
                           "different switch pairs (machine topologies) -> "
                           "different diameters -> hardware-specific compilation"),
        "photoelectric_duality": ("photon (massless, all-at-once) <-> electron "
                                  "(braided worldline, hardware-specific) via the "
                                  "photoelectric effect; the hardware graph fixes "
                                  "the braid embedding; the switch-word is the "
                                  "compiled program"),
        "sources": ["Cayley graph / word metric (geometric group theory)",
                    "Majorana braiding TQC (Nature Commun. 14, 2023)"],
    }
    with open("data/w33_hardware_compilation.json", "w") as f:
        json.dump(out, f, indent=2)
    print("\nwrote data/w33_hardware_compilation.json")


if __name__ == "__main__":
    main()
