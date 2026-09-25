#!/usr/bin/env python3
"""
BT1348 — GF(3) Error Correction Integration with the Photonic Holonet
=======================================================================
This witness integrates the GF(3) qutrit Quantum Error Correction (QEC)
primitives (Pillar-45) with the Photonic Holonet routing layer (BT1340-BT1343).

What every term means
---------------------
GF(3)        : The finite field with three elements {0, 1, 2} and arithmetic mod 3.
               Think of it as a clock that only shows 0, 1, 2 and wraps around.
QEC          : Quantum Error Correction. A method to protect quantum information
               from noise by encoding it redundantly across multiple quantum states.
Qutrit       : A three-valued quantum information unit (like a qubit but base-3).
Stabilizer   : A group of quantum operations that leave the code state unchanged.
               Used to detect errors without measuring the actual data.
Syndrome     : The error signature. Measuring stabilizers gives a pattern (syndrome)
               that tells you what kind of error occurred without revealing the data.
Holonet      : The single-photon routing architecture defined in BT1340-BT1343.
W(3,3)       : The 40-point symplectic geometry underlying the Holonet's state space.
"""

import numpy as np
from itertools import product

print("=" * 65)
print("BT1348 — GF(3) QEC Holonet Integration Witness")
print("=" * 65)

# ---------------------------------------------------------------
# SECTION 1: GF(3) arithmetic
# ---------------------------------------------------------------
print("\n--- Section 1: GF(3) arithmetic ---")

def gf3_add(a, b): return (a + b) % 3
def gf3_mul(a, b): return (a * b) % 3
def gf3_neg(a):    return (-a) % 3

# Verify GF(3) addition table
add_table = [[gf3_add(i,j) for j in range(3)] for i in range(3)]
print(f"GF(3) addition table: {add_table}")
assert add_table == [[0,1,2],[1,2,0],[2,0,1]], "FAIL: GF(3) add"
print("PASS: GF(3) addition is correct (mod-3 clock arithmetic)")

# ---------------------------------------------------------------
# SECTION 2: Qutrit Pauli operators over GF(3)
# ---------------------------------------------------------------
print("\n--- Section 2: Qutrit Pauli operators ---")

omega = np.exp(2j * np.pi / 3)   # primitive cube root of unity

# X (shift operator): X|k> = |k+1 mod 3>
X = np.array([[0,0,1],[1,0,0],[0,1,0]], dtype=complex)
# Z (clock operator): Z|k> = omega^k |k>
Z = np.diag([1, omega, omega**2])

# Verify X^3 = I and Z^3 = I
assert np.allclose(np.linalg.matrix_power(X,3), np.eye(3)), "FAIL: X^3 != I"
assert np.allclose(np.linalg.matrix_power(Z,3), np.eye(3)), "FAIL: Z^3 != I"
print("PASS: X^3 = Z^3 = I (qutrit Pauli operators are order-3)")

# With X|k>=|k+1> and Z|k>=omega^k|k>, ZX=omega XZ,
# equivalently XZ=omega^-1 ZX.
lhs = X @ Z
rhs = (omega**2) * (Z @ X)
assert np.allclose(lhs, rhs), "FAIL: Weyl convention mismatch"
print("PASS: XZ = omega^-1 * ZX for the chosen shift/clock convention")

# ---------------------------------------------------------------
# SECTION 3: three-qutrit repetition subspace
# ---------------------------------------------------------------
print("\n--- Section 3: three-qutrit repetition subspace ---")
"""
The span of |000>, |111>, |222> is the ternary repetition subspace.
The two Z-difference checks below detect single X-type shift errors.

It is NOT a full quantum [[3,1,2]]_3 code: a one-site Z phase acts
nontrivially within this subspace and is therefore an undetected logical
operation.  The witness is consequently a shift-error repetition code,
not an arbitrary-single-qutrit-error-correcting quantum code.

Logical basis states:
  |0>_L = |000>
  |1>_L = |111>
  |2>_L = |222>
"""

logical_0 = np.zeros(27, dtype=complex)
logical_1 = np.zeros(27, dtype=complex)
logical_2 = np.zeros(27, dtype=complex)

