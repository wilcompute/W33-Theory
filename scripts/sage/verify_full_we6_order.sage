#!/usr/bin/env sage
from sage.libs.gap.libgap import libgap
import json
from pathlib import Path

ROOT = Path('.')
path = ROOT / 'artifacts' / 'sp43_we6_generator_map_full_we6.json'
if not path.exists():
    print('Missing', path)
    exit(1)

data = json.loads(path.read_text())
perms = data['generators']

# Convert to GAP permutations (1-based) and check validity
valid = True
for perm in perms:
    n = len(perm)
    if sorted(perm) != list(range(n)):
        valid = False
        break

if not valid:
    print('Invalid permutation detected')
    exit(1)

# Only attempt order computation if all perms valid
try:
    gap_perms = [libgap.PermList([x + 1 for x in perm]) for perm in perms]
    G = libgap.Group(gap_perms)
    order = int(libgap.Order(G))
except Exception as e:
    order = None
    err = str(e)
else:
    err = None

out = {
    'order': order,
    'error': err,
}

out_path = ROOT / 'artifacts' / 'sp43_we6_generator_map_full_we6_verify.json'
out_path.write_text(json.dumps(out, indent=2))
print('Order:', order)
print('Error:', err)
print('Wrote', out_path)
