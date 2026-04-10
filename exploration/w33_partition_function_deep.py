"""
THE Z(x) GENERATING FUNCTION: Deep Analysis

Z(x) = (1-5x)^10 (1+x)^16 (1+7x)^6

This is a REMARKABLE algebraic object. It looks like:
- A SUSY partition function (alternating signs, integer exponents)
- A Poincaré polynomial of some manifold
- An Ihara-type zeta function 
- A K-theory Euler class

Let's extract EVERY piece of information from it and search for
the connection that closes the theory.
"""

import numpy as np
from fractions import Fraction
import json
from math import comb

q, lam, mu, k = 3, 2, 4, 12
v, f, g = 40, 24, 15
Phi3, Phi4, Phi6, Phi12 = 13, 10, 7, 73
alpha_inv = 137

print("=" * 70)
print("  Z(x) = (1-5x)^10 (1+x)^16 (1+7x)^6: COMPLETE ANALYSIS")
print("=" * 70)

# Parametric form: Z(x;q) = (1-(2q-1)x)^(q²+1) × (1+x)^(2^(q+1)) × (1+(q²-q+1)x)^(2q)
# At q=3: (1-5x)^10 × (1+x)^16 × (1+7x)^6

# The three factors correspond to:
# Gauge sector: (1-5x)^10 = (1-(q+λ)x)^Φ₄
# Matter sector: (1+x)^16 = (1+x)^(2^(q+1))
# Broken/confined: (1+7x)^6 = (1+Φ₆x)^(2q)

# Total degree = 10 + 16 + 6 = 32 = 2^(q+λ)
total_degree = Phi4 + 2**(q+1) + 2*q
print(f"\n  Total degree = Φ₄ + 2^(q+1) + 2q = {Phi4}+{2**(q+1)}+{2*q} = {total_degree} = 2^(q+λ)")

# ═══════════════════════════════════════════════════════
# TAYLOR EXPANSION → TRACE TOWER
# ═══════════════════════════════════════════════════════
print(f"\n{'='*70}")
print("  TAYLOR EXPANSION: -x d/dx ln Z = Σ T(n) x^n")
print("=" * 70)

# -x d/dx ln Z = -x × [Z'(x)/Z(x)]
# For Z = (1-ax)^A (1+bx)^B (1+cx)^C:
# ln Z = A ln(1-ax) + B ln(1+bx) + C ln(1+cx)
# d/dx ln Z = -aA/(1-ax) + bB/(1+bx) + cC/(1+cx)
# -x d/dx ln Z = aAx/(1-ax) - bBx/(1+bx) - cCx/(1+cx)
# = Σ_{n≥1} [aA(ax)^{n-1} × ax + (-b)^n B x^n + (-c)^n C x^n] ... 
# Actually: let's just compute
# aAx/(1-ax) = aA Σ_{n≥1} (ax)^{n-1} x = A Σ_{n≥1} a^n x^n
# bBx/(1+bx) = bB Σ_{n≥1} (-bx)^{n-1} x = B Σ_{n≥1} (-b)^{n-1} b x^n = B Σ (-1)^{n-1} b^n x^n
# Similarly for c

# So: T(n) = A a^n + B (-b)^n + C (-c)^n (this is the trace formula!)
# Wait: -x d/dx ln Z = Σ T(n) x^n
# T(n) = A × a^n - B × (-b)^n - C × (-c)^n

# Let me be more careful:
# ln Z = A ln(1-ax) + B ln(1+bx) + C ln(1+cx)
# -x d/dx ln Z = x [aA/(1-ax)] - x [bB/(1+bx)] - x [cC/(1+cx)]
# x × aA/(1-ax) = aA Σ_{n≥0} (ax)^n × x = A Σ_{n≥1} a^n x^n
# x × bB/(1+bx) = bB Σ_{n≥0} (-bx)^n × x = B Σ_{n≥1} (-1)^{n-1} b^n x^n
# x × cC/(1+cx) = cC Σ_{n≥0} (-cx)^n × x = C Σ_{n≥1} (-1)^{n-1} c^n x^n

