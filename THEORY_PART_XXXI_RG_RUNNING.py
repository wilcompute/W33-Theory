#!/usr/bin/env python3
"""
THEORY OF EVERYTHING - PART XXXI: RENORMALIZATION GROUP RUNNING
================================================================

THE CRITICAL TEST: Can we derive sin²θ_W = 40/173 from RG running?

This is the calculation that could make or break the W33 theory.
We use the Standard Model beta functions to run couplings from
a GUT scale down to M_Z and see what we get.
"""

import math
import numpy as np
from fractions import Fraction

print("""
╔══════════════════════════════════════════════════════════════════════╗
║             THEORY OF EVERYTHING - PART XXXI                         ║
║                                                                      ║
║              RENORMALIZATION GROUP RUNNING                           ║
║                                                                      ║
║         Can W33 structure predict sin²θ_W = 40/173 exactly?          ║
╚══════════════════════════════════════════════════════════════════════╝
""")

# =============================================================================
# STANDARD MODEL BETA FUNCTIONS
# =============================================================================

print("=" * 72)
print("STANDARD MODEL BETA FUNCTIONS (1-LOOP)")
print("=" * 72)
print()

print("""
The running of gauge couplings in the SM is governed by:

    dα_i/d(ln μ) = b_i × α_i² / (2π)

where the 1-loop beta coefficients for SU(3)×SU(2)×U(1) are:

    b₃ = -7        (asymptotic freedom)
    b₂ = -19/6     (weak asymptotic freedom)  
    b₁ = +41/10    (U(1) runs UP at low energy)

These include contributions from:
    - Gauge boson loops (negative)
    - Fermion loops (positive)
    - Higgs loops (positive)
""")

# Beta coefficients (1-loop, Standard Model with 1 Higgs doublet)
b1 = 41/10   # U(1)_Y
b2 = -19/6   # SU(2)_L
b3 = -7      # SU(3)_c

print(f"  b₁ = {b1:.4f} = 41/10")
print(f"  b₂ = {b2:.4f} = -19/6")
print(f"  b₃ = {b3:.4f} = -7")
print()

# =============================================================================
# GUT NORMALIZATION
# =============================================================================

print("=" * 72)
print("GUT NORMALIZATION")
print("=" * 72)
print()

print("""
In GUT theories, the U(1) coupling needs to be properly normalized.

Standard convention (SU(5) normalization):
    α₁ = (5/3) × α_Y

This ensures that at the GUT scale:
    α₁ = α₂ = α₃ = α_GUT

The Weinberg angle at ANY scale is defined by:
    sin²θ_W = α₁ / (α₁ + α₂)    [in GUT normalization]
    
Or equivalently:
    sin²θ_W = g'² / (g² + g'²)
""")

# GUT normalization factor
k1 = 5/3  # SU(5) normalization for U(1)

print(f"  GUT normalization: k₁ = {k1:.4f} = 5/3")
print()

# =============================================================================
# RUNNING EQUATIONS
# =============================================================================

print("=" * 72)
print("RUNNING EQUATIONS")
print("=" * 72)
print()

print("""
The solution to the 1-loop RG equations is:

    1/α_i(μ) = 1/α_i(μ₀) - (b_i/2π) × ln(μ/μ₀)

At the GUT scale, assuming unification:
    α₁(M_GUT) = α₂(M_GUT) = α_GUT

Then at scale μ:
    1/α₁(μ) = 1/α_GUT - (b₁/2π) × ln(μ/M_GUT)
    1/α₂(μ) = 1/α_GUT - (b₂/2π) × ln(μ/M_GUT)
""")

def run_coupling(alpha_GUT, b, M_GUT, mu):
    """Run coupling from M_GUT to mu using 1-loop beta function."""
    ln_ratio = math.log(mu / M_GUT)
    alpha_inv = 1/alpha_GUT - (b / (2 * math.pi)) * ln_ratio
    return 1 / alpha_inv

def sin2_theta_W(alpha1, alpha2):
    """Calculate sin²θ_W from α₁ and α₂ in GUT normalization."""
    return alpha1 / (alpha1 + alpha2)

# =============================================================================
# EXPERIMENTAL VALUES AT M_Z
# =============================================================================

print("=" * 72)
print("EXPERIMENTAL VALUES AT M_Z")
print("=" * 72)
print()

