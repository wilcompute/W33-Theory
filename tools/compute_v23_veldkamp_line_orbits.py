import json
from pathlib import Path
from collections import deque

repo = Path.cwd()
ext_json = repo / 'bundles' / 'v23_toe_finish' / 'v23' / 'veld_summary_extended.json'
tri_csv = repo / 'bundles' / 'v23_toe_finish' / 'v23' / 'Q_triangles_with_centers_Z2_S3_fiber6.csv'
out_json = repo / 'bundles' / 'v23_toe_finish' / 'v23' / 'veldkamp_line_orbits.json'

# Make repo importable and load hyperplane generators from triangles using existing code
import sys
sys.path.insert(0, str(repo))
from src.finite_geometry.veldmap import load_triangles, neighborhoods_from_triangles, point_hyperplanes

triangles = list(load_triangles(tri_csv))
neighborhoods = neighborhoods_from_triangles(triangles)
gens_map = point_hyperplanes(neighborhoods)
# index generators deterministically by sorted point index
gens_items = sorted(gens_map.items(), key=lambda x: x[0])  # (point_label, frozenset)
# canonical ordering of point labels (original labels in the universe)
points_sorted = sorted(set().union(*(s for _, s in gens_items)))
# gens as sets of original labels
gens_labels = [s for _, s in gens_items]
index_of = {g: i for i, g in enumerate(gens_labels)}
# number of generators
n_generators = len(gens_labels)
# sanity about expected number of generators
if n_generators != 45:
    print('Warning: expected 45 generators, found', n_generators)

# enumerate Veldkamp lines: triples {i,j,k} with k = index(A xor B) where A,B are label-sets
lines = set()
for i in range(n_generators):
    for j in range(i + 1, n_generators):
        sd = frozenset(gens_labels[i].symmetric_difference(gens_labels[j]))
        k = index_of.get(sd)
        if k is not None:
            triple = tuple(sorted((i, j, k)))
            lines.add(triple)

lines = sorted(lines)

# Load point/vertex permutations from extended JSON
with open(ext_json, 'r', encoding='utf8') as f:
    ext = json.load(f)
perm90_samples = ext['automorphism']['generators_sample']
# Determine universe size (max label + 1)
universe_size = max(points_sorted) + 1
# build full-label permutations (0..universe_size-1 -> 0..universe_size-1)
label_perms = []
for perm90 in perm90_samples:
    # accept full 90-element permutations (actions on the entire universe)
    label_perms.append(tuple(perm90))

# helper to canonicalize a triple of sets as tuple of sorted tuples
def canonical_triple(A, B, C):
    t = [tuple(sorted(A)), tuple(sorted(B)), tuple(sorted(C))]
    t_sorted = tuple(sorted(t))
    return t_sorted

# Build lines as triples of frozensets (A,B,A^B) using label-sets
lines_sets = []
for i in range(n_generators):
    for j in range(i + 1, n_generators):
        A = gens_labels[i]
        B = gens_labels[j]
        C = frozenset(A.symmetric_difference(B))
        lines_sets.append(canonical_triple(A, B, C))

# Use generator action on labels to compute orbits
unseen = set(lines_sets)
orbits = []
while unseen:
    seed = unseen.pop()
    orbit = {seed}
    dq = deque([seed])
    while dq:
        cur = dq.popleft()
        # cur is tuple of three tuples of sorted labels
        cur_sets = [set(t) for t in cur]
        for p in label_perms:
            # apply label permutation p to each set
            try:
                nxt_sets = [frozenset([p[q] for q in s]) for s in cur_sets]
            except IndexError as e:
                print('IndexError applying permutation:')
                print('perm length', len(p))
                print('perm sample', p[:10])
                print('current triple (as sets)', cur_sets)
                # find offending q
                for s in cur_sets:
                    for q in s:
                        try:
                            _ = p[q]
                        except Exception as e2:
                            print('offending q', q)
                            raise
                raise
            nxt = canonical_triple(*nxt_sets)
            if nxt not in orbit:
                orbit.add(nxt)
                dq.append(nxt)
    unseen -= orbit
    orbits.append({'rep': tuple(orbit)[0], 'size': len(orbit)})

orbits = sorted(orbits, key=lambda o: (-o['size'], o['rep']))

res = {'n_lines': len(lines), 'n_orbits': len(orbits), 'orbits': orbits}
with open(out_json, 'w', encoding='utf8') as f:
    json.dump(res, f, indent=2, default=str)
print('Wrote', out_json)