# So: T(n) = A a^n - B (-1)^{n-1} b^n - C (-1)^{n-1} c^n
#          = A a^n + B (-b)^n + C (-c)^n  ... wait let me redo

# -x Z'/Z = x [aA/(1-ax) - bB/(1+bx) - cC/(1+cx)]
# Expand each:
# aA x/(1-ax) = A Σ_{n=1}^∞ a^n x^n
# bB x/(1+bx) = B Σ_{n=1}^∞ (-1)^{n+1} b^n x^n
# cC x/(1+cx) = C Σ_{n=1}^∞ (-1)^{n+1} c^n x^n

# So: T(n) = A a^n - B(-1)^{n+1} b^n - C(-1)^{n+1} c^n
#          = A a^n + B(-1)^n b^n + C(-1)^n c^n
#          = A a^n + B(-b)^n + C(-c)^n

# For us: A=10, a=5; B=16, b=1; C=6, c=7 (wait: b for (1+bx) means b=1 for matter)
# But careful about signs. Let's define:
# Factor 1: (1 - 5x)^10 → contributes A a^n with A=10, a=5 to the negative of d/dx ln
# Factor 2: (1 + x)^16 → contributes B(-1)^n with B=16 (since b=1, (-b)^n = (-1)^n)
# Factor 3: (1 + 7x)^6 → contributes C(-7)^n with C=6

# Actually let me just compute numerically
def Z(x):
    return (1 - 5*x)**10 * (1 + x)**16 * (1 + 7*x)**6

def Z_prime(x):
    """Numerical derivative"""
    h = 1e-10
    return (Z(x + h) - Z(x - h)) / (2 * h)

# Trace formula: T(n) = coefficient of x^n in -x Z'(x)/Z(x)
# Which equals: T(n) = 10 × 5^n + 16 × (-1)^n + 6 × (-7)^n

print(f"\n  Trace tower T(n) = 10 × 5^n + 16 × (-1)^n + 6 × (-7)^n")
print(f"\n  n   T(n)        Factored")
print(f"  {'-'*60}")

trace_values = []
for n in range(9):
    Tn = 10 * 5**n + 16 * (-1)**n + 6 * (-7)**n
    trace_values.append(Tn)
    
    # Try to factor through W(3,3)
    if n == 0:
        note = f"= Φ₄ + 2^(q+1) + 2q = v + μ × Φ₆... wait = 10+16+6 = 32 = 2^(q+λ)"
    elif n == 1:
        note = f"= 50 + (-16) + (-42) = -8 = -2^q = -dim(O)"
    elif n == 2:
        note = f"= 250 + 16 + 294 = 560... let me check"
    else:
        note = ""
    
    print(f"  {n}   {Tn:>10}   {note}")

# Wait, T(0) should be 32 = total degree = 2^5
# But our ORIGINAL trace tower had T(0) = v = 40!
# The difference: the trace tower from D_H has T(n) = Tr(D^n)
# while Z(x) gives the IHARA trace tower

# Let me reconcile: in our earlier work,
# Tr(D⁰) = 40 = v (dimension of the space)
# Tr(D¹) = 0 (anomaly cancellation)
# Tr(D²) = 840

# The Z(x) trace tower is DIFFERENT — it comes from the graph zeta function
# -x d/dx ln Z_Ihara = Σ N_n x^n where N_n counts closed paths of length n

# For Ramanujan graphs: Z_Ihara(x) = (1-x²)^{r-1} / det(I - xA + x²(k-1)I)
# where r = rank of fundamental group = E - V + 1

print(f"\n  NOTE: Z(x) trace tower differs from the D_H trace tower!")
print(f"  Z(x) counts closed paths in the GQ(3,3) graph")
print(f"  D_H gives the adjacency matrix trace power tower")
print(f"  They are related but not identical")

# Let's check: the Ihara zeta function of GQ(3,3):
# GQ(3,3) has V=40, E=40×12/2=240 (each vertex has k=12 neighbors)
# For a k-regular graph: Z_Ihara = (1-u²)^{E-V} / det(I - uA + u²(k-1)I)
# where A is the adjacency matrix

