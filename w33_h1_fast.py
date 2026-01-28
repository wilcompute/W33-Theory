#!/usr/bin/env sage
"""
Compute H1 character with numpy for speed.
"""

import json
import sys
from pathlib import Path

import numpy as np
from sage.all import *

print("=== Fast H1 Character Computation ===\n")

# Load W33 lines
here = Path(".").resolve()
sys.path.insert(0, str(here / "claude_workspace"))

from lib.simplicial_homology import faces
from lib.w33_io import W33DataPaths, load_w33_lines, simplices_from_lines

paths = W33DataPaths.from_this_file(
    str(here / "claude_workspace" / "w33_sage_incidence_and_h1.py")
)
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

A = G.automorphism_group(partition=[list(range(1, 41)), list(range(41, 81))])
gens = list(A.gens())

group_order = int(A.order())
print(f"Group order: {group_order}")
print(f"Number of generators: {len(gens)}")

# Build simplicial complex
simplices = simplices_from_lines(lines)
vertices = simplices[0]
edges1 = simplices[1]
tris2 = simplices[2]

n0 = len(vertices)
n1 = len(edges1)
n2 = len(tris2)

# Build boundary matrices as numpy
print(f"Building boundary matrices... n0={n0}, n1={n1}, n2={n2}")


def boundary_matrix_np(k_simplices, km1_simplices):
    idx = {s: i for i, s in enumerate(km1_simplices)}
    m = len(km1_simplices)
    n = len(k_simplices)
    M = np.zeros((m, n), dtype=float)
    for j, s in enumerate(k_simplices):
        for sign, f in faces(s):
            i = idx.get(f)
            if i is not None:
                M[i, j] = sign
    return M


d1 = boundary_matrix_np(edges1, vertices)
d2 = boundary_matrix_np(tris2, edges1)

print(f"d1: {d1.shape}, d2: {d2.shape}")

# Compute Z1 (kernel of d1) and B1 (image of d2)
# Z1 = nullspace of d1
# B1 = columnspace of d2

# Use SVD for numerical stability
U, s, Vh = np.linalg.svd(d1)
rank_d1 = np.sum(s > 1e-10)
Z1_basis = Vh[rank_d1:].T  # Last rows of V are nullspace
dim_Z1 = Z1_basis.shape[1] if len(Z1_basis.shape) > 1 else 0

print(f"Z1 dimension: {dim_Z1}")

# B1 from d2
U2, s2, Vh2 = np.linalg.svd(d2)
rank_d2 = np.sum(s2 > 1e-10)
dim_B1 = rank_d2

print(f"B1 dimension: {dim_B1}")
print(f"H1 dimension (beta1): {dim_Z1 - dim_B1}")

beta1 = dim_Z1 - dim_B1

# Build H1 basis: orthogonal complement of B1 within Z1
# B1 in Z1 coordinates: project columns of d2 onto Z1 basis
B1_in_Z1 = Z1_basis.T @ d2  # Shape: (dim_Z1, n2)

print(f"B1_in_Z1 shape: {B1_in_Z1.shape}")

# Get orthonormal basis for B1 subspace within Z1
if dim_B1 > 0 and dim_Z1 > 0:
    # SVD of B1_in_Z1 to find orthonormal basis of B1 within Z1
    U_B, s_B, _ = np.linalg.svd(B1_in_Z1, full_matrices=False)
    rank_B1_in_Z1 = np.sum(s_B > 1e-10)
    print(f"Rank of B1 in Z1: {rank_B1_in_Z1}")

    # First rank_B1_in_Z1 columns of U_B span B1 within Z1
    B1_orthonormal = U_B[:, :rank_B1_in_Z1]  # Shape: (dim_Z1, rank)

    # Now find orthogonal complement (H1 basis)
    # Complete to full orthonormal basis of R^{dim_Z1}
    # Use random vectors and Gram-Schmidt
    full_basis = np.hstack(
        [B1_orthonormal, np.random.randn(dim_Z1, dim_Z1 - rank_B1_in_Z1)]
    )
    Q_full, _ = np.linalg.qr(full_basis)

    H1_basis_in_Z1 = Q_full[
        :, rank_B1_in_Z1 : rank_B1_in_Z1 + beta1
    ]  # Shape: (dim_Z1, beta1)
else:
    H1_basis_in_Z1 = np.eye(dim_Z1)[:, :beta1]

print(f"H1_basis_in_Z1 shape: {H1_basis_in_Z1.shape}")

# Convert back to edge space
H1_basis = Z1_basis @ H1_basis_in_Z1  # Shape: (n1, beta1)

print(f"H1 basis shape: {H1_basis.shape}")

# Verify H1 basis are cycles
for i in range(min(3, beta1)):
    d1_h = d1 @ H1_basis[:, i]
    print(f"  ||d1 * h_{i}|| = {np.linalg.norm(d1_h):.2e}")

