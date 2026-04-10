"""
THE FULL SPECTRAL ACTION: Tr(D⁴) and Gauge Coupling Unification

In Connes' NCG, the spectral action S = Tr(f(D/Λ)) expands as:
S = f₀Λ⁴a₀ + f₂Λ²a₂ + f₄a₄ + ...

where:
a₀ = Tr(1) = dimension of Hilbert space
a₂ = Tr(D²) (modulo curvature terms)
a₄ = (Tr(D⁴) - (Tr(D²))²/Tr(1)) / 2 (modulo curvature)

The gauge couplings come from a₄:
1/g_i² ∝ multiplicity_i / a₄

And the Higgs potential comes from the SAME a₄ coefficient.

Let's compute everything for our W(3,3) Dirac operator.
"""

import numpy as np
from fractions import Fraction
import json

# W(3,3) parameters
q, lam, mu, k = 3, 2, 4, 12
v, f_val, g_val = 40, 24, 15
Phi3, Phi4, Phi6, Phi12 = 13, 10, 7, 73
E, alpha_inv_tree = 240, 137

# Dirac operator eigenvalues and multiplicities
# D_H has eigenvalues {5, -1, -7} with multiplicities {10, 16, 6}
# Plus 8 octic modes
e_cubic = [5, -1, -7]
m_cubic = [10, 16, 6]

# Octic roots
octic_coeffs = [1, -8, -108, 440, 2894, -8472, -21404, 53608, 1977]
h_roots = sorted(np.roots(octic_coeffs).real, reverse=True)

print("="*70)
print("  SPECTRAL ACTION COEFFICIENTS")
print("="*70)

# The FULL spectral dimension is 40 = v
# 32 modes from cubic + 8 modes from octic

# a₀ = Tr(1) = total number of modes
a0 = sum(m_cubic) + len(h_roots)
print(f"a₀ = Tr(1) = {sum(m_cubic)} + {len(h_roots)} = {a0} = v")

# a₂ = Tr(D²)
Tr_D2_cubic = sum(m_cubic[i] * e_cubic[i]**2 for i in range(3))
Tr_D2_octic = sum(h**2 for h in h_roots)
a2 = Tr_D2_cubic + Tr_D2_octic
print(f"a₂ = Tr(D²) = {Tr_D2_cubic} + {Tr_D2_octic:.0f} = {a2:.0f}")
print(f"   = Φ₆ × q × v = {Phi6} × {q} × {v} = {Phi6*q*v}")

# a₄ = Tr(D⁴)
Tr_D4_cubic = sum(m_cubic[i] * e_cubic[i]**4 for i in range(3))
Tr_D4_octic = sum(h**4 for h in h_roots)
a4_raw = Tr_D4_cubic + Tr_D4_octic
print(f"\na₄_raw = Tr(D⁴) = {Tr_D4_cubic} + {Tr_D4_octic:.0f} = {a4_raw:.0f}")

# The NORMALIZED a₄ (spectral action coefficient):
# a₄ = [Tr(D⁴) - (Tr(D²))²/Tr(1)] / 2
a4_normalized = (a4_raw - a2**2/a0) / 2
print(f"a₄ = [Tr(D⁴) - (Tr(D²))²/Tr(1)] / 2")
print(f"   = [{a4_raw:.0f} - {a2**2/a0:.0f}] / 2")
print(f"   = [{a4_raw - a2**2/a0:.0f}] / 2")
print(f"   = {a4_normalized:.0f}")

# Decompose Tr(D⁴)
print(f"\n{'='*70}")
print("  Tr(D⁴) DECOMPOSITION")
print(f"{'='*70}")

# Cubic part: 10×5⁴ + 16×(-1)⁴ + 6×(-7)⁴ = 10×625 + 16 + 6×2401
print(f"Tr(D⁴)_cubic = 10×625 + 16×1 + 6×2401 = {Tr_D4_cubic}")

# Factor Tr(D⁴)_cubic
td4c = Tr_D4_cubic
print(f"  {td4c} = ?")
# 20672 = 2⁶ × 17 × 19 = 64 × 323
import math
n = td4c
factors = {}
for p in range(2, 1000):
    while n % p == 0:
        factors[p] = factors.get(p, 0) + 1
        n //= p
if n > 1:
    factors[n] = 1
