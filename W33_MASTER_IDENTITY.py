#!/usr/bin/env python3
"""
THE MASTER IDENTITY
===================

Every result in the entire paper should flow from ONE algebraic identity.

The characteristic polynomial of the W(3,3) adjacency matrix is:
  P(x) = (x-k)(x-r)^f(x-s)^g = (x-12)(x-2)^24(x+4)^15

This polynomial, evaluated at specific points, generates EVERYTHING.
"""

import json
from math import comb, factorial, log, sqrt, pi
from fractions import Fraction

q, v, k, lam, mu = 3, 40, 12, 2, 4
r_val, s_val, f, g = 2, -4, 24, 15
Phi3, Phi4, Phi6, Phi12 = 13, 10, 7, 73
E_val = 240

print("=" * 72)
print("THE MASTER IDENTITY")
print("=" * 72)

# The characteristic polynomial
# P(x) = (x-12)(x-2)^24(x+4)^15

def P(x):
    return (x - k) * (x - r_val)**f * (x + abs(s_val))**g

# ═══════════════════════════════════════════════════════════════
# EVALUATIONS OF P(x) AT W(3,3) SPECIAL POINTS
# ═══════════════════════════════════════════════════════════════

print(f"\nP(x) = (x-{k})(x-{r_val})^{f}(x+{abs(s_val)})^{g}")
print(f"\nEvaluations at special points:")

# P(0) = (-k)(-r)^f(|s|)^g = (-12)(-2)^24 × 4^15
P0 = P(0)
print(f"\n  P(0) = (-{k})×(-{r_val})^{f}×{abs(s_val)}^{g}")
print(f"       = {-k} × {(-r_val)**f} × {abs(s_val)**g}")
print(f"       = {P0}")
print(f"       = -12 × 2^24 × 4^15 = -12 × 16777216 × 1073741824")

# Factor P(0)
# = -k × r^f × |s|^g = -12 × 2^24 × 2^30 = -12 × 2^54
# Wait: 4^15 = 2^30, so P(0) = -12 × 2^24 × 2^30 = -12 × 2^54
# = -3 × 2^56
print(f"       = -k × 2^(f+2g) = -12 × 2^54 = -3 × 2^56")
print(f"       = {-3 * 2**56}")
print(f"  Check: {P0 == -3 * 2**56}")

# P'(0) - the derivative gives the trace condition
# Actually, -P'(0)/P(0) = sum of inverse eigenvalues weighted by multiplicity
# = 1/k + f/r + g/s

# Let's try something more revealing: the LOGARITHMIC DERIVATIVE
# -P'(x)/P(x) = 1/(x-k) + f/(x-r) + g/(x-s)
# This is the RESOLVENT of the adjacency matrix!

print(f"\n  The resolvent (log derivative of P):")
print(f"  R(x) = -P'(x)/P(x) = 1/(x-k) + f/(x-r) + g/(x-s)")
print(f"  R(x) = 1/(x-12) + 24/(x-2) + 15/(x+4)")

# Evaluate the resolvent at x = 0:
R0 = Fraction(1, -k) + Fraction(f, -r_val) + Fraction(g, abs(s_val))
print(f"\n  R(0) = -1/k + -f/r + g/|s|")
print(f"       = -1/{k} - {f}/{r_val} + {g}/{abs(s_val)}")
print(f"       = {Fraction(-1,k)} + {Fraction(-f,r_val)} + {Fraction(g,abs(s_val))}")
print(f"       = {Fraction(-1,k) + Fraction(-f,r_val) + Fraction(g,abs(s_val))}")
# = -1/12 - 12 + 15/4 = -1/12 - 12 + 15/4
# = -1/12 - 144/12 + 45/12 = (-1-144+45)/12 = -100/12 = -25/3
R0_val = Fraction(-1, k) + Fraction(-f, r_val) + Fraction(g, abs(s_val))
print(f"       = {R0_val}")

# Hmm, R(0) = -25/3. Let me try the resolvent at OTHER points.