edge_index = {e: i for i, e in enumerate(edges1)}


def gen_point_perm(gen):
    return [int(gen(i + 1)) - 1 for i in range(40)]


def edge_action_matrix(point_perm):
    """Build n1 x n1 permutation-sign matrix for edge action."""
    M = np.zeros((n1, n1), dtype=float)
    for i, (a, b) in enumerate(edges1):
        ua = point_perm[a]
        ub = point_perm[b]
        if ua < ub:
            j = edge_index[(ua, ub)]
            M[j, i] = 1
        else:
            j = edge_index[(ub, ua)]
            M[j, i] = -1
    return M


def h1_action_matrix(g):
    """Compute H1 action matrix for group element g."""
    perm = gen_point_perm(g)
    E = edge_action_matrix(perm)

    # Action on H1: project E * H1_basis back onto H1
    # New coords = H1_basis^+ * E * H1_basis
    # Using pseudoinverse for stability
    E_h1 = E @ H1_basis
    # Project onto H1 subspace
    H1_coords = np.linalg.lstsq(H1_basis, E_h1, rcond=None)[0]
    return H1_coords


# Compute H1 matrices for generators
print("\n--- Generator H1 matrices ---")
h1_gen_matrices = []
for i, g in enumerate(gens):
    mat = h1_action_matrix(g)
    h1_gen_matrices.append(mat)
    tr = np.trace(mat)
    det = np.linalg.det(mat)
    print(f"Generator {i}: order={g.order()}, trace={tr:.2f}, det={det:.2f}")

# Test homomorphism
print("\n--- Testing homomorphism ---")
for trial in range(3):
    idx1 = trial % len(gens)
    idx2 = (trial + 1) % len(gens)
    g1 = gens[idx1]
    g2 = gens[idx2]
    g12 = g1 * g2

    mat1 = h1_gen_matrices[idx1]
    mat2 = h1_gen_matrices[idx2]
    mat12 = h1_action_matrix(g12)

    product = mat1 @ mat2
    match = np.allclose(product, mat12)
    print(f"  g{idx1}*g{idx2}: ρ(g1*g2) = ρ(g1)ρ(g2)? {match}")
    if not match:
        print(f"    Max diff: {np.max(np.abs(product - mat12)):.6f}")

# If homomorphism passes, compute character on conjugacy classes
print("\n--- Computing H1 character ---")

gap_G = libgap(A)
char_table = gap_G.CharacterTable()
gap_classes = char_table.ConjugacyClasses()
n_classes = len(gap_classes)
class_sizes = [int(libgap.Size(c)) for c in gap_classes]

print(f"Number of classes: {n_classes}")

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

    mat = h1_action_matrix(g)
    trace = np.trace(mat)
    h1_chi.append(round(trace))

    order_elem = int(libgap.Order(rep_gap))
    print(
        f"  Class {c_idx}: size={class_sizes[c_idx]:5}, order={order_elem:2}, chi={h1_chi[-1]}"
    )

# Compute <chi, chi>
chi_squared = (
    sum(class_sizes[j] * h1_chi[j] ** 2 for j in range(n_classes)) / group_order
)
print(f"\n<chi_H1, chi_H1> = {chi_squared:.4f}")

if chi_squared >= 0.99:
    print("✓ Valid character!")

    # Now compute multiplicities
    print("\n--- Irreducible decomposition ---")
    irreps = char_table.Irr()

    decomposition = []
    total_dim = 0

    for i in range(len(irreps)):
        irrep_chi_list = list(irreps[i])
        dim_i = int(
            irrep_chi_list[0].IsInt()
            and int(irrep_chi_list[0])
            or round(complex(str(irrep_chi_list[0].sage())).real)
        )

        # Compute inner product
        inner_sum = 0
        for j in range(n_classes):
            gap_val = irrep_chi_list[j]
            try:
                if gap_val.IsInt():
                    chi_i_val = int(gap_val)
                else:
                    chi_i_val = complex(str(gap_val.sage()))
            except:
                chi_i_val = complex(str(gap_val.sage()))

            chi_i_conj = (
                chi_i_val.conjugate() if isinstance(chi_i_val, complex) else chi_i_val
            )
            inner_sum += class_sizes[j] * h1_chi[j] * chi_i_conj

        inner = inner_sum / group_order
        mult_approx = inner.real if hasattr(inner, "real") else float(inner)
        mult = round(mult_approx)

        if mult > 0:
            print(f"  Irrep {i}: dim={dim_i:3}, multiplicity={mult}")
            decomposition.append((i, dim_i, mult))
            total_dim += mult * dim_i

    print(f"\nTotal dimension: {total_dim}")
    print(f"Expected (H1 dim): {beta1}")
    print(f"Match: {total_dim == beta1}")
else:
    print("✗ Character invalid - check H1 computation")