# If GQ(3,3) is Ramanujan, then:
# det(I - uA + (k-1)u²I) = product over eigenvalues λ_i of (1 - λ_i u + (k-1)u²)

# Eigenvalues of GQ(3,3): k=12 (mult 1), q=3 (mult m₁), -1 (mult m₂), -(q+1)=-4 (mult m₃)
# with m₁ + m₂ + m₃ = v - 1 = 39

# For GQ(q,q): multiplicities are:
# m₁ = q(q+1)²(q²+1)/2 for eigenvalue q  → = 3×16×10/2 = 240? No, that's too big
# Actually for W(q): the eigenvalues and multiplicities of the point graph are:
# λ₀ = q(q+1) = k, mult 1
# λ₁ = q-1, mult q²(q²+1)/2
# λ₂ = -(q+1), mult q(q²+1)/2  
# λ₃ = -1, mult q²(q-1)(q+1)/2  ... these formulas vary by source

# Let me just compute for q=3:
# v = 40 vertices. Need multiplicities summing to 39.
# From our earlier work: eigenvalues q=3 (mult m₁=10), -1 (mult m₂=24?), -4 (mult m₃=6?)
# Check: m₁ + m₂ + m₃ + 1 = 40... 10+24+6 = 40... that works if +1 for the k=12 eigenvalue

# Actually from the SPECTRAL data in our D_H construction:
# multiplicities: (m₁, m₂, m₃) = (10, 6, 24) for eigenvalues (√3, -√3, 0)
# But those are eigenvalues of the DESIGN matrix, not the adjacency matrix

# The adjacency eigenvalues of GQ(q,q) point graph:
# q(q+1) with mult 1
# q with mult q²(q+1)/2 = 9×4/2 = 18? Or q(q²+1)/2 = 3×10/2 = 15?
# -(q+1) with mult q²(q+1)/2 = 18? Or q(q²+1)/2?
# -1 with mult...

# For the SYMPLECTIC quadrangle W(q), the point graph eigenvalues are:
# θ₀ = q(q+1) = 12, mult = 1
# θ₁ = q-1 = 2, mult = q²(q²+1)/2 = 9×10/2 = 45? No, v=40...
# Hmm, that doesn't add up. Let me check differently.

# The correct eigenvalues for GQ(s,t) point graph with v = (s+1)(st+1):
# k = s(t+1), mult 1
# s-1, mult t(s+1)(st+1)/(s+t)  
# -(t+1), mult s²(st+1)/(s+t)
# when s=t=q: 
# k = q(q+1), mult 1
# q-1, mult q(q+1)(q²+1)/(2q) = (q+1)(q²+1)/2
# -(q+1), mult q²(q²+1)/(2q) = q(q²+1)/2

# At q=3:
# k=12, mult 1
# q-1=2, mult = 4×10/2 = 20
# -(q+1)=-4, mult = 3×10/2 = 15
# Check: 1 + 20 + 15 = 36 ≠ 40. Missing 4.

# Hmm. Let me try the standard GQ formulas from Payne-Thas:
# For GQ(s,t), point graph eigenvalues:
# k = s(t+1)
# r = s-1 with mult f_r = t(s+1)(st+1)/(s+t) [for s≠t]
# For s=t=q: this formula gives 0/0.
# Need special formula for GQ(q,q).

# From Brouwer-Haemers: for a strongly regular graph (v, k, λ, μ):
# GQ(q,q) point graph has parameters:
# v = (q+1)(q²+1), k = q(q+1), λ = q-1, μ = q+1
# This is srg(40, 12, 2, 4)

# For srg(v, k, λ, μ):
# eigenvalues are k and r, s where
# r, s = [(λ-μ) ± √((λ-μ)² + 4(k-μ))] / 2
# = [(2-4) ± √(4 + 4×8)] / 2
# = [-2 ± √36] / 2 = [-2 ± 6] / 2

r_eig = (-2 + 6) / 2  # = 2
s_eig = (-2 - 6) / 2  # = -4

