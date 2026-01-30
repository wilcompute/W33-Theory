#!/usr/bin/env sage
"""Compute true W(E6) action on E8 roots and export generator permutations.

Also attempts to build the even subgroup (order 25920) and export its generators.
"""

from __future__ import annotations

import json

from sage.all import Permutation, PermutationGroup, RootSystem, WeylGroup


def vec_key_exact(v):
    try:
        return tuple(v.to_vector())
    except Exception:
        return tuple(v)


def vec_key_int2(v):
    try:
        coords = list(v.to_vector())
    except Exception:
        coords = list(v)
    return [int(2 * x) for x in coords]


def main():
    R8 = RootSystem(["E", 8]).ambient_space()
    roots = list(R8.roots())
    root_keys = [vec_key_exact(r) for r in roots]
    if len(root_keys) != len(set(root_keys)):
        raise RuntimeError("Duplicate root keys detected")
    root_to_idx = {k: i for i, k in enumerate(root_keys)}

    W8 = WeylGroup(["E", 8])
    s = W8.simple_reflections()

    subset = [1, 2, 3, 4, 5, 6]
    gens = [s[i] for i in subset]
    WE6 = W8.subgroup(gens)
    print(f"W(E6) order: {WE6.order()}")

    # Generator perms on E8 roots
    gen_perms = []
    for g in gens:
        perm = []
        for r in roots:
            img = g.action(r)
            perm.append(root_to_idx[vec_key_exact(img)] + 1)  # 1-based
        if len(set(perm)) != len(perm):
            raise RuntimeError("Generator perm not bijective")
        gen_perms.append(perm)

    # Build WE6 permutation group
    WE6_perm = PermutationGroup([Permutation(p) for p in gen_perms])
    print(f"WE6_perm order: {WE6_perm.order()}")

    # Attempt even subgroup by generators as pair products
    even_gens = []
    for i in range(len(gens)):
        for j in range(i + 1, len(gens)):
            even_gens.append(gens[i] * gens[j])
    even_perms = []
    for g in even_gens:
        perm = []
        for r in roots:
            img = g.action(r)
            perm.append(root_to_idx[vec_key_exact(img)] + 1)
        if len(set(perm)) != len(perm):
            raise RuntimeError("Even generator perm not bijective")
        even_perms.append(perm)

    WE6_even = PermutationGroup([Permutation(p) for p in even_perms])
    print(f"WE6_even order: {WE6_even.order()}")

    out = {
        "roots_int2": [vec_key_int2(r) for r in roots],
        "we6_generators": gen_perms,
        "we6_order": int(WE6_perm.order()),
        "we6_even_generators": even_perms,
        "we6_even_order": int(WE6_even.order()),
        "subset": subset,
    }

    with open("artifacts/we6_true_action.json", "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2, default=str)

    print("Wrote artifacts/we6_true_action.json")


if __name__ == "__main__":
    main()