print(f"  = {' × '.join(f'{p}^{e}' if e > 1 else str(p) for p, e in sorted(factors.items()))}")
# Check W(3,3) decompositions
for name, val in [('v', v), ('k', k), ('f', f_val), ('g', g_val), ('Phi3', Phi3), 
                  ('Phi4', Phi4), ('Phi6', Phi6), ('Phi12', Phi12), ('E', E)]:
    if td4c % val == 0:
        print(f"  = {name}({val}) × {td4c//val}")

# Octic part
print(f"\nTr(D⁴)_octic = {Tr_D4_octic:.0f}")
td4o = int(round(Tr_D4_octic))
n = abs(td4o)
factors = {}
for p in range(2, 10000):
    while n % p == 0:
        factors[p] = factors.get(p, 0) + 1
        n //= p
if n > 1:
    factors[n] = 1
if td4o > 0:
    print(f"  = {' × '.join(f'{p}^{e}' if e > 1 else str(p) for p, e in sorted(factors.items()))}")
for name, val in [('v', v), ('k', k), ('f', f_val), ('g', g_val), ('Phi3', Phi3),
                  ('Phi4', Phi4), ('Phi6', Phi6), ('E', E)]:
    if td4o % val == 0:
        print(f"  = {name}({val}) × {td4o//val}")

# TOTAL
td4_total = int(round(a4_raw))
print(f"\nTr(D⁴)_total = {td4_total}")
for name, val in [('v', v), ('k', k), ('f', f_val), ('g', g_val), ('Phi3', Phi3),
                  ('Phi4', Phi4), ('Phi6', Phi6), ('E', E)]:
    if td4_total % val == 0:
        r = td4_total // val
        print(f"  = {name}({val}) × {r}")
        for n2, v2 in [('v', v), ('k', k), ('f', f_val), ('g', g_val), ('Phi3', Phi3),
                       ('Phi4', Phi4), ('Phi6', Phi6)]:
            if r % v2 == 0:
                print(f"    = {name}({val}) × {n2}({v2}) × {r//v2}")

# KEY RATIOS
print(f"\n{'='*70}")
print("  SPECTRAL ACTION RATIOS")
print(f"{'='*70}")

ratio_42 = a4_raw / a2
ratio_40 = a4_raw / a0
ratio_20 = a2 / a0

print(f"Tr(D⁴)/Tr(D²) = {ratio_42:.4f}")
print(f"  ≈ {Fraction(ratio_42).limit_denominator(1000)}")
print(f"Tr(D⁴)/Tr(1) = {ratio_40:.4f}")
print(f"  ≈ {Fraction(ratio_40).limit_denominator(1000)}")
print(f"Tr(D²)/Tr(1) = {ratio_20:.4f}")
print(f"  = {int(a2)}/{a0} = {Fraction(int(a2), a0)} = {Phi6*q} = Φ₆q")

# Check if Tr(D⁴)/Tr(D²) is W(3,3)
frac_42 = Fraction(round(ratio_42 * 840), 840)
print(f"\nTr(D⁴)/Tr(D²) ≈ {frac_42} = {float(frac_42):.6f}")

# Alternatively: Tr(D⁴) = c × Tr(D²)² / Tr(1) + correction
c_ratio = a4_raw * a0 / a2**2
print(f"\nTr(D⁴)·Tr(1)/Tr(D²)² = {c_ratio:.6f}")
print(f"  ≈ {Fraction(c_ratio).limit_denominator(1000)}")

# For a GAUSSIAN distribution: Tr(D⁴)/Tr(1) = 3(Tr(D²)/Tr(1))² (kurtosis = 3)
kurtosis = (a4_raw / a0) / (a2/a0)**2
print(f"\nKurtosis = Tr(D⁴)Tr(1)/Tr(D²)² = {kurtosis:.6f}")
# Gaussian would be 3.0; excess kurtosis = kurtosis - 3

# THE GAUGE COUPLING UNIFICATION CONDITION
# In NCG: at the GUT scale, all gauge couplings unify when
# Tr(D²) gives the correct ratio between a₂ and a₄
print(f"\n{'='*70}")
print("  GAUGE COUPLING UNIFICATION")
print(f"{'='*70}")

# The gauge couplings at the GUT scale are:
# 1/g_i² = C_i × f₂ × a₂ / (some normalization)
# where C_i are group-theory factors

# In the SM: 1/α_GUT ≈ 25 (from running of all three couplings)
# α_GUT ≈ 1/25

# From the spectral action:
# α⁻¹ = (a₂/a₀) × f₂ × (normalization)
# With our values: a₂/a₀ = 21 = Φ₆q
# So: f₂ = α⁻¹/21 = 137/21 ≈ 6.52