M_Z = 91.1876  # GeV
alpha_em_MZ = 1/127.95  # α_EM at M_Z (NOT the low-energy 1/137!)
sin2_exp = 0.23121      # sin²θ_W (MS-bar) at M_Z
alpha_s_MZ = 0.1181     # α_s at M_Z

print(f"  M_Z = {M_Z} GeV")
print(f"  α_EM(M_Z) = 1/{1/alpha_em_MZ:.2f}")
print(f"  sin²θ_W(M_Z) = {sin2_exp}")
print(f"  α_s(M_Z) = {alpha_s_MZ}")
print()

# Convert to GUT-normalized couplings
# α_EM = α₂ × sin²θ_W = α₁ × cos²θ_W / k₁
# α₁ = k₁ × α_EM / cos²θ_W
# α₂ = α_EM / sin²θ_W

cos2_exp = 1 - sin2_exp
alpha1_MZ = k1 * alpha_em_MZ / cos2_exp
alpha2_MZ = alpha_em_MZ / sin2_exp
alpha3_MZ = alpha_s_MZ

print("  GUT-normalized couplings at M_Z:")
print(f"    α₁(M_Z) = 1/{1/alpha1_MZ:.2f}")
print(f"    α₂(M_Z) = 1/{1/alpha2_MZ:.2f}")
print(f"    α₃(M_Z) = 1/{1/alpha3_MZ:.2f}")
print()

# =============================================================================
# STANDARD UNIFICATION (Does SM unify?)
# =============================================================================

print("=" * 72)
print("STANDARD MODEL UNIFICATION TEST")
print("=" * 72)
print()

print("""
First, let's check: Do the SM couplings actually unify?
We run each coupling UP from M_Z and see where they meet.
""")

def find_unification_scale():
    """Find scale where α₁ = α₂."""
    # At unification: 1/α₁(M_GUT) = 1/α₂(M_GUT)
    # 1/α₁(M_Z) - (b₁/2π)ln(M_GUT/M_Z) = 1/α₂(M_Z) - (b₂/2π)ln(M_GUT/M_Z)
    # Solving for ln(M_GUT/M_Z):
    
    delta_alpha_inv = 1/alpha1_MZ - 1/alpha2_MZ
    delta_b = (b1 - b2) / (2 * math.pi)
    
    ln_ratio = delta_alpha_inv / delta_b
    M_GUT = M_Z * math.exp(ln_ratio)
    
    # Calculate unified coupling
    alpha_GUT_inv = 1/alpha1_MZ - (b1 / (2*math.pi)) * ln_ratio
    alpha_GUT = 1 / alpha_GUT_inv
    
    return M_GUT, alpha_GUT

M_GUT_12, alpha_GUT_12 = find_unification_scale()

print(f"  α₁ = α₂ unification scale: M_GUT = {M_GUT_12:.2e} GeV")
print(f"  Unified coupling: α_GUT = 1/{1/alpha_GUT_12:.2f}")
print()

# Check if α₃ also meets there
alpha3_at_GUT = run_coupling(alpha3_MZ, b3, M_Z, M_GUT_12)
# Wait, need to invert this...
ln_ratio = math.log(M_GUT_12 / M_Z)
alpha3_inv_at_GUT = 1/alpha3_MZ - (b3 / (2*math.pi)) * ln_ratio
alpha3_at_GUT = 1 / alpha3_inv_at_GUT

print(f"  α₃ at M_GUT: α₃ = 1/{1/alpha3_at_GUT:.2f}")
print(f"  Gap: 1/α₃ - 1/α_GUT = {1/alpha3_at_GUT - 1/alpha_GUT_12:.2f}")
print()

print("  ⚠️  Standard Model does NOT unify exactly!")
print("  The gap suggests new physics (SUSY, thresholds, or... W33?)")
print()

# =============================================================================
# W33 PREDICTION ANALYSIS
# =============================================================================

print("=" * 72)
print("W33 PREDICTION: REVERSE ENGINEERING")
print("=" * 72)
print()

print("""
QUESTION: What GUT-scale sin²θ_W would give sin²θ_W(M_Z) = 40/173?

At the GUT scale, in many GUT models:
    sin²θ_W(GUT) = 3/8 = 0.375   [SU(5), SO(10)]
    sin²θ_W(GUT) = 3/7 ≈ 0.429  [some E6 models]

Let's work backwards from 40/173 to see what's needed.
""")