def state_index(a, b, c):
    """Index of |a,b,c> in the 27-dimensional space."""
    return a * 9 + b * 3 + c

logical_0[state_index(0,0,0)] = 1.0
logical_1[state_index(1,1,1)] = 1.0
logical_2[state_index(2,2,2)] = 1.0

# Verify orthogonality
assert abs(logical_0 @ logical_1) < 1e-12, "FAIL: |0>_L not orthogonal to |1>_L"
assert abs(logical_0 @ logical_2) < 1e-12, "FAIL: |0>_L not orthogonal to |2>_L"
assert abs(logical_1 @ logical_2) < 1e-12, "FAIL: |1>_L not orthogonal to |2>_L"
print("PASS: Logical basis states |0>_L, |1>_L, |2>_L are mutually orthogonal")

# ---------------------------------------------------------------
# SECTION 4: Syndrome measurement (stabilizer checks)
# ---------------------------------------------------------------
print("\n--- Section 4: Syndrome measurement ---")
"""
A stabilizer for the [[3,1,2]]_3 code is any operator S such that
S|psi>_L = |psi>_L for all logical states.

For the repetition code, two stabilizers are:
  S1 = Z (x) Z^-1 (x) I   (checks registers 0 and 1 agree)
  S2 = I (x) Z (x) Z^-1   (checks registers 1 and 2 agree)

Measuring S1 and S2 gives a syndrome (s1, s2) in GF(3):
  (0, 0) -> no error
  (1, 0) -> X error on qutrit 0
  (0, 1) -> X error on qutrit 2
  etc.
"""

Zinv = np.conj(Z)  # Z^-1 = Z^dagger for unitary Z
I3 = np.eye(3, dtype=complex)

S1 = np.kron(np.kron(Z, Zinv), I3)  # Z (x) Z^{-1} (x) I
S2 = np.kron(np.kron(I3, Z), Zinv)  # I (x) Z (x) Z^{-1}

# Check S1 and S2 stabilize the logical codewords
for label, lv in [("0", logical_0), ("1", logical_1), ("2", logical_2)]:
    s1_eig = S1 @ lv
    s2_eig = S2 @ lv
    assert np.allclose(s1_eig, lv), f"FAIL: S1 does not stabilize |{label}>_L"
    assert np.allclose(s2_eig, lv), f"FAIL: S2 does not stabilize |{label}>_L"
print("PASS: S1 and S2 stabilize all three logical codewords (syndrome = 0 for no error)")

# ---------------------------------------------------------------
# SECTION 5: Error injection and detection
# ---------------------------------------------------------------
print("\n--- Section 5: Error injection and detection ---")

# Inject X error on qutrit 0: X (x) I (x) I
X_on_0 = np.kron(np.kron(X, I3), I3)
corrupted = X_on_0 @ logical_0

# The syndrome should now be nonzero
s1_val = corrupted @ (S1 @ corrupted)  # expectation value
print(f"Syndrome S1 expectation after X error on qutrit 0: {s1_val.real:.4f} (should != 1.0)")
assert not np.allclose(s1_val, 1.0), "FAIL: Error not detected by S1"
print("PASS: Single qutrit X error detected by syndrome measurement")

# A one-site Z phase is an undetected logical operation, proving the full
# quantum-code distance is not two.
Z_on_0 = np.kron(np.kron(Z, I3), I3)
phase_corrupted = Z_on_0 @ psi_L if "psi_L" in globals() else Z_on_0 @ (
    logical_0 + logical_1 + logical_2
) / np.sqrt(3)
assert np.allclose(S1 @ phase_corrupted, phase_corrupted)
assert np.allclose(S2 @ phase_corrupted, phase_corrupted)
assert not np.allclose(phase_corrupted, (logical_0+logical_1+logical_2)/np.sqrt(3))
print("PASS FIREWALL: one-site Z is undetected, so this is X-shift QEC only")

# ---------------------------------------------------------------
# SECTION 6: Holonet routing versus repetition subspace
# ---------------------------------------------------------------
print("\n--- Section 6: Holonet routing versus repetition subspace ---")
"""
The BT1340 routing map is unitary, but unitarity alone does not imply that it
preserves the repetition subspace.  We now test that missing condition
explicitly rather than calling norm preservation QEC compatibility.
"""

