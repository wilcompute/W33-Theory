"""Pass 6201-6216: Transport-cocycle comparison scaffold.

Builds the exact comparison scaffold between the internal family flag
(span(1,1,0) < {x=y}) and the external U1 head-biased line/plane,
without claiming the final isomorphism prematurely.
"""

import numpy as np

# Internal plane P_int = span(u,v) with u=(1,1,0), v=(0,0,1)
u = np.array([1.0, 1.0, 0.0])
v = np.array([0.0, 0.0, 1.0])
P_int = np.stack([u, v], axis=1)
G_int = P_int.T @ P_int

# External plane P_ext = U1 hyperbolic plane with basis e=(1,0), f=(0,1)
e = np.array([1.0, 0.0])
f = np.array([0.0, 1.0])
G_ext = np.array([[0.0, 1.0], [1.0, 0.0]])

# Canonical comparison data:
# internal flag line = span(u)
# external head line = span(e+rho f), rho>1 from selector dominance
rho = 1.3257392335
head_line_ext = np.array([1.0, rho])

print("=== Transport-Cocycle Comparison Scaffold ===")
print("Internal Gram matrix on span((1,1,0),(0,0,1)):")
print(G_int)
print("\nExternal U1 hyperbolic form:")
print(G_ext)
print(f"\nExternal head-biased line generator: (1, {rho})")

# Rank checks
print(f"\nrank(G_int) = {np.linalg.matrix_rank(G_int)}")
print(f"rank(G_ext) = {np.linalg.matrix_rank(G_ext)}")

# Signature checks
int_eigs = np.linalg.eigvalsh(G_int)
ext_eigs = np.linalg.eigvalsh(G_ext)
print(f"eig(G_int) = {int_eigs}")
print(f"eig(G_ext) = {ext_eigs}")

print("\nComparison status:")
print("  - Both ambient spaces are rank-2 planes.")
print("  - Internal plane is positive semidefinite in inherited Euclidean metric.")
print("  - External U1 plane is hyperbolic of signature (1,1).")
print("  - Any exact identification must therefore include a transport/cocycle renormalization,")
print("    not a naive linear isometry in the raw inherited metrics.")
print("\nScaffold result: exact cocycle map remains OPEN, but the metric mismatch is now isolated.")