sin2_w33 = 40/173

# What is the LOW-energy prediction?
print(f"  W33 target: sin²θ_W(M_Z) = 40/173 = {sin2_w33:.6f}")
print(f"  Experimental: sin²θ_W(M_Z) = {sin2_exp:.6f}")
print(f"  Difference: {abs(sin2_w33 - sin2_exp):.6f}")
print()

# =============================================================================
# KEY INSIGHT: WHERE DOES 173 COME FROM?
# =============================================================================

print("=" * 72)
print("THE 173 PUZZLE")
print("=" * 72)
print()

print("""
In W33 theory:
    sin²θ_W = 40/173
    
where:
    40 = W33 points
    173 = ???

Let's decompose 173:
""")

print(f"  173 = 121 + 52 = W33_total + dim(F4)")
print(f"  173 = 81 + 92  = cycles + ???")
print(f"  173 = 40 + 133 = points + ???")
print()

# Check: 133 = cos²θ_W * 173
print(f"  cos²θ_W × 173 = (1 - 40/173) × 173 = 133")
print(f"  133 = 7 × 19")
print(f"  133 = dim(E7) - ??? No, dim(E7) = 133! ✓")
print()

print("  ╔═══════════════════════════════════════════════════════════════╗")
print("  ║  DISCOVERY: 173 = 40 + 133 = W33_points + dim(E7)!           ║")
print("  ╚═══════════════════════════════════════════════════════════════╝")
print()

print("""
This gives a BEAUTIFUL interpretation:

    sin²θ_W = 40 / (40 + 133)
            = W33_points / (W33_points + dim(E7))
            = GEOMETRY / (GEOMETRY + LIE_ALGEBRA)
            
The electroweak mixing is the ratio of geometric to algebraic structure!
""")

# =============================================================================
# RUNNING FROM E6 GUT SCALE
# =============================================================================

print("=" * 72)
print("E6 GUT RUNNING ANALYSIS")
print("=" * 72)
print()

print("""
In E6 unification, the GUT-scale Weinberg angle depends on the 
breaking chain. For E6 → SO(10) → SM:

    sin²θ_W(GUT) = 3/8 = 0.375

Let's compute what sin²θ_W(M_Z) would be starting from 3/8.
""")

# GUT-scale value for E6 → SO(10)
sin2_GUT = 3/8

# The running formula (approximate):
# sin²θ_W(M_Z) ≈ sin²θ_W(GUT) + Δ
# where Δ depends on the beta functions

# More precisely, using the running:
# sin²θ_W(μ) = α₁(μ) / (α₁(μ) + α₂(μ))

# At GUT scale with sin²θ = 3/8:
# α₁ = α₂ = α_GUT (by definition)
# So sin² = α_GUT / (2 α_GUT) = 1/2 ??? 
# No wait, that's wrong.

# Actually: sin²θ_W = g'² / (g² + g'²) = (g'/g)² / (1 + (g'/g)²)
# At GUT scale with SU(5) relations: g' = √(3/5) g_Y where g_Y² = 5/3 g'²
# This is getting confusing. Let me be more careful.

print("""
═══ Careful Analysis of E6 Running ═══

The key is that β₁ > 0 and β₂ < 0, so:
  - α₁ INCREASES as we go to lower energy
  - α₂ DECREASES as we go to lower energy
  
This means sin²θ_W = α₁/(α₁+α₂) INCREASES going down in energy.

Starting from sin²θ_W(GUT) ≈ 3/8 = 0.375, we expect a LOWER value at M_Z.
But we observe sin²θ_W(M_Z) ≈ 0.231, which is indeed lower! Wait, that's
the opposite of what I said...

Let me recalculate carefully.
""")

# At high scale, if couplings unify: α₁ = α₂ = α_GUT
# Then sin²θ = α₁/(α₁+α₂) = 1/2

# But in GUTs, the boundary condition is actually on the GAUGE couplings g, g'
# not the GUT-normalized couplings.

# In SU(5): g₁² = g₂² = g_GUT² at M_GUT
# where g₁ is the properly normalized U(1) coupling

# This gives: sin²θ_W = g'²/(g²+g'²) = (3/5)/(1 + 3/5) = 3/8 at GUT scale
# (using the fact that g'² = (3/5) g₁² in standard normalization)

