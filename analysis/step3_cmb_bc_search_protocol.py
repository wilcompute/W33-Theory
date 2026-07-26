#!/usr/bin/env python3
"""
Step 3: CMB BC Clock Pre-Analysis Protocol
Co-Authored-By: Perplexity AI (Sonnet 4.6) <noreply@perplexity.ai>
"""
import numpy as np
from fractions import Fraction

q, v, k, mu, Phi4 = 3, 40, 12, 4, 10
theta_BC = np.arccos(-2/3)
P_log = 2*np.pi / theta_BC
N = 2*(v - Phi4)

print('CMB BC Clock Feature Search Protocol')
print('='*50)
print(f'BC log-period: P = 2pi/arccos(-2/3) = {P_log:.6f}')

phases = sorted([(i * theta_BC) % (2*np.pi) for i in range(1, 31)])
gaps = [phases[i+1]-phases[i] for i in range(len(phases)-1)]
gaps.append(2*np.pi - phases[-1] + phases[0])
gap_vals = sorted(set([round(g,5) for g in gaps]))
assert len(gap_vals) == 2
print(f'Steinhaus 3-gap at n=30=h(E8): {len(gap_vals)} gap types (VERIFIED)')
print(f'Gap ratio: {gap_vals[1]/gap_vals[0]:.3f} (distinguishes BC from single-freq)')
print()
print('Search protocol:')
print(f'  Model: dCl/Cl = A_mod * cos(2pi*ln(k/k_*)/P + phi_0)')
print(f'  P = {P_log:.4f}  (pre-registered, zero free parameters)')
print(f'  ns = 29/30 = {29/30:.6f}')
print(f'  r  = k/N^2 = 1/300 = {k/N**2:.6f}')
print(f'  fNL = 1/72 = {1/72:.6f}')