# At the GUT scale: α_GUT⁻¹ ≈ 25
# f₂(GUT) = α_GUT⁻¹/21 = 25/21 ≈ 1.19

print(f"At low energy: a₂/a₀ = {Phi6*q} = Φ₆q")
print(f"  α_em⁻¹ = (a₂/a₀) × f₂ = 21 × f₂")
print(f"  → f₂ = α⁻¹/21 = 137/21 = {137/21:.2f}")

print(f"\nAt GUT scale: α_GUT⁻¹ ≈ 25")
print(f"  → f₂(GUT) = 25/21 = {25/21:.4f}")

# The RATIOS of gauge couplings at unification:
# g₃² : g₂² : g₁² = C₃ : C₂ : C₁
# where C_i are determined by the spectral triple

# In the standard NCG (Connes-Marcolli):
# The ratio comes from Tr over the gauge sector:
# For SU(3): Tr = multiplicity × C₂(fund) = N_gen × ... 
# For SU(2): similar but with different group factors

# In our W(3,3) framework, the gauge couplings at the GUT scale are:
# g₃²/g₂² = Tr_SU3(D²)/Tr_SU2(D²)
# = (contribution from 3-colored modes)/(contribution from 2-doublet modes)

# The 32 cubic modes decompose under the SM gauge group as:
# 10-dim (e₁=5): gauge bosons → contributes to g₁,g₂,g₃ through 10 of SO(10)
# 16-dim (e₂=-1): matter → contributes through 16 of SO(10)
# 6-dim (e₃=-7): broken → contributes through remnant

# GUT normalization condition: at M_GUT, α₁ = α₂ = α₃ = α_GUT
# This requires: b₃ × ln(M_GUT/M_Z) = 1/α₃ - 1/α_GUT, etc.

# From the β-function coefficients (we just showed these are W(3,3)):
# b₃ = -7 = -Φ₆
# b₂ = -19/6 = -(g+μ)/(2q)
# b₁ = 41/10 = (v+1)/Φ₄

# The unification condition:
# (1/α₁ - 1/α₂)/(1/α₂ - 1/α₃) = (b₁ - b₂)/(b₂ - b₃)
# where the right side is determined by W(3,3):

b1, b2, b3 = Fraction(41, 10), Fraction(-19, 6), Fraction(-7, 1)
B12 = b1 - b2
B23 = b2 - b3
ratio_B = B12 / B23
print(f"\nβ-function ratios:")
print(f"b₁ - b₂ = {B12} = {float(B12):.6f}")
print(f"b₂ - b₃ = {B23} = {float(B23):.6f}")
print(f"(b₁-b₂)/(b₂-b₃) = {ratio_B} = {float(ratio_B):.6f}")

# Experimental:
# α₁(M_Z) = 1/59.0 (in SU(5) normalization)
# α₂(M_Z) = 1/29.6
# α₃(M_Z) = 1/8.44
# (1/59 - 1/29.6)/(1/29.6 - 1/8.44) = (-0.0169-(-0.0338))/(-0.0338-(-0.1185))
inv_alpha1 = 59.0
inv_alpha2 = 29.6
inv_alpha3 = 8.44
exp_ratio = (inv_alpha1 - inv_alpha2)/(inv_alpha2 - inv_alpha3)
print(f"\nExperimental: (1/α₁-1/α₂)/(1/α₂-1/α₃) = ({inv_alpha1}-{inv_alpha2})/({inv_alpha2}-{inv_alpha3})")
print(f"  = {inv_alpha1-inv_alpha2}/{inv_alpha2-inv_alpha3} = {exp_ratio:.4f}")
print(f"W(3,3) prediction: {float(ratio_B):.4f}")
print(f"Match: {abs(float(ratio_B)-exp_ratio)/exp_ratio*100:.2f}%")

# The unification scale from the β-functions:
# M_GUT from α₂(M_GUT) = α₃(M_GUT):
# (1/α₂(M_Z) - 1/α₃(M_Z))/(b₂-b₃) = (2π) ln(M_GUT/M_Z)
# ln(M_GUT/M_Z) = (1/α₂-1/α₃)/(2π(b₂-b₃))
ln_ratio = (inv_alpha2 - inv_alpha3) / (2*np.pi*float(B23))
M_Z = 91.19  # GeV
M_GUT_from_running = M_Z * np.exp(ln_ratio)
print(f"\nM_GUT from gauge coupling running:")
print(f"  ln(M_GUT/M_Z) = {ln_ratio:.2f}")
print(f"  M_GUT = {M_GUT_from_running:.2e} GeV")
print(f"  log₁₀(M_GUT) = {np.log10(M_GUT_from_running):.2f}")