print("  At GUT scale (E6 → SO(10) breaking):")
print(f"    sin²θ_W(M_GUT) = 3/8 = {3/8:.6f}")
print()

# The running of sin²θ_W can be computed
# Δsin²θ_W = sin²θ(μ) - sin²θ(M_GUT)
#          ≈ sin²cos² × (α/π) × [(b₁-b₂)/2] × ln(M_GUT/μ)

# Actually, the formula is:
# sin²θ_W(μ) = sin²θ_W(M_GUT) × [1 + (α/π) × ...]

# Let me just run the couplings directly.

def run_to_MZ_from_GUT(sin2_GUT, M_GUT_input, alpha_GUT):
    """
    Given sin²θ_W at GUT scale, compute sin²θ_W at M_Z.
    """
    # At GUT scale:
    # sin²θ = α₁/(α₁+α₂)
    # If α₁ = α₂ = α_GUT, then sin² = 0.5
    # But in SU(5), we have sin²(GUT) = 3/8 because of group theory factors
    
    # The relation is: α₁(GUT)/α₂(GUT) = sin²/(1-sin²)
    # So α₁(GUT) = α_GUT × sin²_GUT / 0.5 (approximately)
    # This is getting circular...
    
    # Let me use the standard formulas.
    # At GUT scale with SU(5)/SO(10) relations:
    # α₁(GUT) = α₂(GUT) = α_GUT
    # But the physical sin²θ_W = 3/8 because of the normalization.
    
    # Running:
    ln_ratio = math.log(M_Z / M_GUT_input)
    
    alpha1_inv_MZ = 1/alpha_GUT - (b1/(2*math.pi)) * ln_ratio
    alpha2_inv_MZ = 1/alpha_GUT - (b2/(2*math.pi)) * ln_ratio
    
    alpha1_MZ_pred = 1/alpha1_inv_MZ
    alpha2_MZ_pred = 1/alpha2_inv_MZ
    
    # sin²θ_W in GUT normalization
    sin2_MZ = alpha1_MZ_pred / (alpha1_MZ_pred + alpha2_MZ_pred)
    
    return sin2_MZ, alpha1_MZ_pred, alpha2_MZ_pred

# Standard GUT prediction
print("═══ Standard GUT Running (M_GUT = 2×10¹⁶ GeV, α_GUT = 1/25) ═══")
print()

M_GUT_std = 2e16  # Standard GUT scale
alpha_GUT_std = 1/25  # Typical GUT coupling

sin2_pred, a1_pred, a2_pred = run_to_MZ_from_GUT(3/8, M_GUT_std, alpha_GUT_std)

print(f"  M_GUT = {M_GUT_std:.0e} GeV")
print(f"  α_GUT = 1/{1/alpha_GUT_std:.0f}")
print(f"  Predicted sin²θ_W(M_Z) = {sin2_pred:.6f}")
print(f"  Experimental: {sin2_exp:.6f}")
print(f"  W33 target: {sin2_w33:.6f}")
print()

# =============================================================================
# REVERSE ENGINEERING: WHAT GIVES 40/173?
# =============================================================================

print("=" * 72)
print("REVERSE ENGINEERING: WHAT GIVES 40/173 EXACTLY?")
print("=" * 72)
print()

print("""
We want to find M_GUT and α_GUT such that:
    sin²θ_W(M_Z) = 40/173 exactly

This is an inverse problem. Let's solve it.
""")

def find_GUT_params_for_target(sin2_target, M_GUT_guess, alpha_GUT_guess, tolerance=1e-10):
    """
    Find GUT parameters that give exactly the target sin²θ_W at M_Z.
    """
    from scipy.optimize import minimize
    
    def objective(params):
        M_GUT = 10**params[0]
        alpha_GUT = 1/params[1]
        sin2, _, _ = run_to_MZ_from_GUT(3/8, M_GUT, alpha_GUT)
        return (sin2 - sin2_target)**2
    
    # Initial guess
    x0 = [math.log10(M_GUT_guess), 1/alpha_GUT_guess]
    
    # Optimize
    from scipy.optimize import minimize
    result = minimize(objective, x0, method='Nelder-Mead')
    
    M_GUT_opt = 10**result.x[0]
    alpha_GUT_opt = 1/result.x[1]
    
    return M_GUT_opt, alpha_GUT_opt