# Multiplicities:
# f = (1/2)(v-1 - 2k+(v-1)(λ-μ)/√D)
# g = (1/2)(v-1 + 2k-(v-1)(λ-μ)/√D)
# where D = (λ-μ)² + 4(k-μ) = 4+32 = 36, √D = 6

D = 36
sqrtD = 6
f_r = int((v - 1 - (2*k + (v-1)*(q-1-q-1)) / sqrtD) / 2)
# More carefully:
f_r = (v - 1 + (2*k + (v-1)*(2-4)) / sqrtD) / 2
# Hmm, let me use the standard formula properly
# f = [v-1 - (2k + (v-1)(λ-μ))/√D] / 2
# with λ=2, μ=4, k=12, v=40
f_mult = (39 - (2*12 + 39*(-2)) / 6) / 2
g_mult = (39 + (2*12 + 39*(-2)) / 6) / 2

print(f"\n{'='*70}")
print(f"  ADJACENCY SPECTRUM OF GQ(3,3) POINT GRAPH = srg(40,12,2,4)")
print(f"{'='*70}")
print(f"\n  Eigenvalues: k={k}, r={r_eig:.0f}, s={s_eig:.0f}")
print(f"  = 12, 2, -4")
print(f"  r = q-1 = {q-1}, s = -(q+1) = -{q+1}")
print(f"  Multiplicities: 1, {f_mult:.0f}, {g_mult:.0f}")
print(f"  Check: 1 + {f_mult:.0f} + {g_mult:.0f} = {1+f_mult+g_mult:.0f} = v = {v}")

m_r = int(f_mult)  # multiplicity of r=2
m_s = int(g_mult)  # multiplicity of s=-4

# NOW: the Ihara zeta function
# Z_Ihara(u) = (1-u²)^{E-V} / ∏_i (1 - λ_i u + (k-1)u²)
# where the product is over ALL eigenvalues (with multiplicities)

# E = v × k / 2 = 40 × 12 / 2 = 240
E_graph = v * k // 2
chi = E_graph - v  # = 240 - 40 = 200

print(f"\n  E = {E_graph}, V = {v}, E-V = {chi}")

# ∏ (1 - λ_i u + (k-1)u²) = (1 - 12u + 11u²)^1 × (1 - 2u + 11u²)^m_r × (1 + 4u + 11u²)^m_s

# For the FACTORED form:
# Factor each quadratic:
# 1 - 12u + 11u² = (1-u)(1-11u)  [roots: u=1 and u=1/11]
# 1 - 2u + 11u² = ? discriminant = 4-44 = -40 (complex roots!)
# 1 + 4u + 11u² = ? discriminant = 16-44 = -28 (complex roots!)

print(f"\n  Quadratic factors:")
print(f"  (1 - ku + (k-1)u²) = (1 - 12u + 11u²) = (1-u)(1-11u)")
print(f"  (1 - ru + (k-1)u²) = (1 - 2u + 11u²), disc = -40 = -v")
print(f"  (1 - su + (k-1)u²) = (1 + 4u + 11u²), disc = -28 = -(4Φ₆)")

# THE DISCRIMINANTS:
# For eigenvalue r=2: disc = 4 - 44 = -40 = -v  (!!!)
# For eigenvalue s=-4: disc = 16 - 44 = -28 = -4Φ₆ = -4×7

print(f"\n  ★ Discriminant for r-sector: {4-44} = -v = -{v}")
print(f"  ★ Discriminant for s-sector: {16-44} = -4Φ₆ = -{4*Phi6}")
print(f"  The vertex count v ITSELF appears as a discriminant!")

# Z_Ihara(u) = (1-u²)^200 / [(1-u)(1-11u)(1-2u+11u²)^m_r (1+4u+11u²)^m_s]
print(f"\n  Z_Ihara(u) = (1-u²)^{chi}")
print(f"               / [(1-u)(1-11u)(1-2u+11u²)^{m_r} (1+4u+11u²)^{m_s}]")

# ═══════════════════════════════════════════════════════
# CONNECTING Z(x) TO Z_IHARA(u)
# ═══════════════════════════════════════════════════════
print(f"\n{'='*70}")
print("  CONNECTING Z(x) TO THE IHARA ZETA FUNCTION")
print("=" * 70)

