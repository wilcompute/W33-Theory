#!/usr/bin/env sage
"""
Extract explicit E6 simple root sets from the 72-root orthogonal complement in E8 using random linear functionals, and compute Cartan matrices for each.
"""
from sage.all_cmdline import *
import json
from pathlib import Path
import random

data = json.loads(Path('PART_CVII_e6_via_A2.json').read_text())
orth = data[0]['orth_indices']

E8 = RootSystem(['E',8])
RL = E8.root_lattice()
roots = list(RL.roots())
orth_roots = [roots[i] for i in orth]

results = []
for trial in range(20):
    coeffs = [ZZ.random_element(1,20) for _ in range(8)]
    v = vector(coeffs)
    positives = [r for r in north_roots if r.dot_product(v) > 0]
    pos_set = set(tuple(r) for r in positives)
    indecomp = []
    for r in positives:
        can = False
        for a in positives:
            if a == r:
                continue
            b = r - a
            if tuple(b) in pos_set:
                can = True
                break
        if not can:
            indecomp.append(r)
    if len(indecomp) == 6:
        M = matrix(6,6)
        for i in range(6):
            for j in range(6):
                M[i,j] = 2 * indecomp[i].dot_product(indecomp[j]) / indecomp[i].dot_product(indecomp[i])
        results.append({'trial': trial, 'coeffs': list(coeffs), 'indecomp_cartan': [[int(x) for x in row] for row in M.rows()]})
        print(f'Trial {trial}: Found indecomp=6, Cartan matrix:')
        print(M)
    else:
        print(f'Trial {trial}: indecomp={len(indecomp)}')
Path('PART_CVII_e6_indec_simple_trials_sage.json').write_text(json.dumps(results, indent=2))
print('Wrote PART_CVII_e6_indec_simple_trials_sage.json')