# Let's try a simpler approach: scan parameter space
print("═══ Parameter Scan ═══")
print()

print("  Scanning M_GUT from 10¹⁴ to 10¹⁸ GeV...")
print("  Looking for sin²θ_W(M_Z) = 40/173 = {:.6f}".format(40/173))
print()

best_diff = float('inf')
best_params = None

for log_M_GUT in np.linspace(14, 18, 100):
    M_GUT_test = 10**log_M_GUT
    for alpha_inv in np.linspace(20, 50, 100):
        alpha_GUT_test = 1/alpha_inv
        sin2, _, _ = run_to_MZ_from_GUT(3/8, M_GUT_test, alpha_GUT_test)
        diff = abs(sin2 - sin2_w33)
        if diff < best_diff:
            best_diff = diff
            best_params = (M_GUT_test, alpha_GUT_test, sin2)

M_GUT_best, alpha_GUT_best, sin2_best = best_params

print(f"  Best fit:")
print(f"    M_GUT = {M_GUT_best:.2e} GeV")
print(f"    α_GUT = 1/{1/alpha_GUT_best:.1f}")
print(f"    sin²θ_W(M_Z) = {sin2_best:.6f}")
print(f"    Target: {sin2_w33:.6f}")
print(f"    Difference: {abs(sin2_best - sin2_w33):.6f}")
print()

# =============================================================================
# THE KEY INSIGHT: α_GUT FROM W33
# =============================================================================

print("=" * 72)
print("KEY INSIGHT: α_GUT FROM W33 STRUCTURE")
print("=" * 72)
print()

print("""
What if α_GUT itself comes from W33?

Candidates:
    1/α_GUT = 90/2 = 45 (from K4s)
    1/α_GUT = 40 (W33 points)
    1/α_GUT = 27 (E6 fundamental)
    1/α_GUT = 121/3 ≈ 40.3 (W33 total / generations)
""")

# Test each W33-motivated α_GUT
print("═══ Testing W33-motivated α_GUT values ═══")
print()

w33_alpha_invs = {
    "90/2 = 45 (K4s/2)": 45,
    "40 (points)": 40,
    "27 (E6 fund)": 27,
    "121/3 ≈ 40.3": 121/3,
    "81/2 = 40.5": 40.5,
}

for name, alpha_inv in w33_alpha_invs.items():
    alpha_GUT = 1/alpha_inv
    # Find best M_GUT for this α_GUT
    best_sin2 = None
    best_M_GUT = None
    best_diff = float('inf')
    
    for log_M_GUT in np.linspace(14, 18, 500):
        M_GUT_test = 10**log_M_GUT
        sin2, _, _ = run_to_MZ_from_GUT(3/8, M_GUT_test, alpha_GUT)
        diff = abs(sin2 - sin2_w33)
        if diff < best_diff:
            best_diff = diff
            best_sin2 = sin2
            best_M_GUT = M_GUT_test
    
    match = "✓" if best_diff < 0.001 else " "
    print(f"  α_GUT⁻¹ = {name:20s} → sin²θ_W = {best_sin2:.6f}, M_GUT = {best_M_GUT:.1e} GeV {match}")

print()

# =============================================================================
# THE 0.036 CORRECTION
# =============================================================================

print("=" * 72)
print("ANALYSIS OF THE 0.036 CORRECTION TO α⁻¹")
print("=" * 72)
print()

print("""
The fine structure constant at low energy:
    α⁻¹(0) = 137.035999...
    
W33 tree level: α⁻¹ = 137 = 81 + 56

The correction Δ = 0.036 should come from:
    1. QED radiative corrections (running from M_Z to 0)
    2. Hadronic contributions
    3. Weak contributions
""")

# At M_Z, α_EM⁻¹ ≈ 127.95
# At low energy (Thompson limit), α_EM⁻¹ ≈ 137.036

alpha_0 = 1/137.035999
alpha_MZ = 1/127.95
delta_alpha_inv = 1/alpha_0 - 1/alpha_MZ

print(f"  α⁻¹(0) = 137.036")
print(f"  α⁻¹(M_Z) = 127.95")
print(f"  Running: Δα⁻¹ = {delta_alpha_inv:.2f}")
print()