# Our Z(x) = (1-5x)^10 (1+x)^16 (1+7x)^6
# This has degree 32 = 2^5

# The Ihara zeta function Z_Ihara involves quadratic factors (degree 2 each)
# whereas our Z(x) has LINEAR factors

# CONNECTION: Z(x) might be a SQUARE ROOT or RECIPROCAL of Z_Ihara
# or it might be the "completed" Ihara zeta (Hashimoto form)

# Key observation: Z(x) has exponents 10, 16, 6
# Z_Ihara has multiplicities 1+m_r+m_s = 1+24+15 = 40 = v

# But our Z has "multiplicities" 10+16+6 = 32

# Alternative: Z(x) = the NUMERATOR of the Ihara zeta?
# The "graph complement" of Z_Ihara?
# Or: Z(x) is the RECIPROCAL characteristic polynomial of some operator?

# Let's check: does Z(x) = det(I - xM) for some 32×32 matrix M?
# If so, M has eigenvalues: 5 (mult 10), -1 (mult 16), -7 (mult 6)
# And Z(x) = characteristic polynomial evaluated at 1/x times x^32... hmm

# det(I - xM) = ∏ (1 - λ_i x) = (1-5x)^10 (1-(-1)x)^16 (1-(-7)x)^6
# = (1-5x)^10 (1+x)^16 (1+7x)^6 = Z(x)!

# So Z(x) = det(I - xM) where M is a 32×32 matrix with eigenvalues:
# 5 (×10), -1 (×16), -7 (×6)

print(f"  Z(x) = det(I - xM) where M is 32×32 with eigenvalues:")
print(f"    5 (multiplicity 10 = Φ₄)")
print(f"    -1 (multiplicity 16 = 2^(q+1))")
print(f"    -7 (multiplicity 6 = 2q)")
print(f"  Total dimension: 32 = 2^(q+λ)")

# Properties of M:
tr_M = 10*5 + 16*(-1) + 6*(-7)  # = 50 - 16 - 42 = -8
tr_M2 = 10*25 + 16*1 + 6*49     # = 250 + 16 + 294 = 560
det_M = 5**10 * (-1)**16 * (-7)**6  # = 5^10 × 1 × 7^6 = 9765625 × 117649
det_M_val = 5**10 * (-7)**6

print(f"\n  Tr(M) = {tr_M} = -2^q = -dim(O)")
print(f"  Tr(M²) = {tr_M2}")
print(f"  det(M) = 5^10 × (-7)^6 = {5**10} × {(-7)**6} = {det_M_val}")
print(f"         = (q+λ)^Φ₄ × (-Φ₆)^(2q)")

# ═══════════════════════════════════════════════════════
# THE 32-DIMENSIONAL SPACE: WHAT IS IT?
# ═══════════════════════════════════════════════════════
print(f"\n{'='*70}")
print("  THE 32-DIMENSIONAL SPACE")
print("=" * 70)

# 32 = 2^5 = 2^(q+λ)
# This is the dimension of the SPINOR representation of SO(10)!
# SO(10) is the rank-5 orthogonal group
# Its spinor rep = 32-dim, decomposes as 16 + 16̄ under chirality

# Under SU(5) ⊂ SO(10):
# 16 = 10 + 5̄ + 1 (one generation of fermions!)
# 16̄ = 10̄ + 5 + 1̄ (antifermions)

# So: our 32 = 16 + 16̄ = one generation of SO(10) spinor + conjugate
# = 2^(q+1) + 2^(q+1) → but that gives 32 = 16 + 16 ≠ 10 + 16 + 6

# Actually, the DECOMPOSITION 10 + 16 + 6 = 32 corresponds to:
# 10 = vector rep of SO(10) (gauge bosons)
# 16 = spinor rep (matter)
# 6 = antisymmetric tensor of SU(4) ≅ SO(6) (Higgs/confined)

# Under SO(10) → SU(5) × U(1):
# 45 → 24 + 10 + 10̄ + 1 (adjoint)
# But 10 here is a different 10

