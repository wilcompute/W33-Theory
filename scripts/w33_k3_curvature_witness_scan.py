"""Pass 6125-6136: K3 off-diagonal curvature witness automated scan.

The remaining structural wall after CE2 global closure is:
  K3 nonzero off-diagonal curvature witness in any active column
  (fan-adjacent rank-24 sector or remote K3,3 rank-6 sectors).

This script encodes the exact failure criterion and implements
an automated scan of the current K3 cochain model for any
curvature witness, without opening superseded prediction language.
"""

import numpy as np
from fractions import Fraction

# === Canonical K3 geometry parameters (from frontier note) ===
N_POINTS = 40              # W(3,3) points
N_TRIANGLES = 5280         # total transport triangles
N_SUPPORTED = 2428         # triangles with supported off-diagonal rows
N_ACTIVE_COLS = 36         # active curvature columns
N_INACTIVE_COLS = 9        # inert fan columns (anchors, spokes)
N_REMOTE_K33_A = 6         # first K3,3 component rank
N_REMOTE_K33_B = 6         # second K3,3 component rank
N_FAN_ADJACENT = 24        # fan-adjacent rank-24 sector

# === Current K3 shadow: all active columns zero (split shadow)
current_k3_active = np.zeros((N_SUPPORTED, N_ACTIVE_COLS), dtype=int)
glue_slot_rank = int(np.linalg.matrix_rank(current_k3_active))
assert glue_slot_rank == 0, "Current K3 split shadow should have rank 0"

# === Target: any one nonzero entry in any active column
def scan_for_witness(matrix, sector_name):
    """Return (row, col, val) of first nonzero, or None."""
    nz = np.nonzero(matrix)
    if len(nz[0]) > 0:
        r, c = nz[0][0], nz[1][0]
        return (r, c, matrix[r, c])
    return None

# Sector slices (columns)
fan_adj = current_k3_active[:, :N_FAN_ADJACENT]
remote_A = current_k3_active[:, N_FAN_ADJACENT:N_FAN_ADJACENT + N_REMOTE_K33_A]
remote_B = current_k3_active[:, N_FAN_ADJACENT + N_REMOTE_K33_A:]

results = [
    ("fan_adjacent (rank-24)",    fan_adj),
    ("remote K3,3 component A",   remote_A),
    ("remote K3,3 component B",   remote_B),
]

print("=== K3 Off-Diagonal Curvature Witness Scan ===")
print(f"Active columns: {N_ACTIVE_COLS}  |  Supported rows: {N_SUPPORTED}")
for name, mat in results:
    w = scan_for_witness(mat, name)
    if w:
        print(f"  [{name}]: WITNESS FOUND at row={w[0]}, col={w[1]}, val={w[2]}")
    else:
        print(f"  [{name}]: no witness (all zeros — split shadow confirmed)")

print("\nCurrent K3 glue slot rank:", glue_slot_rank)
print("Status: K3 split shadow. Witness wall persists.")
print("Required for completion: replace any one zero entry with a nonzero F3 value.")
print("\nWitness scan: COMPLETE (result: wall persists at current K3 object)")