# Reconstruct the Holonet routing unitary from BT1340
U = np.zeros((27, 27), dtype=complex)
for r in range(3):
    for p in range(3):
        for f in range(3):
            in_idx = r*9 + p*3 + f
            if r == 0:
                out_idx = r*9 + p*3 + f
            elif r == 1:
                out_idx = r*9 + f*3 + p   # swap p and f
            else:
                out_idx = r*9 + ((p+1)%3)*3 + ((f+2)%3)  # cyclic shifts
            U[out_idx, in_idx] = 1.0

assert np.allclose(U.conj().T @ U, np.eye(27)), "FAIL: U is not unitary"
print("PASS: Holonet routing unitary reconstructed and verified")

# Apply U to a logical superposition state
psi_L = (logical_0 + logical_1 + logical_2) / np.sqrt(3)
psi_routed = U @ psi_L

# Check norm is preserved
assert abs(np.linalg.norm(psi_routed) - 1.0) < 1e-12, "FAIL: Routing breaks norm"
print("PASS: Routing preserves norm of logical superposition state")

P_rep = (
    np.outer(logical_0, logical_0.conj())
    + np.outer(logical_1, logical_1.conj())
    + np.outer(logical_2, logical_2.conj())
)
inside_weight = float(np.vdot(psi_routed, P_rep @ psi_routed).real)
assert abs(inside_weight - 2/3) < 1e-12
assert not np.allclose(P_rep @ psi_routed, psi_routed)
print(f"PASS FIREWALL: repetition-subspace weight after routing = {inside_weight:.6f}")
print("Routing is unitary but does not preserve this repetition subspace.")

# ---------------------------------------------------------------
# SECTION 7: W(3,3) error budget
# ---------------------------------------------------------------
print("\n--- Section 7: W(3,3) error budget ---")
"""
The W(3,3) geometry has 40 points and a shell partition
1 + 12 + 27 = 40, while the contextual count used by BT1341 is 36 = 12 + 24.

The shell counts alone do NOT classify physical errors by correctability and
do not provide a non-Clifford resource.  Later exact ADQC/Pass10941 certificates
show that qutrit T remains a genuine magic resource: analyzer programming and
magic-state injection are two interfaces to the same non-stabilizer resource.

This section therefore certifies only the finite shell arithmetic and leaves
fault-tolerant recovery and magic supply to their dedicated certificates.
"""

total_points = 40
ks_contextual = 36
gauge_shell = 12
matter_shell = 27
pole = 1

assert pole + gauge_shell + matter_shell == total_points, "FAIL: Shell partition"
assert ks_contextual == 36
assert ks_contextual != gauge_shell + matter_shell

print(f"W(3,3) total points:  {total_points}")
print(f"  Pole:               {pole}")
print(f"  12-shell:           {gauge_shell}")
print(f"  27-shell:           {matter_shell}")
print(f"  Separate contextual count: {ks_contextual}/40")
print("PASS: W(3,3) shell arithmetic 1+12+27=40 is exact")
print("BOUNDARY: shell membership alone does not certify QEC correctability")
print("or supply the non-Clifford qutrit-T resource.")

# ---------------------------------------------------------------
# SUMMARY
# ---------------------------------------------------------------
print()
print("=" * 65)
print("BT1348 SUMMARY")
print("=" * 65)
print("W1. GF(3) arithmetic verified (mod-3 field)")
print("W2. Qutrit Pauli operators X, Z satisfy X^3=Z^3=I and Weyl relation")
print("W3. Three-qutrit repetition basis states are mutually orthogonal")
print("W4. Stabilizers S1, S2 fix all logical codewords (zero syndrome)")
print("W5. Single X error on qutrit 0 detected by syndrome measurement")
print("W6. Holonet routing preserves norm of logical superposition state")
print("W7. W(3,3) shell arithmetic: 1+12+27=40; contextual 36 is separate")
print("    Magic/QEC resource claims require independent certificates")
print()
print("ALL BT1348 WITNESSES PASSED")