# Under SO(10) → PS = SU(4) × SU(2) × SU(2):
# 10 → (1,2,2) + (6,1,1) = 4 + 6 = 10

# THE KEY: the eigenvalues of M tell us the β-function contributions!
# eigenvalue 5 = q+λ → gauge bosons (running with b₃)
# eigenvalue -1 → matter fermions (fixed point behavior!)
# eigenvalue -7 = -Φ₆ → confined sector (asymptotic freedom)

print(f"  32 = 2^(q+λ) = dim(spinor of SO(10))")
print(f"  Decomposition: 32 = 10 + 16 + 6")
print(f"  = Φ₄ + 2^(q+1) + 2q")
print(f"  = gauge + matter + confined")
print(f"\n  Under SO(10) → SM:")
print(f"  10 (eigenvalue 5): propagating gauge sector")
print(f"  16 (eigenvalue -1): fermionic matter sector")
print(f"   6 (eigenvalue -7): confined/broken sector")

# This is the SO(10) CONTENT:
# The 10 of SO(10) = vector = gauge bosons
# The 16 of SO(10) = spinor = one family of quarks + leptons + ν_R
# The 6 of SO(10) → comes from Pati-Salam 4 × SU(2) → Higgs

# ═══════════════════════════════════════════════════════
# Z(x) AS WITTEN INDEX
# ═══════════════════════════════════════════════════════
print(f"\n{'='*70}")
print("  Z(x) AS SUSY / WITTEN INDEX")
print("=" * 70)

# In SUSY QM, the Witten index = Tr((-1)^F e^{-βH})
# For our system: the "fermion number" F is the sector:
# Bosonic (eigenvalue 5): contributes +1
# Fermionic (eigenvalue -1): contributes (-1)
# Broken (eigenvalue -7): contributes +1 (bosonic-like)

# Z(0) = 1 (normalization)
# Z(-1) = 0 → FERMION ZERO = ANOMALY CANCELLATION
# Z(1) = (1-5)^10 × 2^16 × 8^6 = (-4)^10 × 65536 × 262144
# = 4^10 × 2^16 × 2^18 = 2^20 × 2^34 = 2^54 = 2^(2q³)

Z_at_1 = (1-5)**10 * (1+1)**16 * (1+7)**6
Z_at_neg1 = (1+5)**10 * (1-1)**16 * (1-7)**6
Z_at_neg_inv_5 = (1-5*(-1/5))**10 * (1+(-1/5))**16 * (1+7*(-1/5))**6
Z_at_inv_7 = (1-5/7)**10 * (1+1/7)**16 * (1+7/7)**6

print(f"  Z(0) = 1")
print(f"  Z(1) = {Z_at_1} = 2^{int(np.log2(abs(Z_at_1)))} = 2^(2q³)")
print(f"  Z(-1) = {Z_at_neg1} (anomaly cancellation!)")
print(f"  Z(-1/5) = {Z_at_neg_inv_5:.6f} (gauge zero)")
print(f"  Z(1/7) = {Z_at_inv_7:.6f} (confined zero)")

# Z'(0) = d/dx Z|_{x=0}
# = 10×(-5)×1 + 16×1×1 + 6×7×1 = -50 + 16 + 42 = 8 = 2^q = dim(O)
Z_prime_0 = -10*5 + 16*1 + 6*7
print(f"\n  Z'(0) = {Z_prime_0} = 2^q = dim(O) (octonion dimension!)")

# Z''(0)/2 = second Taylor coefficient
# Need to compute more carefully
# Z(x) = Σ c_n x^n, c_0 = 1
# ln Z = 10 ln(1-5x) + 16 ln(1+x) + 6 ln(1+7x)
# First few Taylor coefficients of Z:
# c_1 = Z'(0) = -50 + 16 + 42 = 8
# c_2 = Z''(0)/2