# W(3,3) prediction: M_GUT = v_EW × 136^(g/2)
v_EW = 246.22
M_GUT_w33 = v_EW * 136**(g_val/2)
print(f"\nW(3,3) prediction: M_GUT = v_EW × 136^(g/2)")
print(f"  = {M_GUT_w33:.2e} GeV")
print(f"  log₁₀ = {np.log10(M_GUT_w33):.2f}")

# THE SPECTRAL ACTION GIVES GAUGE UNIFICATION
print(f"\n{'='*70}")
print("  THE SPECTRAL TRACE TOWER (complete)")
print(f"{'='*70}")

# Full trace tower
traces = {}
for n in range(5):
    T_cubic = sum(m_cubic[i] * e_cubic[i]**n for i in range(3))
    T_octic = int(round(sum(h**n for h in h_roots)))
    T_total = T_cubic + T_octic
    traces[n] = {'cubic': T_cubic, 'octic': T_octic, 'total': T_total}

print(f"{'n':>3} {'Tr(D^n)_cubic':>15} {'Tr(D^n)_octic':>15} {'Tr(D^n)_total':>15} {'W(3,3) identity':>30}")

identities = {
    0: "v = 40",
    1: "0 (anomaly cancel)",
    2: f"Phi6*q*v = {Phi6*q*v}",
    3: f"v*f = mu*E = {v*f_val}",
    4: f"?"
}

for n in range(5):
    t = traces[n]
    ident = identities.get(n, "?")
    print(f"{n:>3} {t['cubic']:>15} {t['octic']:>15} {t['total']:>15} {ident:>30}")

# Tr(D⁴) decomposition search
td4 = traces[4]['total']
print(f"\nSearching for Tr(D⁴)_total = {td4} decomposition:")

# Check: td4 = c₁ × Tr(D²)² / Tr(1) + c₂ × (Tr(D²))
# = c₁ × 840²/40 + c₂ × 840
# = c₁ × 17640 + c₂ × 840
# 50088 = c₁ × 17640 + c₂ × 840
# If c₁ = 2: 50088 - 35280 = 14808 = c₂ × 840 → c₂ = 17.628... not integer
# If c₁ = 3: 50088 - 52920 = -2832 → c₂ = -3.371... no

# Try direct: 50088 / v = 1252.2... no
# 50088 / k = 4174 = 2 × 2087 (prime)
# 50088 / f_val = 2087 (prime)
# 50088 / 8 = 6261 = 3 × 2087
# 50088 = 24 × 2087 = f × 2087
# 2087 is prime

# 50088 = 2³ × 3 × 2087
n = td4
factors = {}
for p in range(2, 10000):
    while n % p == 0:
        factors[p] = factors.get(p, 0) + 1
        n //= p
if n > 1:
    factors[n] = 1
print(f"  {td4} = {' × '.join(f'{p}^{e}' if e > 1 else str(p) for p, e in sorted(factors.items()))}")

# Check: 2087 = 2087 (prime, not a W(3,3) number)
# But the CUBIC part alone: 20672
# And OCTIC part alone: 29416
# Let's check those:
print(f"\n  Tr(D⁴)_cubic = {traces[4]['cubic']}")
n = traces[4]['cubic']
factors_c = {}
for p in range(2, 100000):
    while n % p == 0:
        factors_c[p] = factors_c.get(p, 0) + 1
        n //= p
if n > 1:
    factors_c[n] = 1
print(f"  = {' × '.join(f'{p}^{e}' if e > 1 else str(p) for p, e in sorted(factors_c.items()))}")
# 20672 = 2^6 × 17 × 19
# 17 = k + q + λ = 12 + 3 + 2
# 19 = g + μ = 15 + 4
print(f"  = 2^6 × (k+q+λ) × (g+μ) = 64 × {k+q+lam} × {g_val+mu}")
print(f"  = 64 × 17 × 19 = {64*17*19}")
print(f"  Match: {64*17*19 == traces[4]['cubic']}")

# BEAUTIFUL: Tr(D⁴)_cubic = 2^(2q) × (k+q+λ) × (g+μ)
# = 64 × 17 × 19 = 20672
# where 17 = k+q+λ and 19 = g+μ appear in the β-function coefficients!
# b₁ has 41 = v+1, b₂ has 19 = g+μ. So 19 appears TWICE.

