"""Attack 4: Clifford stabilizer of the 9+6 determinant split in Sp(4,2) ≅ S_6.

Status: OPEN — scaffolding only. No closures claimed.

Goal:
  1. Enumerate Sp(4,2) (order 720 = |S_6|).
  2. Find the setwise stabilizer of the rank-1 locus (9 points) = Stab_Sp(4,2)(singular).
  3. Find the setwise stabilizer of the units locus (6 points) = Stab_Sp(4,2)(units).
  4. Determine the action on the 10 quadratic grids (how many orbits).
  5. Identify the bridge to two-qubit Clifford geometry via Sp(4,2).

NOTE: The isomorphism Sp(4,2) ≅ S_6 is classical (order 720).
The stabilizer computation is a clean finite-group problem solvable by enumeration.
This script enumerates Sp(4,2) explicitly.

FIREWALL: results here are finite symplectic geometry, not quantum circuit claims.
"""
from itertools import product
import numpy as np

F2 = [0, 1]

def mat4(rows): return tuple(tuple(r) for r in rows)

def matmul4(A, B):
    return mat4([[ sum(A[i][k]*B[k][j] for k in range(4))%2
                   for j in range(4)] for i in range(4)])

def is_symplectic4(M):
    """Check M^T J M = J mod 2, J = [[0,I],[−I,0]] = [[0,1,0,0],[−1,0,0,0],[0,0,0,1],[0,0,−1,0]] over F_2."""
    # Over F_2, -1 = 1, so J = [[0,1,0,0],[1,0,0,0],[0,0,0,1],[0,0,1,0]] — WRONG.
    # Standard J for Sp(4,2) with ordered basis (x1,z1,x2,z2):
    # <u,v> = u0v1-u1v0+u2v3-u3v2 mod 2 = u0v1+u1v0+u2v3+u3v2 mod 2
    # J[i][j] = <e_i, e_j>:
    # e0=(1,0,0,0),e1=(0,1,0,0),e2=(0,0,1,0),e3=(0,0,0,1)
    # <e0,e1>=1, <e1,e0>=1, <e2,e3>=1, <e3,e2>=1, rest 0
    J = ((0,1,0,0),(1,0,0,0),(0,0,0,1),(0,0,1,0))
    def sp(u,v): return (u[0]*v[1]+u[1]*v[0]+u[2]*v[3]+u[3]*v[2])%2
    for i in range(4):
        for j in range(4):
            # (M^T J M)[i][j] should equal J[i][j]
            # = sp(M_col_i, M_col_j) where M_col_k = (M[0][k],M[1][k],M[2][k],M[3][k])
            ci = tuple(M[r][i] for r in range(4))
            cj = tuple(M[r][j] for r in range(4))
            if sp(ci,cj) != J[i][j]: return False
    return True

# OPEN: full Sp(4,2) enumeration is feasible (720 elements) but expensive by brute force.
# Recommended approach: generate from known generators of Sp(4,2).
# Standard generators (transvections):
# T_{e_i,e_j} for i != j with sp(e_i,e_j) != 0: add sp(v,e_i)*e_j component.
# We use the Steinberg presentation: generators are transvections T_v for isotropic v.

# For now we enumerate by random walk / closure — scaffold only.
# TODO: implement Schreier-Sims or use a generating set to close the group.

print("Attack 4 scaffold loaded.")
print("Status: OPEN — Sp(4,2) stabilizer computation not yet executed.")
print("Next step: implement transvection generators and close under multiplication.")

# Sanity: count isotropic vectors in F_2^4 (should be 15 nonzero + 0 = 15 for Sp(4,2))
def sp_form(u,v): return (u[0]*v[1]+u[1]*v[0]+u[2]*v[3]+u[3]*v[2])%2
all_v4 = list(product(F2,repeat=4))
isotropic_nz = [v for v in all_v4 if any(v) and sp_form(v,v)==0]
print(f"Nonzero isotropic vectors in F_2^4: {len(isotropic_nz)} (all 15 are isotropic over F_2)")
# Over F_2, sp(v,v) = 2*(v0v1+v2v3) = 0 always, so all nonzero vectors are isotropic.
assert len(isotropic_nz)==15

# OPEN items logged explicitly:
OPEN_ITEMS = [
    "Sp(4,2) full group enumeration",
    "Setwise stabilizer of rank-1 locus (9 pts)",
    "Setwise stabilizer of unit locus (6 pts)",
    "Orbit structure of 10 quadratic grids under Sp(4,2)",
    "Connection to two-qubit Clifford group (image in Sp(4,2))",
]
for item in OPEN_ITEMS:
    print(f"  OPEN: {item}")
