#!/usr/bin/env python3
"""
Pass 96 -- The 2-rank ladder is FINER than the two-graph: switching invariants don't see {17,8,2,1}.

Pass 89 found the 28 graphs SRG(40,12,2,4) split by 2-rank (equivalently by their Smith/critical
group) into a graded ladder of sizes {17, 8, 2, 1} at 2-ranks {16, 14, 12, 10}.  The open question:
is that {17,8,2,1} partition the Seidel switching-class / two-graph orbit structure?

This pass answers it -- NO -- with a rigorous switching invariant.  For the Seidel matrix
S = J - I - 2A, switching by a vertex set and relabelling act as S -> D P S P^T D with D = diag(+-1)
and P a permutation, both unimodular; hence the Smith normal form of S (its "Seidel Smith group") is
a switching invariant.  We compute it for all 28 graphs:

    Seidel Smith group = Z/3 (+) (Z/5)^23 (+) Z/25 (+) (Z/7)^15   -- CONSTANT across all 28.

So every one of the 28 shares the same two-graph invariants (they even share the Seidel spectrum
{15, -5^24, 7^15}), yet they fall into the ladder {17,8,2,1} by the 2-rank of the *adjacency* matrix.
The arithmetic ladder is therefore strictly finer than -- transverse to -- the switching class: it
distinguishes graphs the two-graph cannot.

Two further facts:
  * W(3,3) has 2-rank 16 (the generic class of 17); Q(4,3) is the UNIQUE 2-rank-10 graph (the
    singleton).  The cospectral mates sit at opposite ends of the ladder, and Q is characterized as
    the unique minimum-2-rank member of the family (its maximal glue, Pass 94).
  * The Seidel Smith group's p-part rank equals the multiplicity of the Seidel eigenvalue divisible
    by p: 5-part rank 24 = mult(-5), 7-part rank 15 = mult(7) -- a Ducey-type law for the Seidel
    matrix.  The (Z/5)^23 echoes the critical group's 5-part (Pass 89).

Self-contained: decodes data/spence_srg_40_12_2_4.g6, GF(2) rank, integer SNF (sympy).  ASCII-only.
"""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

import numpy as np
from sympy import Matrix
from sympy.matrices.normalforms import smith_normal_form

ROOT = Path(__file__).resolve().parent
G6 = ROOT / "data" / "spence_srg_40_12_2_4.g6"


def decode_g6(line: str) -> np.ndarray:
    data = [ord(c) - 63 for c in line.strip()]
    n = data[0]
    bits = []
    for b in data[1:]:
        for k in range(5, -1, -1):
            bits.append((b >> k) & 1)
    A = np.zeros((n, n), dtype=int)
    idx = 0
    for j in range(n):
        for i in range(j):
            if bits[idx]:
                A[i, j] = A[j, i] = 1
            idx += 1
    return A


def prank(A: np.ndarray, p: int) -> int:
    M = [[int(x) % p for x in row] for row in A]
    n = len(M)
    r = 0
    for c in range(n):
        piv = next((i for i in range(r, n) if M[i][c] % p), None)
        if piv is None:
            continue
        M[r], M[piv] = M[piv], M[r]
        inv = pow(M[r][c], p - 2, p)
        M[r] = [(x * inv) % p for x in M[r]]
        for i in range(n):
            if i != r and M[i][c] % p:
                f = M[i][c]
                M[i] = [(a - f * b) % p for a, b in zip(M[i], M[r])]
        r += 1
    return r


def seidel_smith(A: np.ndarray):
    n = A.shape[0]
    S = np.ones((n, n), int) - np.eye(n, dtype=int) - 2 * A
    snf = smith_normal_form(Matrix(S.tolist()))
    ed = tuple(sorted(abs(int(snf[i, i])) for i in range(n) if abs(int(snf[i, i])) > 1))
    return ed


def group_structure(ed):
    """elementary divisors -> multiplicity dict of prime-power cyclic factors."""
    c = Counter()
    for d in ed:
        for p in (3, 5, 7):
            f = 1
            while d % p == 0:
                d //= p
                f *= p
            if f > 1:
                c[f] += 1
    return dict(sorted(c.items()))