# At x = 1:
R1 = Fraction(1, 1-k) + Fraction(f, 1-r_val) + Fraction(g, 1+abs(s_val))
print(f"\n  R(1) = 1/(1-k) + f/(1-r) + g/(1+|s|)")
print(f"       = 1/{1-k} + {f}/{1-r_val} + {g}/{1+abs(s_val)}")
print(f"       = {Fraction(1,1-k)} + {Fraction(f,1-r_val)} + {Fraction(g,1+abs(s_val))}")
print(f"       = {Fraction(1,1-k) + Fraction(f,1-r_val) + Fraction(g,1+abs(s_val))}")
# 1/(-11) + 24/(-1) + 15/5 = -1/11 - 24 + 3 = -1/11 - 21 = -232/11
R1_val = Fraction(1, 1-k) + Fraction(f, 1-r_val) + Fraction(g, 1+abs(s_val))
print(f"       = {R1_val}")

# KEY: Try x = -1 (the "critical" point):
Rm1 = Fraction(1, -1-k) + Fraction(f, -1-r_val) + Fraction(g, -1+abs(s_val))
print(f"\n  R(-1) = 1/(-1-k) + f/(-1-r) + g/(-1+|s|)")
print(f"        = 1/{-1-k} + {f}/{-1-r_val} + {g}/{-1+abs(s_val)}")
print(f"        = {Fraction(1,-1-k)} + {Fraction(f,-1-r_val)} + {Fraction(g,-1+abs(s_val))}")
Rm1_val = Fraction(1, -1-k) + Fraction(f, -1-r_val) + Fraction(g, -1+abs(s_val))
print(f"        = {Rm1_val}")
# 1/(-13) + 24/(-3) + 15/3 = -1/13 - 8 + 5 = -1/13 - 3 = -40/13
print(f"        = -40/13 = -v/Φ₃ !!!")

# DISCOVERY: R(-1) = -v/Φ₃!
print(f"\n*** R(-1) = -{v}/{Phi3} = -v/Φ₃ ***")

# What about R at x = q = 3?
Rq = Fraction(1, q-k) + Fraction(f, q-r_val) + Fraction(g, q+abs(s_val))
print(f"\n  R(q) = R(3) = 1/(3-12) + 24/(3-2) + 15/(3+4)")
print(f"       = {Fraction(1,q-k)} + {Fraction(f,q-r_val)} + {Fraction(g,q+abs(s_val))}")
Rq_val = Fraction(1, q-k) + Fraction(f, q-r_val) + Fraction(g, q+abs(s_val))
print(f"       = {Rq_val}")
# = -1/9 + 24 + 15/7 = -1/9 + 24 + 15/7
# = -7/63 + 1512/63 + 135/63 = 1640/63
print(f"       = {Rq_val} = {float(Rq_val):.6f}")

# x = q+1 = μ:
Rmu = Fraction(1, mu-k) + Fraction(f, mu-r_val) + Fraction(g, mu+abs(s_val))
Rmu_val = Fraction(1, mu-k) + Fraction(f, mu-r_val) + Fraction(g, mu+abs(s_val))
print(f"\n  R(μ) = R(4) = 1/(4-12) + 24/(4-2) + 15/(4+4)")
print(f"       = {Rmu_val} = {float(Rmu_val):.6f}")
# = -1/8 + 12 + 15/8 = -1/8 + 12 + 15/8 = 14/8 + 12 = 7/4 + 12 = 55/4
print(f"       = {Rmu_val}")

# x = -μ = -4 = s:
# This is a POLE (x = s), so skip

