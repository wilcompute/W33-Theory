#!/usr/bin/env sage
"""Sample Weyl(E8) elements, conjugate simple roots, and test for E6 Cartan patterns.
Writes PART_CVII_e6_weyl_samples.json if embeddings are found (or empty list otherwise).
"""
from sage.all_cmdline import *
import json
from pathlib import Path
from itertools import combinations, permutations

E8 = RootSystem(['E',8])
W = E8.weyl_group()
RL = E8.root_lattice()
# simple roots as vectors
simple = RL.simple_roots()
simple_list = [simple[i] for i in sorted(simple.keys())]
# target cartan
E6 = RootSystem(['E',6])
E6_C = E6.cartan_matrix()
E6_det = E6_C.determinant()

print('Weyl group order:', W.order())

found = []
trials = 1000
for t in range(trials):
    g = W.random_element()
    # conjugate simple roots
    conj = [g.action(v) for v in simple_list]
    # try all 6-subsets
    for subset_idxs in combinations(range(len(conj)), 6):
        subset = [conj[i] for i in subset_idxs]
        # build cartan matrix
        M = matrix(QQ, 6, 6)
        ok = True
        for i in range(6):
            for j in range(6):
                M[i,j] = 2 * (subset[i].dot_product(subset[j])) / (subset[i].dot_product(subset[i]))
        # determinant quick check
        if M.determinant() != E6_det:
            continue
        # check permutation equivalence
        eq = False
        for p in permutations(range(6)):
            P = permutation_matrix(QQ, list(p))
            Mp = P * M * P.inverse()
            if Mp == E6_C:
                eq = True
                perm = list(p)
                break
        if eq:
            print('Found E6 embedding at trial', t, 'subset', subset_idxs)
            found.append({'trial': t, 'subset_idxs': subset_idxs, 'perm': perm})
            Path('PART_CVII_e6_weyl_samples.json').write_text(json.dumps(found, indent=2))
            raise SystemExit(0)

# none found
Path('PART_CVII_e6_weyl_samples.json').write_text(json.dumps(found, indent=2))
print('Finished sampling; found count=', len(found))
