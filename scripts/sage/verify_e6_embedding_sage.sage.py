#!/usr/bin/env sage
"""Verify the E6 subsystem found by checking which E8 roots lie in integer span of the chosen simple roots (exact arithmetic).
Writes PART_CVII_e6_in_e8_sage_verify.json with results.
"""
from sage.all_cmdline import *
import json
from pathlib import Path

# load backtrack result
info = json.loads(Path('PART_CVII_e6_in_e8_backtrack.json').read_text())
if not info:
    print('No backtrack solution found')
    raise SystemExit(1)
nodes = info[0]['nodes']
print('Nodes:', nodes)

E8 = RootSystem(['E',8])
RL = E8.root_lattice()
roots = list(RL.roots())
# Convert roots to vectors over QQ
root_vecs = [v for v in roots]

# selected simple roots (as elements of ambient lattice)
simples = [root_vecs[i] for i in nodes]
# form matrix with simples as rows
M = matrix(QQ, [[c for c in v] for v in simples])
print('M shape', M.nrows(), M.ncols())

in_span = []
for i, r in enumerate(root_vecs):
    # Solve M^T * x = r as rational system for x coefficients in QQ
    # We want r = sum_i x_i * simple_i, so M^T * x = r_vector
    rvec = vector(QQ, list(r))
    try:
        # Solve via M.transpose() * x = rvec
        x = M.transpose().solve_right(rvec)
        # check integer coefficients
        if all(c in ZZ for c in x):
            in_span.append({'index': i, 'coeffs': [int(ci) for ci in x]})
    except Exception:
        continue

print('Number of E8 roots in span:', len(in_span))
# Save
out = {'nodes': nodes, 'in_span_count': len(in_span), 'in_span_indices': [e['index'] for e in in_span][:200]}
Path('PART_CVII_e6_in_e8_sage_verify.json').write_text(json.dumps(out, indent=2))
print('Wrote PART_CVII_e6_in_e8_sage_verify.json')
print(json.dumps(out, indent=2))
