#!/usr/bin/env sage
"""Find E6 subsystems inside E8 and produce diagnostics to attempt embedding Aut(W33) into W(E8).
Write PART_CVII_e6_in_e8_probe.json with candidate subsystems.
"""
from sage.all_cmdline import *
import json
from pathlib import Path

E8 = RootSystem(['E',8])
RL = E8.root_lattice()
roots = list(RL.roots())
num_roots = len(roots)
print('E8 roots:', num_roots)

# get simple roots of E8 in ambient coordinates
try:
    simple = RL.simple_roots()
except Exception:
    # alternative approach via ambient
    R = E8.ambient_space()
    # Using standard simple roots from Cartan type maybe accessible via E8.simple_root_system()
    simple = RL.simple_roots()

simple_list = [v for k,v in sorted(simple.items())]

# function to compute Cartan matrix between basis vectors
def cartan_matrix(vecs):
    m = matrix(QQ, len(vecs))
    for i,v in enumerate(vecs):
        for j,w in enumerate(vecs):
            m[i,j] = 2 * (v.dot_product(w)) / (v.dot_product(v))
    return m

# Known Cartan matrix for E6
E6 = RootSystem(['E',6])
E6_C = E6.cartan_matrix()

candidates = []
# search subsets of 6 simple roots among the 8 simple roots that form E6 subdiagram (choose 6 out of 8 = 28 tests)
from itertools import combinations
for idxs in combinations(range(len(simple_list)), 6):
    subset = [simple_list[i] for i in idxs]
    try:
        C = cartan_matrix(subset)
        # compare to E6 cartan up to permutation
        if C.is_symmetric() and sorted(list(C.nrows())):
            # check if isomorphic to E6 Cartan by eigenvalues or determinant
            if C.determinant() == E6_C.determinant():
                candidates.append({'idxs': idxs, 'det': int(C.determinant())})
    except Exception:
        pass

out = {
    'num_roots': num_roots,
    'num_candidates': len(candidates),
    'candidates': candidates[:10]
}
Path('PART_CVII_e6_in_e8_probe.json').write_text(json.dumps(out, indent=2))
print('Wrote PART_CVII_e6_in_e8_probe.json')
print(json.dumps(out, indent=2))