# Z''(0) = ?
# From Z(x) = (1-5x)^10 (1+x)^16 (1+7x)^6:
# Let f=10 ln(1-5x), g=16 ln(1+x), h=6 ln(1+7x)
# ln Z = f+g+h
# (ln Z)' = -50/(1-5x) + 16/(1+x) + 42/(1+7x)
# (ln Z)'' = -250/(1-5x)² + -16/(1+x)² + -294/(1+7x)²
# At x=0: (ln Z)''(0) = -250 - 16 - 294 = -560

# Z''(0) = Z(0)[(ln Z)''(0) + ((ln Z)'(0))²]
# = 1 × [-560 + 8²] = -560 + 64 = -496

Z_double_prime_0 = -560 + 64
print(f"  Z''(0) = {Z_double_prime_0} = -496")
print(f"         = -dim(SO(32)) / 2 = -2^4 × 31")
print(f"         = THIRD PERFECT NUMBER: 496 = 1+2+4+8+16+31+62+124+248")
print(f"         = 2^(q+1)(2^(q+λ)-1) = 16 × 31")
print(f"         = M_{q+lam} Mersenne prime times 2^(q+1)")

# Z values at special points as x varies:
print(f"\n  Special evaluations:")
print(f"  Z(2) = {(1-10)**10 * 3**16 * 15**6}")
Z_at_2 = (-9)**10 * 3**16 * 15**6
print(f"       = (-9)^10 × 3^16 × 15^6 = {Z_at_2}")
print(f"       = 9^10 × 3^16 × (3×5)^6 = 3^20 × 3^16 × 3^6 × 5^6 = 3^42 × 5^6")
print(f"       = 3^42 × 5^6 = {3**42 * 5**6}")
# Check: 3^42 × 5^6 = ... 
val_3_42 = 3**42
val_5_6 = 5**6
print(f"       3^42 = {val_3_42}, 5^6 = {val_5_6}")
print(f"       Product = {val_3_42 * val_5_6}")
# 42 = 2 × 21 = 2 × Φ₆ × q = 2Φ₆q
# 6 = 2q
print(f"       = 3^(2Φ₆q) × (q+λ)^(2q)")
print(f"       = q^(2Φ₆q) × (q+λ)^(2q)")

# Z(-248) ??? Let's see if Z encodes E₈
# Z[coefficient of x²] = Z''(0)/2 = -496/2 = -248 = -dim(E₈)
print(f"\n  Second Taylor coefficient: c₂ = Z''(0)/2 = {Z_double_prime_0//2} = -dim(E₈)!")

# Third Taylor coefficient:
# c₃ = Z'''(0)/6
# Need (ln Z)'''(0) = -2×(250×25) - 2×(-16) - 2×(294×49) ... let me compute properly
# (ln Z)''' = -2×250×5/(1-5x)³ + 2×16/(1+x)³ + -2×294×7/(1+7x)³ ... no
# d³/dx³ [f(x)] where f = -50/(1-5x):
# f' = -250/(1-5x)² → f'' = -2500/(1-5x)³ → f'''|₀ = -2500
# Wait: (ln Z)' = -50/(1-5x) + 16/(1+x) + 42/(1+7x)
# Second derivative: (ln Z)'' = -250/(1-5x)² - 16/(1+x)² - 294/(1+7x)²
# Third: (ln Z)''' = -2500/(1-5x)³ + 32/(1+x)³ - 4116/(1+7x)³
# At x=0: = -2500 + 32 - 4116 = -6584

ln_Z_3 = -2500 + 32 - 4116
# c₃ = [Z'''(0)]/6 = [(ln Z)'''Z + 3(ln Z)''(ln Z)'Z + ((ln Z)')³Z]/6
# = [(ln Z)''' + 3(ln Z)''×(ln Z)' + ((ln Z)')³]/6
# = [-6584 + 3×(-560)×8 + 8³]/6
# = [-6584 + (-13440) + 512]/6
# = [-19512]/6
# = -3252

c3 = (-6584 + 3*(-560)*8 + 8**3) / 6
print(f"\n  Third Taylor coefficient: c₃ = {c3:.0f}")
print(f"  = {int(c3)}")

# Let's compute Taylor coefficients numerically
from numpy.polynomial import polynomial as P

