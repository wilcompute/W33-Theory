#!/usr/bin/env python3
"""Pass 1052: BC clock CMB signature — falsifiable prediction
Co-Authored-By: Perplexity AI (Sonnet 4.6) <noreply@perplexity.ai>
"""
import numpy as np
from fractions import Fraction

q, v, k, mu, Phi4 = 3, 40, 12, 4, 10

theta_BC = np.arccos(-2/3)
log_period = 2*np.pi / theta_BC
N = 2*(v - Phi4)  # 60
ns = 1 - 2/N
r  = k / N**2
f_NL = Fraction(1, 72)

print("Boerdijk-Coxeter Clock -> CMB Predictions (zero free parameters)")
print(f"  theta_BC = arccos(-2/3) = {theta_BC:.8f} rad")
print(f"  theta/pi = {theta_BC/np.pi:.8f}  (irrational, Niven's theorem)")
print(f"  CMB log-period = 2pi/theta = {log_period:.6f} in ln(k)")
print(f"  N efolds = 2*(v-Phi4) = {N} = 2*h(E8)")
print(f"  ns = 1 - 2/N = {ns:.6f} = 29/30")
print(f"  r  = k/N^2  = {r:.6f} = 1/300")
print(f"  fNL = 1/72  = {float(f_NL):.6f}")
print()

# Steinhaus 3-gap verification at n=30=h(E8)
phases = sorted([(i * theta_BC) % (2*np.pi) for i in range(1, 31)])
gaps = [phases[i+1]-phases[i] for i in range(len(phases)-1)]
gaps.append(2*np.pi - phases[-1] + phases[0])
n_gaps = len(set([round(g, 5) for g in gaps]))
print(f"Steinhaus 3-gap at n=30=h(E8): {n_gaps} distinct gap lengths (expected: 2)")
assert n_gaps == 2, f"Expected 2 gaps, got {n_gaps}"
print("BC quasicrystal signature VERIFIED at h(E8) ring length")
print()
print("FALSIFIABLE: LiteBIRD/CMB-S4 three-gap comb with log-period ~2.73")
print(f"Planck 2018: ns=0.9649+-0.0044")
print(f"W33 ns=0.9667, agreement = {abs(ns-0.9649)/0.9649*100:.2f}%")
