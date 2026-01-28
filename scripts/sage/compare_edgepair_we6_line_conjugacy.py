#!/usr/bin/env sage
"""Check conjugacy between PSp(4,3) edge-pair action and true W(E6) even action on root lines."""
from __future__ import annotations

import json
from sage.all import Permutation, PermutationGroup
from sage.interfaces.gap import gap


def to_gap_group(perms):
    gap_perms = [gap.PermList(p) for p in perms]
    return gap.Group(gap_perms)


def main():
    edgepair = json.loads(open('artifacts/sp43_edgepair_generators.json').read())
    we6 = json.loads(open('artifacts/we6_true_action.json').read())

    edge_gens = [[x + 1 for x in p] for p in edgepair['pair_generators']]  # 1-based

    # Build WE6 even action on root lines
    roots = [tuple(r) for r in we6['roots_int2']]
    root_to_idx = {r: i for i, r in enumerate(roots)}
    line_id = [-1] * len(roots)
    line_reps = []
    for i, r in enumerate(roots):
        if line_id[i] != -1:
            continue
        j = root_to_idx[tuple(-x for x in r)]
        lid = len(line_reps)
        line_id[i] = lid
        line_id[j] = lid
        rep = i if i < j else j
        line_reps.append(rep)

    gens = we6['we6_even_generators']
    line_perms = []
    for g in gens:
        # g is 1-based root perm
        perm = [0] * len(line_reps)
        for lid, rep in enumerate(line_reps):
            img = g[rep] - 1
            lid2 = line_id[img]
            perm[lid] = lid2 + 1
        line_perms.append(perm)

    # Build permutation groups
    G1 = PermutationGroup([Permutation(p) for p in edge_gens])
    G2 = PermutationGroup([Permutation(p) for p in line_perms])

    print(f"G1 order: {G1.order()}")
    print(f"G2 order: {G2.order()}")

    GG1 = to_gap_group(edge_gens)
    GG2 = to_gap_group(line_perms)
    Sn = gap.SymmetricGroup(120)

    is_conj = gap.IsConjugate(Sn, GG1, GG2)
    print(f"IsConjugate: {is_conj}")

    conj_perm = None
    if is_conj == True:
        conj = gap.ConjugatingElement(Sn, GG1, GG2)
        conj_perm = list(conj)
        with open('artifacts/edgepair_we6line_conjugating_perm.json', 'w') as f:
            json.dump({"perm": conj_perm}, f)
        print("Wrote artifacts/edgepair_we6line_conjugating_perm.json")

    out = {
        "g1_order": int(G1.order()),
        "g2_order": int(G2.order()),
        "is_conjugate": bool(is_conj),
    }
    with open('artifacts/edgepair_we6line_conjugacy.json', 'w') as f:
        json.dump(out, f, indent=2)
    print("Wrote artifacts/edgepair_we6line_conjugacy.json")


if __name__ == '__main__':
    main()