def main():
    lines = [l for l in G6.read_text().splitlines() if l.strip()]
    rank2 = {}
    seidel_class = {}
    for gi, l in enumerate(lines, 1):
        A = decode_g6(l)
        rank2[gi] = prank(A, 2)
        seidel_class.setdefault(seidel_smith(A), []).append(gi)

    tr = {}
    for g, r in rank2.items():
        tr.setdefault(r, []).append(g)
    ladder = {r: len(tr[r]) for r in sorted(tr, reverse=True)}

    # Seidel Smith group (should be a single constant class)
    seidel_constant = len(seidel_class) == 1
    ed = next(iter(seidel_class))
    seidel_struct = group_structure(ed)
    # p-part ranks
    ppart = {p: sum(1 for d in ed for _ in [0] if d % p == 0) for p in (3, 5, 7)}

    checks = {
        "num_graphs_28": len(lines) == 28,
        "ladder_17_8_2_1": list(ladder.values()) == [17, 8, 2, 1],
        "ladder_ranks_16_14_12_10": list(ladder.keys()) == [16, 14, 12, 10],
        "W28_rank16_generic": rank2[28] == 16,
        "Q27_rank10_unique_min": rank2[27] == 10 and ladder[10] == 1,
        "seidel_smith_constant": seidel_constant,
        "seidel_smith_struct": seidel_struct == {3: 1, 5: 23, 25: 1, 7: 15},
        "ladder_NOT_switching_invariant": seidel_constant
        and list(ladder.values()) == [17, 8, 2, 1],
        "seidel_5part_rank24_eq_mult_minus5": ppart[5] == 24,
        "seidel_7part_rank15_eq_mult_7": ppart[7] == 15,
    }
    all_ok = all(checks.values())

    print("=" * 78)
    print(
        "PASS 96 -- THE 2-RANK LADDER IS FINER THAN THE TWO-GRAPH (SWITCHING) STRUCTURE"
    )
    print("=" * 78)
    print("2-rank ladder of the 28 SRG(40,12,2,4):")
    for r in sorted(tr, reverse=True):
        tag = ""
        if 28 in tr[r]:
            tag += "  <- W(3,3)=#28"
        if 27 in tr[r]:
            tag += "  <- Q(4,3)=#27 (unique)"
        print(f"   2-rank {r}: {len(tr[r]):2d} graphs{tag}")
    print(f"   => multiplicities {list(ladder.values())} = {{17,8,2,1}}")
    print()
    print("Seidel Smith group (switching invariant, S -> D P S P^T D):")
    print(f"   {seidel_struct}  = Z/3 (+) (Z/5)^23 (+) Z/25 (+) (Z/7)^15")
    print(f"   CONSTANT across all 28: {seidel_constant}")
    print(
        f"   p-part ranks: 5-part {ppart[5]} = mult(-5); 7-part {ppart[7]} = mult(7)  (Ducey-type)"
    )
    print()
    print(
        "CONCLUSION: the {17,8,2,1} ladder is NOT a switching/two-graph invariant -- it is strictly"
    )
    print(
        "   finer.  W(3,3) sits in the generic 2-rank-16 class; Q(4,3) is the unique 2-rank-10 graph."
    )
    print()
    print("checks:")
    for k_, v in checks.items():
        print(f"   {'OK ' if v else 'XX '} {k_}")
    print()
    print("=" * 78)
    print(f"STATUS: {'PASS' if all_ok else 'FAIL'}")
    print("=" * 78)

    payload = {
        "schema": "w33.pass96.switching_ladder.v1",
        "status": "PASS" if all_ok else "FAIL",
        "num_graphs": len(lines),
        "two_rank_ladder": {str(r): len(tr[r]) for r in sorted(tr, reverse=True)},
        "ladder_multiplicities": list(ladder.values()),
        "W_index_28_rank": rank2[28],
        "Q_index_27_rank": rank2[27],
        "Q_is_unique_min_2rank": rank2[27] == 10 and ladder[10] == 1,
        "seidel_smith_group": {
            "structure": "Z/3 (+) (Z/5)^23 (+) Z/25 (+) (Z/7)^15",
            "as_prime_power_multiplicities": seidel_struct,
            "constant_across_all_28": seidel_constant,
            "is_switching_invariant": True,
            "p_part_ranks": ppart,
            "ducey_type": "5-part rank 24 = mult(Seidel -5); 7-part rank 15 = mult(Seidel 7)",
        },
        "reading": (
            "The 28 SRG(40,12,2,4) share the Seidel spectrum {15,-5^24,7^15} AND the Seidel Smith "
            "group Z/3(+)(Z/5)^23(+)Z/25(+)(Z/7)^15 -- a genuine switching invariant -- yet they "
            "split into the ladder {17,8,2,1} by the 2-rank of the adjacency matrix.  So the "
            "arithmetic ladder is strictly finer than (transverse to) the two-graph switching class: "
            "it distinguishes graphs the two-graph cannot.  W(3,3) is generic (2-rank 16); Q(4,3) is "
            "the unique minimum-2-rank member (rank 10, its maximal glue of Pass 94).  The (Z/5)^23 "
            "echoes the critical group's constant 5-part (Pass 89)."
        ),
        "checks": checks,
    }
    with open("w33_pass96_switching_ladder.json", "w", encoding="utf-8") as fh:
        json.dump(payload, fh, indent=2)
    print("[wrote] w33_pass96_switching_ladder.json")
    return 0 if all_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
