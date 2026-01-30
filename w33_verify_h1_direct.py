#!/usr/bin/env sage
"""
Verify H1 action matrices are a valid representation by recomputing directly.
"""

import json
import numpy as np
from sage.all import *

# Load the JSON data
json_path = 'claude_workspace/data/w33_sage_incidence_h1.json'
with open(json_path, 'r') as f:
    data = json.load(f)

print("=== Recompute H1 Action to Verify ===\n")

# Load W33 lines from the data source
from lib.w33_io import W33DataPaths, load_w33_lines, simplices_from_lines
from pathlib import Path

here = Path('.').resolve()
sys.path.insert(0, str(here / 'claude_workspace'))

paths = W33DataPaths.from_this_file(str(here / 'claude_workspace' / 'w33_sage_incidence_and_h1.py'))
lines = load_w33_lines(paths)

# Build incidence graph
edges_list = []
for line_index, pts in enumerate(lines):
    line_vertex = 41 + line_index
    for p in pts:
        edges_list.append((p + 1, line_vertex))

G = Graph(multiedges=False, loops=False)
G.add_vertices(range(1, 81))
G.add_edges(edges_list)

# Get automorphism group
A = G.automorphism_group(partition=[list(range(1, 41)), list(range(41, 81))])
gens = list(A.gens())

print(f"Group order: {A.order()}")
print(f"Number of generators: {len(gens)}")

# Build simplicial complex
simplices = simplices_from_lines(lines)
vertices = simplices[0]
edges1 = simplices[1]
tris2 = simplices[2]

n1 = len(edges1)
field = QQ

# Boundary matrices
from lib.simplicial_homology import faces

def boundary_matrix_exact(k_simplices, km1_simplices):
    idx = {s: i for i, s in enumerate(km1_simplices)}
    m = len(km1_simplices)
    n = len(k_simplices)
    M = [[0] * n for _ in range(m)]
    for j, s in enumerate(k_simplices):
        for sign, f in faces(s):
            i = idx.get(f)
            if i is None:
                continue
            M[i][j] += sign
    return M

d1 = matrix(field, boundary_matrix_exact(edges1, vertices))
d2 = matrix(field, boundary_matrix_exact(tris2, edges1))

V = VectorSpace(field, n1)
Z1 = d1.right_kernel()
B1 = d2.column_space()

beta1 = int(Z1.dimension() - B1.dimension())
print(f"H1 dim: {beta1}")

# Build H1 basis
B_basis = list(B1.basis())
Z_basis = list(Z1.basis())

span = V.subspace(B_basis)
H_basis = []
for v in Z_basis:
    if v not in span:
        H_basis.append(v)
        span = V.subspace(list(span.basis()) + [v])
    if len(H_basis) == beta1:
        break

# Z1 basis matrix
Z_cols = [*B_basis, *H_basis]
M = matrix(field, [list(v) for v in Z_cols]).transpose()

edge_index = {e: i for i, e in enumerate(edges1)}

def gen_point_perm(gen):
    return [int(gen(i + 1)) - 1 for i in range(40)]

def edge_action_maps(point_perm):
    idx_map = [0] * n1
    sgn_map = [0] * n1
    for i, (a, b) in enumerate(edges1):
        ua = point_perm[a]
        ub = point_perm[b]
        if ua < ub:
            idx_map[i] = edge_index[(ua, ub)]
            sgn_map[i] = 1
        else:
            idx_map[i] = edge_index[(ub, ua)]
            sgn_map[i] = -1
    return idx_map, sgn_map

def apply_edge_action(v, idx_map, sgn_map):
    w_list = [field(0)] * n1
    for i in range(n1):
        c = v[i]
        if c == 0:
            continue
        j = idx_map[i]
        w_list[j] += c * field(sgn_map[i])
    return V(w_list)

def compute_h1_matrix(g):
    """Compute the H1 action matrix for group element g."""
    perm = gen_point_perm(g)
    idx_map, sgn_map = edge_action_maps(perm)
    
    Acols = []
    for basis_vec in H_basis:
        w = apply_edge_action(basis_vec, idx_map, sgn_map)
        coeffs = M.solve_right(w)
        h_coords = coeffs[len(B_basis):]
        Acols.append(list(h_coords))
    
    Ah = matrix(field, Acols).transpose()
    return np.array(Ah, dtype=float)

# Compute H1 matrices for generators
h1_gen_matrices = []
for i, g in enumerate(gens):
    mat = compute_h1_matrix(g)
    h1_gen_matrices.append(mat)
    tr = np.trace(mat)
    print(f"Generator {i}: order={g.order()}, trace={tr:.1f}")

# Compare with JSON matrices
json_matrices = []
for mat_data in data['h1_action']['generator_matrices']:
    mat = np.array([[float(x) for x in row] for row in mat_data], dtype=float)
    json_matrices.append(mat)

print("\n--- Comparing recomputed vs JSON matrices ---")
for i in range(len(gens)):
    match = np.allclose(h1_gen_matrices[i], json_matrices[i])
    print(f"Generator {i}: {'MATCH' if match else 'DIFFER'}")

# Test homomorphism property with recomputed matrices
print("\n--- Testing homomorphism property (recomputed) ---")

import random
random.seed(42)

for trial in range(5):
    # Generate random group elements
    g1 = A.identity()
    g2 = A.identity()
    for _ in range(3):
        g1 = g1 * gens[random.randint(0, len(gens)-1)]
        g2 = g2 * gens[random.randint(0, len(gens)-1)]
    g12 = g1 * g2
    
    mat1 = compute_h1_matrix(g1)
    mat2 = compute_h1_matrix(g2)
    mat12 = compute_h1_matrix(g12)
    
    product = mat1 @ mat2
    
    match = np.allclose(product, mat12)
    print(f"  Trial {trial}: ρ(g1*g2) = ρ(g1)ρ(g2)? {match}")
    if not match:
        print(f"    Max diff: {np.max(np.abs(product - mat12)):.4f}")

# If homomorphism passes, compute character
print("\n--- Computing H1 character ---")

gap_G = libgap(A)
char_table = gap_G.CharacterTable()
gap_classes = char_table.ConjugacyClasses()
n_classes = len(gap_classes)
class_sizes = [int(libgap.Size(c)) for c in gap_classes]

h1_chi = []
for c_idx in range(n_classes):
    gap_class = gap_classes[c_idx]
    rep_gap = gap_class.Representative()
    
    # Convert to Sage element
    perm_list = list(rep_gap.ListPerm())
    if not perm_list:
        perm_list = list(range(1, 81))
    while len(perm_list) < 80:
        perm_list.append(len(perm_list) + 1)
    
    sage_perm = SymmetricGroup(80)(perm_list)
    g = A(sage_perm)
    
    mat = compute_h1_matrix(g)
    trace = np.trace(mat)
    h1_chi.append(round(trace))
    
    order_elem = int(libgap.Order(rep_gap))
    print(f"  Class {c_idx}: size={class_sizes[c_idx]:5}, order={order_elem:2}, chi={h1_chi[-1]}")

# Compute <chi, chi>
group_order = int(A.order())
chi_squared = sum(class_sizes[j] * h1_chi[j]**2 for j in range(n_classes)) / group_order
print(f"\n<chi_H1, chi_H1> = {chi_squared}")

if chi_squared >= 0.999:
    print("✓ Valid character!")
else:
    print("✗ Issue with character (should be >= 1)")
