#!/usr/bin/env python3
"""
BT426 - SUBSTRATE PARTITION FUNCTION AND VACUUM ENERGY
Minimal toric-code-style partition function for the W(3,3) substrate Hamiltonian.
"""

import math

q, lam, mu = 3, 2, 4
n_vertices = 40
n_lines = 40
N_terms = n_vertices + n_lines
J = 0.5  # choose units so mass gap = 2J = 1 in naturalized substrate units

print("="*70)
print("BT426: SUBSTRATE PARTITION FUNCTION AND VACUUM ENERGY")
print("="*70)
print()
print("Substrate Hamiltonian (BT353):")
print("  H = -J Σ_v A_v - J Σ_L B_L")
print(f"  # vertex stabilizers = {n_vertices}")
print(f"  # line stabilizers   = {n_lines}")
print(f"  total commuting terms N = {N_terms}")
print()

# Since A_v, B_L have eigenvalues ±1 in the effective low-energy commuting sector,
# each term contributes factor 2 cosh(beta J). This is the standard commuting-projector estimate.

def Z(beta):
    return (2*math.cosh(beta*J))**N_terms

def logZ(beta):
    return N_terms * math.log(2*math.cosh(beta*J))

def avgH(beta):
    return -N_terms * J * math.tanh(beta*J)

def freeE(beta):
    return -(1/beta) * logZ(beta)

beta_vals = [0.1, 1.0, 10.0, 100.0]
print("Thermodynamics in substrate units:")
for beta in beta_vals:
    print(f"  beta={beta:6.1f} : log Z = {logZ(beta):10.6f}   <H> = {avgH(beta):10.6f}   F = {freeE(beta):10.6f}")
print()

E0 = -N_terms * J
print(f"Zero-temperature vacuum energy E0 = -N*J = -{N_terms}*{J} = {E0}")
print(f"Mass gap above vacuum = 2J = {2*J}")
print()

# geometric interpretation
print("-"*70)
print("VACUUM ENERGY DENSITY")
print("-"*70)
print("Take one substrate cell per W(3,3) node-volume in Planck units.")
print(f"Effective vacuum energy density rho_vac ~ |E0| / N_terms = {abs(E0)/N_terms:.6f} (Planck-cell units)")
print()

# Fractal suppression to cosmological tier
r = 27/80
n_H0 = 129
suppression = r**(2*n_H0)
print(f"Fractal suppression from Planck sector to H0 tier: r^(2*n_H0) = r^(258) = {suppression:.4e}")
print("This is the natural mechanism turning O(1) Planck vacuum energy into a tiny IR cosmological constant.")
print()

# We do not claim exact physical units here; derive order-of-magnitude logic.
print("Order-of-magnitude substrate cosmological constant:")
Lambda_planck = 1.0
Lambda_IR = Lambda_planck * suppression
print(f"  Lambda_IR / Lambda_Planck ~ {Lambda_IR:.4e}")
print("  The observed Lambda requires additional geometric renormalization from the tier ladder and horizon volume.")
print("  But the key point is now explicit: the commuting-projector partition function gives a finite vacuum energy,")
print("  and the fractal tier ladder suppresses it exponentially into the infrared.")
print()

print("-"*70)
print("SUBSTRATE INTERPRETATION")
print("-"*70)
print("1. The vacuum is NOT a divergent continuum sea; it is a finite stabilizer substrate.")
print("2. Z(beta) is finite because the substrate Hilbert space per cell is finite (qutrit/binary product code).")
print("3. The cosmological constant problem is softened: finite E0 times huge fractal suppression.")
print("4. The IR value of Lambda comes from substrate vacuum energy after tier-flow renormalization.")
print()
print("STATUS:")
print("  First explicit partition function for the W(3,3) substrate Hamiltonian completed.")
print("  Exact SI-unit matching to Lambda_obs is deferred to BT428 (full geometric renormalization).")
