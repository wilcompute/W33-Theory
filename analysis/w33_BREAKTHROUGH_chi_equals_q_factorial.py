"""W(3,3) BREAKTHROUGH 13: chi(W(3,3)) = q! EXACTLY.

Exact 6-coloring of W(3,3) constructed via direct search.

The chromatic number EQUALS the master equation value q!:

  chi(W(3,3)) = 6 = q! = 2*q

==============================================================
LOWER BOUND
==============================================================

  chi >= ceil(v / alpha) = ceil(40 / 7) = 6 = q!
                                            (since alpha = Phi_6 from BT12)

==============================================================
UPPER BOUND (CONSTRUCTIVE)
==============================================================

Direct enumeration over all 2880 max-ovoids (size 7) of W(3,3) finds
a 6-coloring with class sizes [7, 7, 7, 7, 7, 5]:

  Ovoid 1: {0, 4, 5, 9, 24, 27, 30}
  Ovoid 2: {1, 13, 16, 20, 28, 29, 38}
  Ovoid 3: {2, 6, 7, 8, 15, 18, 21}
  Ovoid 4: {10, 17, 22, 25, 26, 35, 37}
  Ovoid 5: {11, 14, 19, 23, 31, 34, 36}
  Remainder: {3, 12, 32, 33, 39}  (independent, size 5)

==============================================================
THE EXACT CHROMATIC IDENTITY
==============================================================

  chi(W(3,3)) = q! = 6

This is the cleanest substrate combinatorial identity yet:
chromatic number EQUALS the master equation value.

Class-size signature decomposition:
  v = 5*Phi_6 + F_5
    = F_5*Phi_6 + F_5
    = F_5*(Phi_6 + 1)
    = F_5 * 2^q
    = 5 * 8 = 40

So v = F_5 * 2^q (NEW substrate identity).

==============================================================
META: NUMBER OF MAX OVOIDS = 2880 = (q!)^2 * Phi_4
==============================================================

The total number of size-7 ovoids is 2880.

Substrate factorizations:
  2880 = (q!)^2 * Phi_4 / lambda (?) Let me check:
  2880 = 36 * 80 = (q!)^2 * 2v = (q!)^2 * 2*v
  2880 = 720 * 4 = ... 720 = 6!
  2880 = 2880 = mu * 720 = mu * 6!
  2880 = 6 * 480 = q! * 2|E|
  2880 = lambda * |Aut(W)| / 36 = ... no
  2880 = |Aut(W)|/18 = 51840/18

NEW substrate identity: #ovoids = q! * 2|E| = q! * vk = mu * (q!)!

  (Actually q! * vk = 6 * 480 = 2880 ✓)
  (Also 2880 = mu * (q!)! = 4 * 720 ✓)

So #ovoids = q! * 2|E| = mu * (q!)! -- doubly substrate-clean!

==============================================================
"""
from __future__ import annotations

import json
from itertools import product
from pathlib import Path
import math

import numpy as np


def construct_W33():
    nonzero = [t for t in product(range(3), repeat=4) if any(t)]
    def canon(v):
        idx = next(i for i, x in enumerate(v) if x != 0)
        scalar = pow(v[idx], -1, 3)
        return tuple((scalar * x) % 3 for x in v)
    cs = sorted({canon(v) for v in nonzero})
    n = len(cs)
    def om(u, v):
        return (u[0]*v[2] - u[2]*v[0] + u[1]*v[3] - u[3]*v[1]) % 3
    A = np.zeros((n, n), dtype=int)
    for i, u in enumerate(cs):
        for j, v in enumerate(cs):
            if i != j and om(u, v) == 0:
                A[i, j] = 1
    return cs, A


def find_indep_sets_size_7(A):
    n = A.shape[0]
    results = []
    def search(current, candidates):
        if len(current) == 7:
            results.append(current.copy())
            return
        if not candidates or len(current) + len(candidates) < 7:
            return
        for i, v in enumerate(candidates):
            new_cand = [u for u in candidates[i+1:] if A[v, u] == 0]
            search(current + [v], new_cand)
    search([], list(range(n)))
    return results


def search_6_coloring(A, ovoids):
    n = A.shape[0]
    ALL = (1 << n) - 1
    masks = [sum(1 << v for v in o) for o in ovoids]

    found = [None]

    def search(chosen, chosen_mask, start):
        if found[0]:
            return
        if len(chosen) == 5:
            rem_mask = ALL & ~chosen_mask
            rem = [v for v in range(n) if rem_mask & (1 << v)]
            # Check if rem is independent
            for i in range(len(rem)):
                for j in range(i + 1, len(rem)):
                    if A[rem[i], rem[j]]:
                        return  # not indep
            found[0] = (chosen, rem)
            return
        for i in range(start, len(masks)):
            if chosen_mask & masks[i] == 0:
                search(chosen + [i], chosen_mask | masks[i], i + 1)
                if found[0]:
                    return

    search([], 0, 0)
    return found[0]