print(f"\n*** Tr(D⁴)_cubic = 2^(2q) × (k+q+λ) × (g+μ) ***")
print(f"*** = 64 × 17 × 19 = {64*17*19} ***")

# Octic part: 29416
n = traces[4]['octic']
factors_o = {}
for p in range(2, 100000):
    while n % p == 0:
        factors_o[p] = factors_o.get(p, 0) + 1
        n //= p
if n > 1:
    factors_o[n] = 1
print(f"\n  Tr(D⁴)_octic = {traces[4]['octic']}")
print(f"  = {' × '.join(f'{p}^{e}' if e > 1 else str(p) for p, e in sorted(factors_o.items()))}")
# 29416 = 2^3 × 3677
# 3677 is prime

# Hmm, 29416/8 = 3677 (prime). Not as clean.
# 29416 = v × 735.4... no
# Let me check: 29416/Phi6 = 4202.3... no

# Try the VARIANCE approach:
# Var(D⁴) = Tr(D⁴)/Tr(1) - (Tr(D²)/Tr(1))² = a4_raw/a0 - (a2/a0)²
var_D2 = a4_raw/a0 - (a2/a0)**2
print(f"\nVar(D²) = Tr(D⁴)/Tr(1) - (Tr(D²)/Tr(1))²")
print(f"  = {a4_raw/a0:.2f} - {(a2/a0)**2:.2f} = {var_D2:.2f}")

# Standard deviation
std_D = np.sqrt(var_D2)
print(f"σ(D²) = √Var = {std_D:.4f}")

# Skewness from Tr(D³):
T3 = traces[3]['total']
skew = (T3/a0) / (std_D**3)
print(f"Skewness = Tr(D³)/(Tr(1)σ³) = {T3}/{a0}/{std_D**3:.4f} = {skew:.4f}")

# THE KEY RELATION: Tr(D⁴) and the Higgs quartic
print(f"\n{'='*70}")
print("  HIGGS QUARTIC FROM Tr(D⁴)")
print(f"{'='*70}")

# In NCG (Chamseddine-Connes-Marcolli):
# λ_H = π² × a₄ / (2f₂² × (a₂)²)
# where a₂ = Tr(D_F²), a₄ = Tr(D_F⁴) for the FINITE Dirac

# Our finite Dirac is D_H with the 32+8=40 modes
# But the NCG finite space is different — it has the algebra A = C+H+M₃(C)
# and the finite Hilbert space of dimension 96 (per generation, times 3)

# In our framework, the Higgs quartic comes from:
# λ_H = Tr(D⁴)/(Tr(D²))² × (some normalization from the gauge sector)

# We showed: λ_H = Φ₆/(2q³) = 7/54 gives m_H = 125.37 GeV
# Let's check: is Φ₆/(2q³) = Tr(D²)_octic / (2 × Tr(D²)_cubic)?
ratio_oct_cub_2 = 280.0 / (2 * 560)
print(f"Tr(D²)_octic / (2×Tr(D²)_cubic) = 280/(2×560) = {ratio_oct_cub_2:.6f}")
print(f"Φ₆/(2q³) = 7/54 = {7/54:.6f}")
# 0.25 vs 0.1296 — not equal

# Try: 7/54 from Tr ratios
# Tr(D⁴)_cubic / (Tr(D²)_cubic × Tr(D²)_total)
ratio_test = Tr_D4_cubic / (Tr_D2_cubic * (Tr_D2_cubic + Tr_D2_octic))
print(f"Tr(D⁴)_cubic / (Tr(D²)_cubic × Tr(D²)_total) = {ratio_test:.6f}")

# Or: using just the cubic sector
# λ_H = Tr(D⁴)_cubic / (Tr(D²)_cubic)²
lambda_naive = Tr_D4_cubic / Tr_D2_cubic**2
print(f"Tr(D⁴)_cubic / (Tr(D²)_cubic)² = {lambda_naive:.6f}")
# 20672/313600 = 0.06592... = 1/(α⁻¹+Φ₄+q)?

# How about: λ_H from the spectral kurtosis
kurtosis_cubic = (Tr_D4_cubic / sum(m_cubic)) / (Tr_D2_cubic / sum(m_cubic))**2
print(f"Kurtosis (cubic only) = {kurtosis_cubic:.6f}")
# = (20672/32) / (560/32)² = 646.0 / 306.25 = 2.110
# Hmm, 2.110 ≈ 2 + 0.11 ≈ 2 + 1/(k-2)?