# x = Φ₃ = 13:
RPhi3 = Fraction(1, Phi3-k) + Fraction(f, Phi3-r_val) + Fraction(g, Phi3+abs(s_val))
print(f"\n  R(Φ₃) = R(13) = 1/(13-12) + 24/(13-2) + 15/(13+4)")
RPhi3_val = Fraction(1, Phi3-k) + Fraction(f, Phi3-r_val) + Fraction(g, Phi3+abs(s_val))
print(f"         = {RPhi3_val} = {float(RPhi3_val):.6f}")
# = 1 + 24/11 + 15/17 = 1 + 24/11 + 15/17
# = 187/187 + 408/187 + 165/187... no, LCD = 187
# Actually: 1 + 24/11 + 15/17 
# LCD = 11×17 = 187
# = 187/187 + (24×17)/187 + (15×11)/187 = (187 + 408 + 165)/187 = 760/187
print(f"         = {RPhi3_val}")
# 760/187 = 40 × 19 / (11 × 17) = v × 19 / ((k-1) × 17)
# Hmm, 760 = v × 19 = 40 × 19. And 187 = 11 × 17 = (k-1) × 17.
print(f"         760 = v × 19, 187 = (k-1) × 17")
print(f"         R(Φ₃) = v × 19 / ((k-1) × 17)")

# ═══════════════════════════════════════════════════════════════
# THE MASTER IDENTITY: R(-1) = -v/Φ₃
# ═══════════════════════════════════════════════════════════════
print(f"\n\n{'═'*72}")
print("THE MASTER IDENTITY")
print(f"{'═'*72}")

print(f"""
The RESOLVENT of the W(3,3) adjacency matrix, evaluated at x = -1:

  R(-1) = 1/(-1-k) + f/(-1-r) + g/(-1+|s|)
        = -1/Φ₃ - f/q + g/q
        = -1/Φ₃ + (g-f)/q
        = -1/Φ₃ + (15-24)/3
        = -1/Φ₃ - 3
        = -1/13 - 3
        = -(1 + 3×13)/13
        = -40/13
        = -v/Φ₃

  *** R(-1) = -v/Φ₃ ***

This identity connects:
  - The SPECTRAL DATA (eigenvalues k, r, s and multiplicities f, g)
  - The VERTEX COUNT v
  - The CYCLOTOMIC VALUE Φ₃
  
  through the RESOLVENT evaluated at the "vacuum point" x = -1.

Let's verify the intermediate steps:
  -1 - k = -13 = -Φ₃
  -1 - r = -3 = -q
  -1 + |s| = 3 = q

So:  R(-1) = 1/(-Φ₃) + f/(-q) + g/q
           = -1/Φ₃ + (-f+g)/q
           = -1/Φ₃ + (g-f)/q

And g - f = 15 - 24 = -9 = -q²

So:  R(-1) = -1/Φ₃ - q²/q = -1/Φ₃ - q

Now: v/Φ₃ = 40/13 and q = 3 = 39/13

So:  R(-1) = -(1 + 39)/13 = -40/13 = -v/Φ₃  ✓

THE IDENTITY IS:

  ┌─────────────────────────────────────────────────┐
  │                                                 │
  │    1/Φ₃ + q = v/Φ₃                             │
  │                                                 │
  │    Which is just: 1 + qΦ₃ = v                  │
  │                                                 │
  │    i.e.: 1 + q(q²+q+1) = q³+q²+q+1 = v       │
  │                                                 │
  │    THIS IS THE DEFINITION OF v = (q⁴-1)/(q-1)  │
  │                                                 │
  └─────────────────────────────────────────────────┘

The resolvent at x = -1 RECOVERS the vertex count formula.
The spectral data knows the graph's size.

But more importantly, the evaluation point x = -1 maps the 
eigenvalues to the CYCLOTOMIC structure:
  k → k+1 = Φ₃  (in the denominator)
  r → r+1 = q   (in the denominator)
  s → |s|-1 = q  (in the denominator)

So the shift x → -(x+1) takes the SRG spectrum to the 
CYCLOTOMIC SPECTRUM. This is the bridge between spectral 
graph theory and number theory.
""")

# ═══════════════════════════════════════════════════════════════
# THE DEEPER IDENTITY: TRACE FORMULAS
# ═══════════════════════════════════════════════════════════════
print(f"{'─'*72}")
print("TRACE FORMULAS: POWERS OF THE ADJACENCY MATRIX")
print(f"{'─'*72}")