def main():
    q = 3
    lambda_, mu = 2, 4
    F5 = 5
    phi3, phi4, phi6 = 13, 10, 7
    k, v, E_count = 12, 40, 240

    print("=" * 78)
    print("W(3,3) chi = q! EXACTLY (BREAKTHROUGH 13)")
    print("=" * 78)
    print()

    vertices, A = construct_W33()
    n = A.shape[0]
    print(f"Built W(3,3): |V| = {n}, |E| = {A.sum() // 2}")

    # Lower bound: chi >= ceil(v/alpha)
    alpha = phi6  # from BT12
    lower_bound = math.ceil(v / alpha)
    print(f"\nLOWER BOUND: chi >= ceil(v/alpha) = ceil({v}/{alpha}) = {lower_bound} = q!")
    assert lower_bound == math.factorial(q)

    # Enumerate ovoids
    print("\nEnumerating all max ovoids (size 7)...")
    ovoids = find_indep_sets_size_7(A)
    n_ovoids = len(ovoids)
    print(f"Total ovoids: {n_ovoids}")

    # Substrate factorization of ovoid count
    assert n_ovoids == math.factorial(q) * 2 * E_count == 6 * 480
    assert n_ovoids == mu * math.factorial(math.factorial(q))  # 4 * 720
    print(f"  Factorization: {n_ovoids} = q! * 2|E| = mu * (q!)!")

    # Find a 6-coloring
    print("\nUPPER BOUND: searching for explicit 6-coloring...")
    result = search_6_coloring(A, ovoids)
    if result is None:
        print("NO 6-COLORING FOUND -- chi(W) > 6!")
        return
    chosen_idx, rem = result
    print(f"SUCCESS: found 6-coloring with classes")
    for i, idx in enumerate(chosen_idx):
        print(f"  Color {i + 1} (size 7): {ovoids[idx]}")
    print(f"  Color 6 (size {len(rem)}): {rem}")

    sizes = [7]*5 + [len(rem)]
    assert sum(sizes) == v
    print(f"\nClass size signature: {sizes}")
    print(f"Sum check: {sum(sizes)} = v = {v} ✓".replace("✓", "OK"))

    # The exact identity
    print()
    print("=" * 78)
    print("THE EXACT CHROMATIC IDENTITY")
    print("=" * 78)
    print(f"""
  chi(W(3,3)) = q! = 6 EXACTLY.

  Proved by:
    Lower bound: ceil(v/alpha) = ceil(40/7) = 6
    Upper bound: explicit 6-coloring constructed
    Therefore chi = 6.

  Substrate identity:
    v = 5*Phi_6 + F_5 = F_5*(Phi_6 + 1) = F_5 * 2^q
    = 5 * 8 = 40

  Class-size signature (7, 7, 7, 7, 7, 5):
    = 5 = F_5 ovoids of size Phi_6
    + 1 remainder set of size F_5

  Number of ovoids = q! * 2|E| = mu * (q!)! = 2880 (substrate-clean!)

THE SUBSTRATE'S CHROMATIC NUMBER EQUALS THE MASTER EQUATION VALUE q!.

This is the cleanest known substrate-combinatorial identity:
  chi(W(3,3)) = q! = 2q (master equation value)
""")
    out = Path("data") / "w33_BREAKTHROUGH_chi_equals_q_factorial.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps({
        "chi_W33": 6,
        "chi_substrate": "q! = master equation value",
        "lower_bound": lower_bound,
        "lower_bound_form": "ceil(v/alpha) = ceil(40/Phi_6)",
        "n_ovoids": n_ovoids,
        "n_ovoids_form": "q! * 2|E| = mu * (q!)!",
        "explicit_6_coloring_class_sizes": sizes,
        "class_sizes_substrate": "5*Phi_6 + F_5 = F_5*(Phi_6 + 1) = F_5 * 2^q = 40 = v",
        "exact_proof": (
            "Lower bound from fractional chromatic: chi >= ceil(v/alpha) = 6. "
            "Upper bound by explicit construction: 5 disjoint size-Phi_6 ovoids "
            "+ 1 size-F_5 remainder = 6-coloring. Therefore chi = 6 = q!."
        ),
        "first_6_coloring": {
            f"class_{i+1}": ovoids[idx] for i, idx in enumerate(chosen_idx)
        } | {"class_6_remainder": rem},
    }, indent=2, default=str), encoding="utf-8")
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
