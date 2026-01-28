#!/usr/bin/env sage
"""Check conjugacy between PSp(4,3) edge action and W(E6) even action on roots.

Uses GAP to attempt conjugating permutation in Sym(240).
"""
from __future__ import annotations

import json
from sage.all import Permutation, PermutationGroup
from sage.interfaces.gap import gap


def to_perm_group(perms):
    return PermutationGroup([Permutation(p) for p in perms])


def to_gap_group(perms):
    # perms are 1-based lists
    gap_perms = [gap.PermList(p) for p in perms]
    return gap.Group(gap_perms)


def main():
    edge = json.loads(open('artifacts/sp43_edge_generators.json').read())
    we6 = json.loads(open('artifacts/we6_true_action.json').read())

    edge_gens = [[x + 1 for x in p] for p in edge['generators']]  # to 1-based
    we6_even = we6['we6_even_generators']

    G1 = to_perm_group(edge_gens)
    G2 = to_perm_group(we6_even)

    print(f"G1 order: {G1.order()}")
    print(f"G2 order: {G2.order()}")

    # GAP conjugacy
    GG1 = to_gap_group(edge_gens)
    GG2 = to_gap_group(we6_even)
    Sn = gap.SymmetricGroup(240)

    is_conj = gap.IsConjugate(Sn, GG1, GG2)
    print(f"IsConjugate: {is_conj}")
    conj = None
    if is_conj == True:
        conj = gap.ConjugatingElement(Sn, GG1, GG2)
        print("Found conjugating element")
        # export permutation
        perm_list = list(conj)
        with open('artifacts/edge_we6_conjugating_perm.json', 'w') as f:
            json.dump({"perm": perm_list}, f)
        print("Wrote artifacts/edge_we6_conjugating_perm.json")

    out = {
        "g1_order": int(G1.order()),
        "g2_order": int(G2.order()),
        "is_conjugate": bool(is_conj),
    }
    with open('artifacts/edge_we6_conjugacy.json', 'w') as f:
        json.dump(out, f, indent=2)
    print("Wrote artifacts/edge_we6_conjugacy.json")


if __name__ == '__main__':
    main()