# Tr(A^n) = k^n + f·r^n + g·s^n
print(f"\n  Tr(Aⁿ) = kⁿ + f·rⁿ + g·sⁿ = 12ⁿ + 24·2ⁿ + 15·(-4)ⁿ")

for n in range(7):
    tr = k**n + f * r_val**n + g * s_val**n
    print(f"  Tr(A^{n}) = {k**n:>10} + {f*r_val**n:>10} + {g*s_val**n:>10} = {tr:>10}", end="")
    if n == 0:
        print(f"  = v = {v}")
    elif n == 1:
        print(f"  = 0 (traceless!)")
    elif n == 2:
        print(f"  = vk = {v*k}")  
    elif n == 3:
        print(f"  = v(k²+kλ-2k) = ... let me check: {tr}")
    else:
        print()

# Tr(A⁰) = v = 40
# Tr(A¹) = 0 (traceless) - this means k + fr + gs = 0, i.e. 12 + 48 - 60 = 0 ✓
# Tr(A²) = vk = 480 = 2E (number of walks of length 2 = edges × 2)

print(f"\n  Key: Tr(A²) = vk = 2E = a₀ = {v*k} = spectral action coefficient!")
print(f"  Tr(A¹) = 0: the adjacency matrix is TRACELESS")
print(f"  This means: 12 + 24×2 + 15×(-4) = 12 + 48 - 60 = 0 ✓")
print(f"  Tracelessness constrains: k = -(fr + gs) = f|r| - g|s|")

# Tr(A³) = number of triangles × 6
tr3 = k**3 + f * r_val**3 + g * s_val**3
print(f"\n  Tr(A³) = {tr3}")
print(f"  = {tr3}/6 × 6 → number of triangles = {tr3//6}")
# Actually Tr(A³) = 6 × (number of triangles in the graph)
# Tr(A³) = 1728 + 192 - 960 = 960
print(f"  Tr(A³) = {tr3} = 6 × {tr3//6} triangles")
print(f"  = {tr3} = 6 × 160 = 6T where T = 160")
print(f"  T = 160 = q³ + q² + q = q(q²+q+1) ... no")
print(f"  T = 160 = 4 × 40 = μ × v")

# T = μv = 160!
print(f"\n  *** Number of triangles = μ × v = {mu} × {v} = {mu*v} ***")
print(f"  (This was known: T = 160 from the W(3,3) parameter set)")

# Tr(A⁴) 
tr4 = k**4 + f * r_val**4 + g * s_val**4
print(f"\n  Tr(A⁴) = {tr4}")
print(f"  = {k**4} + {f*r_val**4} + {g*s_val**4}")
# 20736 + 384 + 3840 = 24960
print(f"  = {tr4} = v × {tr4//v} = 40 × 624 = v × {tr4//v}")
# 624 = 16 × 39 = s² × (v-1) ... interesting
print(f"  624 = s² × (v-1) = {s_val**2} × {v-1} = {s_val**2 * (v-1)}")

# ═══════════════════════════════════════════════════════════════
# THE ZETA FUNCTION IDENTITY  
# ═══════════════════════════════════════════════════════════════
print(f"\n{'─'*72}")
print("IHARA ZETA FUNCTION OF W(3,3)")
print(f"{'─'*72}")

# The Ihara zeta function of a graph is:
# ζ_G(u)^{-1} = (1-u²)^{E-v} det(I - Au + (k-1)u²I)
# For SRG: this factors completely!

# ζ_W(u)^{-1} = (1-u²)^{E-v} × (1-ku+(k-1)u²) × (1-ru+(k-1)u²)^f × (1-su+(k-1)u²)^g

print(f"  Ihara zeta: ζ_W(u)⁻¹ = (1-u²)^(E-v) × Π(1-λᵢu+(k-1)u²)")
print(f"  E - v = {E_val} - {v} = {E_val - v}")
print(f"  k - 1 = {k-1}")

