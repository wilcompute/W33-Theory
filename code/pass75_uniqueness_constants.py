#!/usr/bin/env python3
"""
Pass 75: q=3 uniqueness, sin²θW=37/160, complete constant table
Date: 2026-07-08
"""
import math
from sympy import isprime, Rational

print("=== W(q,q) UNIVERSALITY SCAN ===")
print(f"{'q':<5} {'k':<7} {'α⁻¹':<10} {'prime':<8} {'mp/me':<12} {'Λ_exp'}")
for q in range(2, 8):
    k = q*(q+1)
    v = (q+1)*(q**2+1)
    mu = q+1
    alpha_inv = (k-1)**2 + (k//q)**2
    mp_me = k*(k**2+q**2)
    lam_exp = -(v*(v+1)//2 + mu//2) if q==3 else -(15*16//2 + mu//2)  # v22=15 for bridge
    # Corrected Λ: always use v22=15
    lam_exp = -(15*16//2 + (q+1)//2)
    print(f"{q:<5} {k:<7} {alpha_inv:<10} {('✓' if isprime(alpha_inv) else '✗'):<8} {mp_me:<12} {lam_exp}")

print("\n=== PROOF: EVEN q → α⁻¹ COMPOSITE ===")
for q in [2,4,6,8]:
    k = q*(q+1)
    a, b = k-1, k//q  # a=odd, b=odd (for even q)
    print(f"q={q}: k={k}, k-1={a}({'odd' if a%2 else 'even'}), k/q={b}({'odd' if b%2 else 'even'}), α⁻¹={a**2+b**2}({'even' if (a**2+b**2)%2==0 else 'odd'})")

print("\n=== sin²θW FORMULA ===")
v33, k33, mu22 = 40, 12, 3
beta4 = v33 - mu22
sin2 = Rational(mu22*beta4, k33*v33)
print(f"sin²θW = μ₂₂(v₃₃-μ₂₂)/(k₃₃·v₃₃) = {mu22}×{beta4}/({k33}×{v33}) = {sin2} = {float(sin2):.6f}")
print(f"PDG: 0.23122, error: {abs(float(sin2)-0.23122)/0.23122*100:.4f}%")

print("\n=== COMPLETE CONSTANT TABLE ===")
k, q = 12, 3
v33, v22, mu22, mu33, lam33 = 40, 15, 3, 4, 2
alpha_inv = (k-1)**2 + (k//q)**2
mp_me = k*(k**2+q**2)
lambda_exp = -(v22*(v22+1)//2 + mu33//2)
sin2W = Rational(mu22*(v33-mu22), k33*v33)
koide = Rational(lam33, q)
neff = q + lam33*mu33/v33

for name, w33, pdg in [
    ("α⁻¹", alpha_inv, 137.036),
    ("mₚ/mₑ", mp_me, 1836.15),
    ("Λ_exp", lambda_exp, -122),
    ("sin²θW", float(sin2W), 0.23122),
    ("Koide K", float(koide), 2/3),
    ("Neff", neff, 3.044),
]:
    err = abs(w33-pdg)/abs(pdg)*100 if pdg != 0 else 0
    print(f"  {name}: W33={w33}, PDG={pdg}, err={err:.3f}%")

print("\nPass 75 complete.")