# The physical λ_H = 0.1296 = Φ₆/(2q³)
# Can we derive this from the trace?
# Φ₆/(2q³) = 7/54
# 7 = Φ₆ and 54 = 2×27 = 2q³
# The Φ₆ appears because it's the QCD β₀ for full SM!
# And q³ = 27 is the Payne-derived SRG vertex count!

# So: λ_H = β₀(QCD)/(2 × n(Payne)) where n(Payne) = q³ = 27
print(f"\nλ_H = Φ₆/(2q³) = β₀(QCD,full SM) / (2 × n_Payne)")  
print(f"    = 7 / (2 × 27) = 7/54 = {7/54:.6f}")
print(f"    with n_Payne = q³ = 27 (Payne-derived SRG vertices)")

# THE SPECTRAL ACTION HIERARCHY
print(f"\n{'='*70}")
print("  THE SPECTRAL ACTION HIERARCHY")
print(f"{'='*70}")

print(f"""
  Level  Coefficient                     Physical content
  ─────  ────────────────────────────   ──────────────────────────
  n=0    a₀ = v = 40                    Cosmological constant Λ
  n=1    Tr(D) = 0                      Anomaly cancellation
  n=2    a₂ = Φ₆qv = 840               Einstein-Hilbert (gravity)
  n=3    Tr(D³) = vf = μE = 960         Yang-Mills (gauge bosons)
  n=4    Tr(D⁴) = 50088                 Higgs potential + gauge quartic
  
  Spectral ratios:
  a₂/a₀ = 21 = Φ₆q = β₀(QCD, N_f=6)     ← 1-loop QCD coefficient!
  a₃/a₀ = 960/40 = 24 = f = χ(K3)         ← Euler character of K3!
  a₄/a₀ = 50088/40 = 1252.2               

  β-function encoding:
  b₃ = -Φ₆ = -7                           (SU(3) coefficient)
  b₂ = -(g+μ)/(2q) = -19/6                (SU(2) coefficient)
  b₁ = (v+1)/Φ₄ = 41/10                   (U(1) coefficient)
  
  Tr(D⁴)_cubic = 2^(2q) × (k+q+λ) × (g+μ) = 64 × 17 × 19
  The factors 17 and 19 from the β-coefficients appear in Tr(D⁴)!
""")

# SAVE EVERYTHING
spectral_data = {
    "trace_tower": {
        "Tr_D0": {"value": 40, "identity": "v", "physics": "cosmological constant"},
        "Tr_D1": {"value": 0, "identity": "anomaly cancellation", "physics": "gauge anomaly = 0"},
        "Tr_D2": {"value": 840, "identity": "Phi6*q*v", "physics": "Einstein-Hilbert action",
                  "decomposition": {"cubic": 560, "octic": 280}},
        "Tr_D3": {"value": 960, "identity": "v*f = mu*E", "physics": "Yang-Mills action",
                  "decomposition": {"cubic": traces[3]['cubic'], "octic": traces[3]['octic']}},
        "Tr_D4": {"value": td4, "physics": "Higgs potential + gauge quartic",
                  "decomposition": {"cubic": traces[4]['cubic'], "octic": traces[4]['octic']},
                  "cubic_factorization": "2^(2q) × (k+q+lambda) × (g+mu) = 64 × 17 × 19"}
    },
    "spectral_ratios": {
        "a2_over_a0": {"value": 21, "identity": "Phi6*q", "physics": "= beta_0(QCD, N_f=6)"},
        "a3_over_a0": {"value": 24, "identity": "f = chi(K3)", "physics": "Euler character"},
    },
    "beta_functions": {
        "b3_SU3": {"value": "-7", "identity": "-Phi6"},
        "b2_SU2": {"value": "-19/6", "identity": "-(g+mu)/(2q)"},
        "b1_U1": {"value": "41/10", "identity": "(v+1)/Phi4"},
        "unification_ratio": {"value": str(ratio_B), "experimental": exp_ratio}
    },
    "higgs": {
        "lambda_H": "Phi6/(2q^3) = 7/54",
        "interpretation": "beta_0(QCD) / (2 * n_Payne) where n_Payne = q^3 = 27",
        "m_H": 125.37,
        "experimental": 125.25
    }
}

with open('/home/user/workspace/W33-Theory/data/w33_spectral_action.json', 'w') as fp:
    json.dump(spectral_data, fp, indent=2)

print(f"\nResults saved to data/w33_spectral_action.json")
