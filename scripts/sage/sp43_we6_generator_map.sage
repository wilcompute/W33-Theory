#!/usr/bin/env sage
from sage.all import *
from sage.libs.gap.libgap import libgap
import json
from pathlib import Path

ROOT = Path('.')

# Build Sp(4,3) as permutation group on 80 nonzero vectors of F3^4
F = GF(3)

vectors = []
for a in F:
    for b in F:
        for c in F:
            for d in F:
                if a == 0 and b == 0 and c == 0 and d == 0:
                    continue
                vectors.append((a, b, c, d))

vec_to_idx = {v: i for i, v in enumerate(vectors)}

# Symplectic form matrix
Omega = matrix(F, [[0,0,1,0],[0,0,0,1],[-1,0,0,0],[0,-1,0,0]])

G = Sp(4, F)

# Our chosen generators (same as tools/explicit_coset_bijection.py)
raw_mats = [
    [[1,0,1,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]],
    [[1,0,0,0],[0,1,0,1],[0,0,1,0],[0,0,0,1]],
    [[1,0,0,0],[0,1,0,0],[1,0,1,0],[0,0,0,1]],
    [[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,1,0,1]],
    [[1,1,0,0],[0,1,0,0],[0,0,1,0],[0,0,-1,1]],
    [[1,0,0,0],[1,1,0,0],[0,0,1,-1],[0,0,0,1]],
    [[0,0,1,0],[0,1,0,0],[-1,0,0,0],[0,0,0,1]],
    [[1,0,0,0],[0,0,0,1],[0,0,1,0],[0,-1,0,0]],
    [[-1,0,0,0],[0,1,0,0],[0,0,-1,0],[0,0,0,1]],
    [[1,0,0,0],[0,-1,0,0],[0,0,1,0],[0,0,0,-1]],
]

mats = [matrix(F, M) for M in raw_mats]

# Verify they are symplectic
valid = []
for M in mats:
    if M.transpose() * Omega * M == Omega:
        valid.append(M)

# Build permutations on 80 nonzero vectors
perms = []
for M in valid:
    perm = [None]*len(vectors)
    for i, v in enumerate(vectors):
        vnew = tuple((M * vector(F, v)).list())
        perm[i] = vec_to_idx[vnew] + 1  # Sage permutations are 1-based
    perms.append(Permutation(perm))

Gperm = PermutationGroup(perms)
print("Sp(4,3) perm order:", Gperm.order())

# Weyl group W(E6) as permutation group
H = WeylGroup(['E',6], implementation='permutation')
Hs = H.simple_reflections()
H_perm = PermutationGroup([Hs[i] for i in sorted(Hs.keys())])
print("W(E6) order:", H_perm.order())

# Find isomorphism via GAP
gap_G = libgap(Gperm)
gap_H = libgap(H_perm)
gap_iso = libgap.IsomorphismGroups(gap_G, gap_H)
if gap_iso == libgap.fail:
    print("GAP could not find isomorphism")
    out_path = Path('artifacts') / 'sp43_we6_generator_map_sage.json'
    out = {
        "sp43_order": int(Gperm.order()),
        "we6_order": int(H_perm.order()),
        "status": "isomorphism_failed",
    }
    out_path.write_text(json.dumps(out, indent=2))
    print("Wrote", out_path)
    exit(0)
print("GAP iso:", gap_iso)

# Map generators
mapping = []
for idx, g in enumerate(perms):
    g_gap = libgap(g)
    h_gap = gap_iso.Image(g_gap)
    # Convert GAP permutation back to Sage permutation in H
    try:
        h = H_perm(h_gap)  # coerce into H_perm
        try:
            rw = h.reduced_word()
        except Exception:
            rw = None
        mapping.append({
            "gen_index": idx,
            "reduced_word": rw,
            "perm": list(h)
        })
    except Exception as e:
        mapping.append({"gen_index": idx, "error": str(e)})

out = {
    "sp43_order": int(Gperm.order()),
    "we6_order": int(H.order()),
    "generator_map": mapping,
}

out_path = Path('artifacts') / 'sp43_we6_generator_map.json'
out_path.write_text(json.dumps(out, indent=2))
print("Wrote", out_path)