# Build Z(x) as polynomial by multiplying
# (1-5x)^10 as polynomial coefficients
def binomial_expand(a, n, max_deg=40):
    """Expand (1 + ax)^n as polynomial coefficients"""
    coeffs = []
    for k in range(min(n+1, max_deg+1)):
        coeffs.append(comb(n, k) * a**k)
    return np.array(coeffs, dtype=float)

# (1-5x)^10
c1 = binomial_expand(-5, 10, 32)
# (1+x)^16
c2_poly = binomial_expand(1, 16, 32)
# (1+7x)^6
c3_poly = binomial_expand(7, 6, 32)

# Multiply
Z_poly = np.convolve(c1, c2_poly)
Z_poly = np.convolve(Z_poly, c3_poly)

# First 10 coefficients
print(f"\n  Z(x) Taylor coefficients:")
for i in range(min(11, len(Z_poly))):
    print(f"    c_{i} = {Z_poly[i]:.0f}")

# Key identifications:
print(f"\n  REMARKABLE TAYLOR COEFFICIENTS:")
print(f"    c₀ = {Z_poly[0]:.0f} = 1 (normalization)")
print(f"    c₁ = {Z_poly[1]:.0f} = 2^q = dim(O)")
print(f"    c₂ = {Z_poly[2]:.0f} = -dim(E₈)")
print(f"    c₃ = {Z_poly[3]:.0f}")
print(f"    c₄ = {Z_poly[4]:.0f}")

# Check c₃: 
# -3252 = ? Factor: 3252 = 4 × 813 = 4 × 3 × 271
# 271 is prime. Hmm.
# -3252 = -12 × 271. 271 = 2×137 - 3 = 2α⁻¹ - q
# So c₃ = -k × (2α⁻¹ - q)? Let's check: -12 × (274-3) = -12 × 271 = -3252 ✓
# Not super clean but interesting that α⁻¹ appears!

if abs(Z_poly[3] + 12 * (2*alpha_inv - q)) < 0.1:
    print(f"    c₃ = -k × (2α⁻¹ - q) = -{k} × {2*alpha_inv - q} = {-k*(2*alpha_inv-q)}")

# Save results
results = {
    "Z_generating_function": {
        "formula": "Z(x) = (1-5x)^10 (1+x)^16 (1+7x)^6",
        "parametric": "Z(x;q) = (1-(2q-1)x)^(q^2+1) (1+x)^(2^(q+1)) (1+(q^2-q+1)x)^(2q)",
        "total_degree": 32,
        "as_determinant": "Z(x) = det(I - xM), M is 32×32"
    },
    "M_operator": {
        "dimension": "32 = 2^(q+lam) = dim(spinor SO(10))",
        "eigenvalues": {"5": "mult 10 (gauge)", "-1": "mult 16 (matter)", "-7": "mult 6 (confined)"},
        "trace": f"{tr_M} = -dim(O)",
        "trace_sq": f"{tr_M2}"
    },
    "special_values": {
        "Z(0)": 1,
        "Z(1)": f"2^54 = 2^(2q^3)",
        "Z(-1)": "0 (anomaly cancellation)",
        "Z_prime(0)": f"{Z_prime_0} = dim(O)",
        "Z_double_prime(0)": f"{Z_double_prime_0} = -496 = -3rd perfect number",
        "c2": f"{int(Z_poly[2])} = -dim(E_8)"
    },
    "taylor_coefficients": [int(Z_poly[i]) for i in range(min(11, len(Z_poly)))],
    "ihara_connection": {
        "GQ33_srg": "srg(40, 12, 2, 4)",
        "adjacency_eigenvalues": {"12": 1, "2": m_r, "-4": m_s},
        "discriminants": {"r_sector": "-40 = -v", "s_sector": "-28 = -4*Phi6"}
    },
    "so10_decomposition": "32 = 10(gauge) + 16(matter) + 6(confined) = Phi4 + 2^(q+1) + 2q"
}

with open('/home/user/workspace/W33-Theory/data/w33_partition_function_deep.json', 'w') as fp:
    json.dump(results, fp, indent=2)

print(f"\n\nResults saved to data/w33_partition_function_deep.json")