# The factors (1 - λu + 11u²) for each eigenvalue:
# Eigenvalue k=12: 1 - 12u + 11u²
# Eigenvalue r=2:  1 - 2u + 11u²  (appears f=24 times)
# Eigenvalue s=-4: 1 + 4u + 11u²  (appears g=15 times)

print(f"\n  Factor for k=12: 1 - 12u + 11u²")
print(f"    Discriminant = 144 - 44 = 100, roots u = (12±10)/22 = 1 or 1/11")
print(f"    = (1-u)(1-11u) = (1-u)(1-(k-1)u)")

print(f"\n  Factor for r=2: 1 - 2u + 11u²")
print(f"    Discriminant = 4 - 44 = -40 = -v")
print(f"    Roots: u = (2 ± √(-v))/22 = (2 ± 2i√10)/22 = (1 ± i√10)/11")
print(f"    |u|² = (1+10)/121 = 11/121 = 1/11 = 1/(k-1)")

# DISCOVERY: The discriminant of the r-factor is -v!
print(f"\n  *** DISCRIMINANT OF IHARA r-FACTOR = -v = -40 ***")
print(f"  *** |u_r|² = 1/(k-1) = 1/11 ***")

print(f"\n  Factor for s=-4: 1 + 4u + 11u²")
print(f"    Discriminant = 16 - 44 = -28 = -(v-k) = -28")
print(f"    Roots: u = (-4 ± √(-28))/22 = (-2 ± i√7)/11")
print(f"    |u_s|² = (4+7)/121 = 11/121 = 1/11 = 1/(k-1)")
print(f"    *** SAME MODULUS! Both eigenvalue factors have |u| = 1/√(k-1) ***")

# BOTH non-trivial eigenvalue factors sit on the SAME circle!
print(f"\n  *** ALL non-trivial Ihara zeros lie on the circle |u| = 1/√(k-1) ***")
print(f"  This is the RAMANUJAN PROPERTY of W(3,3)!")
print(f"  W(3,3) satisfies the graph-theoretic Riemann hypothesis!")

# The Ramanujan bound: |eigenvalue| ≤ 2√(k-1) for non-trivial
ramanujan_bound = 2*sqrt(k-1)
print(f"\n  Ramanujan bound: 2√(k-1) = 2√11 = {ramanujan_bound:.6f}")
print(f"  r = 2 ≤ {ramanujan_bound:.2f} ✓")
print(f"  |s| = 4 ≤ {ramanujan_bound:.2f} ✓")
print(f"  Both eigenvalues satisfy the Ramanujan bound.")
print(f"  W(3,3) IS a Ramanujan graph!")

# The connection to the ACTUAL Riemann hypothesis
print(f"\n  *** THE GRAPH-THEORETIC RIEMANN HYPOTHESIS ***")
print(f"  For a k-regular Ramanujan graph, all Ihara zeta zeros")
print(f"  lie on the circle |u| = 1/√(k-1) = 1/√11")
print(f"  This is ANALOGOUS to the Riemann Hypothesis for ζ(s):")
print(f"  all nontrivial zeros on Re(s) = 1/2")
print(f"  W(3,3) satisfies its own Riemann Hypothesis!")

results = {
    'resolvent_at_minus_1': '-v/Φ₃ = -40/13',
    'spectral_to_cyclotomic_bridge': 'x → -(x+1) maps eigenvalues to cyclotomic denominators',
    'trace_A2': f'{v*k} = 2E = a₀',
    'triangles': f'{mu*v} = μv = T',
    'ihara_discriminant_r': f'-v = -40',
    'ihara_discriminant_s': f'-(v-k) = -28',
    'ramanujan_property': True,
    'all_zeros_on_circle': f'|u| = 1/√(k-1) = 1/√11',
    'graph_riemann_hypothesis': True,
}

with open('/home/user/workspace/W33-Theory/checks/W33_MASTER_IDENTITY.json', 'w') as fout:
    json.dump(results, fout, indent=2, default=str)
print(f"\nResults saved.")