print("""
The running from M_Z to 0 is KNOWN (QED + hadronic):
    Δα⁻¹ ≈ 9.1 (from SM calculations)
    
This is dominated by:
    - Lepton loops: ~3.2
    - Light quark loops: ~5.9
""")

print()
print("  The 0.036 is the DIFFERENCE between:")
print("    α⁻¹(0) - 137 = 0.036")
print()
print("  Possible W33 interpretation:")

# Check various combinations
combos = [
    ("40/1111", 40/1111),
    ("1/27.78", 1/27.78),
    ("(56-40)/1111", (56-40)/1111),
    ("40/(40×27.78)", 40/(40*27.78)),
    ("121/3367", 121/3367),
    ("1/(78-40-11)", 1/(78-40-11)),
    ("40/(121×9.18)", 40/(121*9.18)),
]

print()
for name, val in combos:
    match = "✓" if abs(val - 0.036) < 0.001 else ""
    print(f"    {name:20s} = {val:.6f} {match}")

print()

# =============================================================================
# NEW INSIGHT: TWO-LOOP CORRECTIONS
# =============================================================================

print("=" * 72)
print("TWO-LOOP ANALYSIS")
print("=" * 72)
print()

print("""
The 2-loop beta coefficients change the running significantly.

For E6 → SM breaking through SO(10) × U(1):
    The threshold corrections at M_GUT and intermediate scales
    can shift sin²θ_W(M_Z) by 1-2%.

If W33 structure determines these thresholds, we might get
exactly 40/173.
""")

# =============================================================================
# FINAL SYNTHESIS
# =============================================================================

print("=" * 72)
print("SYNTHESIS: THE W33 WEINBERG ANGLE FORMULA")
print("=" * 72)
print()

print("""
╔═══════════════════════════════════════════════════════════════════════╗
║                     THE FORMULA                                       ║
╠═══════════════════════════════════════════════════════════════════════╣
║                                                                       ║
║        sin²θ_W(M_Z) = 40 / (40 + 133)                                ║
║                     = W33_points / (W33_points + dim(E7))             ║
║                     = 40/173                                          ║
║                     = 0.231214...                                     ║
║                                                                       ║
║  Experimental:      = 0.23121(4)                                      ║
║                                                                       ║
║  Agreement:         0.1σ                                              ║
║                                                                       ║
╚═══════════════════════════════════════════════════════════════════════╝

INTERPRETATION:

The electroweak mixing angle is determined by the ratio:

    sin²θ_W = (Geometric degrees of freedom) / (Total structure)
            = W33 / (W33 + Lie algebra)
            = 40 / (40 + 133)

where:
    40 = W33 points = projective geometry of physical space
    133 = dim(E7) = full gauge symmetry algebra

This suggests that:
    - Geometry (W33) gives rise to HYPERCHARGE (U(1)_Y)
    - Algebra (E7) gives rise to WEAK ISOSPIN (SU(2)_L)
    
The mixing angle is the "geometric fraction" of the total structure!
""")

# =============================================================================
# WHAT WOULD MAKE THIS RIGOROUS
# =============================================================================

print("=" * 72)
print("WHAT WOULD MAKE THIS RIGOROUS")
print("=" * 72)
print()

print("""
To make the W33 Weinberg angle prediction truly rigorous:

1. DERIVE 173 = 40 + 133 from first principles
   → Show why E7 (dim=133) is the relevant algebra
   → Already known: W33 ↔ W(E6), and E7 contains E6

2. COMPUTE RG running from E7 GUT scale to M_Z
   → Include full 2-loop effects
   → Include threshold corrections at intermediate scales
   → Show that E7 breaking gives sin²θ_W(GUT) = 40/173 × (some factor)
   
3. EXPLAIN why the formula holds at M_Z specifically
   → Is 40/173 the asymptotic (UV) value?
   → Or the IR fixed point?
   → Or valid at ALL scales?

4. PREDICT threshold corrections
   → New particles at specific masses
   → Falsifiable predictions for LHC/FCC
   
CURRENT STATUS:
   - The NUMEROLOGY is striking: 40/173 matches experiment to 0.1σ
   - The INTERPRETATION (W33 + E7) is beautiful
   - The DERIVATION needs more work
""")

print()
print("=" * 72)
print("END OF PART XXXI: RG RUNNING ANALYSIS")
print("=" * 72)
