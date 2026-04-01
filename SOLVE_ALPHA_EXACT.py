"""
SOLVE_ALPHA_EXACT.py
====================
Close the sub-integer gap in alpha^{-1} = k^2 - Phi6 + epsilon = 137.036.

Integer part: k^2 - Phi6 = 144 - 7 = 137  (error 2.6e-4)
Target: epsilon = alpha^{-1} - 137 = 0.035999084

Strategies tested:
  1. Ihara zeta residue at the Ramanujan bound u_R = 1/(2*sqrt(k-1))
  2. Spectral asymmetry: (p2(u) - p1(u)) / (p2(u) + p1(u)) evaluated
     at various spectral points
  3. Eigenvalue moment expansion: sum of ev^{-2} over non-trivial spectrum
  4. The golden ratio / Phi6 correction: Phi6 * (sqrt(5)-2) / k^2
  5. Quantum correction from k+g = q^q = 27:
     epsilon ~ 1/(k^2 - Phi6) * correction_from_27
  6. The Hall conductance analogy: the fine structure constant as
     a spectral Hall conductance of the W(3,3) graph.
"""

import numpy as np
from math import pi, sqrt, log
import json

# W(3,3) parameters
k, g, f, v = 12, 15, 24, 40
Phi3, Phi4, Phi6, mu, two_k1, km1 = 13, 10, 7, 4, 23, 11
q, ev_r, ev_s = 3, 2, -4
qq = q**q  # = 27 = k+g

# Physical
ALPHA_INV = 137.035999084
EPSILON   = ALPHA_INV - 137  # = 0.035999084

print("=" * 70)
print(f"Target epsilon = alpha^{{-1}} - 137 = {EPSILON:.9f}")
print("=" * 70)

# Ihara zeta polynomial factors
def p1(u): return 1 - 2*u + km1*u**2
def p2(u): return 1 + 4*u + km1*u**2

# Key spectral points
u_k    = 1/k                      # = 1/12
u_R    = 1/(2*sqrt(km1))          # Ramanujan bound = 1/(2*sqrt(11))
u_pole1 = (1 + sqrt(1-4*km1*1/4)) / (km1)  # pole of p1 -- complex, skip
u_spec = 1/sqrt(km1)              # = 1/sqrt(11)

print()
print("STRATEGY 1: Ihara zeta residue at Ramanujan bound u_R = 1/(2*sqrt(11))")
print(f"  u_R = {u_R:.8f}")
print(f"  p1(u_R) = {p1(u_R):.8f}")
print(f"  p2(u_R) = {p2(u_R):.8f}")
print(f"  (p2-p1)/(p2+p1) at u_R = {(p2(u_R)-p1(u_R))/(p2(u_R)+p1(u_R)):.8f}")
print(f"  p2(u_R)/p1(u_R) - 1    = {p2(u_R)/p1(u_R)-1:.8f}")
val1 = (p2(u_R) - p1(u_R)) / 2  # = 3*u_R = 3/(2*sqrt(11))
print(f"  (p2-p1)/2 at u_R       = {val1:.8f}  (= 3*u_R = {3*u_R:.8f})")
print(f"  Target epsilon         = {EPSILON:.8f}")

print()
print("STRATEGY 2: Spectral asymmetry scan over u in [0, u_R]")
# Find u* such that some zeta expression = epsilon
best_u, best_val, best_expr, best_err = None, None, None, float('inf')
for n_u in range(1000):
    u = n_u * u_R / 999
    exprs = {
        "(p2-p1)/2": (p2(u)-p1(u))/2,
        "p2*u - p1*u": (p2(u)-p1(u))*u,
        "(p2/p1-1)/k^2": (p2(u)/p1(u)-1)/k**2 if p1(u) != 0 else None,
        "u*(p2-p1)": u*(p2(u)-p1(u)),
        "(p2-p1)*u^2": (p2(u)-p1(u))*u**2,
    }
    for name, val in exprs.items():
        if val is not None and abs(val) > 0:
            err = abs(val - EPSILON)
            if err < best_err:
                best_err = err
                best_val = val
                best_expr = name
                best_u = u
print(f"  Best match: {best_expr} at u={best_u:.6f}")
print(f"  Value = {best_val:.8f},  epsilon = {EPSILON:.8f},  err = {best_err:.2e}")

print()
print("STRATEGY 3: Eigenvalue moment expansion")
# Non-trivial eigenvalues of W(3,3) bipartite adjacency:
# ev_r = 2 with multiplicity f=24
# ev_s = -4 with multiplicity g=15
# trivial: +k=12 (once), -k=-12 (once)
# Spectral zeta function: zeta_spec(s) = sum_lambda lambda^{-s}
# For s=2: sum = f/ev_r^2 + g/ev_s^2 = 24/4 + 15/16 = 6 + 0.9375 = 6.9375
zeta2 = f/ev_r**2 + g/ev_s**2
print(f"  Spectral zeta(2) = {f}/{ev_r**2} + {g}/{ev_s**2} = {zeta2:.6f}")
# Normalised: zeta2 / k^2
print(f"  zeta2/k^2 = {zeta2/k**2:.8f}")
# zeta2 / k^2 / Phi6
print(f"  zeta2/(k^2*Phi6) = {zeta2/(k**2*Phi6):.8f}")
# zeta2 / (k^2 * two_k1)
print(f"  zeta2/(k^2*two_k1) = {zeta2/(k**2*two_k1):.8f}")
# zeta2 - floor(zeta2)
frac_zeta2 = zeta2 - int(zeta2)
print(f"  fractional part of zeta2 = {frac_zeta2:.8f}  (target epsilon = {EPSILON:.8f})")
print(f"  frac(zeta2) / Phi4 = {frac_zeta2/Phi4:.8f}")
print(f"  frac(zeta2) / qq^2 = {frac_zeta2/qq**2:.8f}")

print()
print("STRATEGY 4: Golden ratio and Phi6 correction")
phi_gold = (1+sqrt(5))/2
print(f"  phi_gold = {phi_gold:.8f}")
eps4a = Phi6 * (phi_gold - 1) / k**2
eps4b = (phi_gold - 1) / Phi4
eps4c = 1 / (k**2 * Phi6 * phi_gold)
eps4d = Phi6 / (k**2 * phi_gold**2)
eps4e = (phi_gold - Phi6/k) / k**2
print(f"  Phi6*(phi-1)/k^2       = {eps4a:.8f}")
print(f"  (phi-1)/Phi4           = {eps4b:.8f}")
print(f"  1/(k^2*Phi6*phi)       = {eps4c:.8f}")
print(f"  Phi6/(k^2*phi^2)       = {eps4d:.8f}")
print(f"  (phi-Phi6/k)/k^2       = {eps4e:.8f}")
print(f"  Target epsilon         = {EPSILON:.8f}")
for name, val in [("Phi6*(phi-1)/k^2",eps4a),("(phi-1)/Phi4",eps4b),
                  ("1/(k^2*Phi6*phi)",eps4c),("Phi6/(k^2*phi^2)",eps4d),
                  ("(phi-Phi6/k)/k^2",eps4e)]:
    print(f"  err({name}) = {abs(val-EPSILON):.2e}")

print()
print("STRATEGY 5: k+g = q^q = 27 quantum correction")
# alpha^{-1} = k^2 - Phi6 + 1/(k^2 - Phi6) * correction
# where correction ~ qq / something
corr_target = EPSILON * (k**2 - Phi6)  # = 0.036 * 137 = 4.932
print(f"  correction_target = epsilon * (k^2-Phi6) = {EPSILON} * 137 = {corr_target:.6f}")
print(f"  qq = q^q = k+g = {qq}")
print(f"  qq/5 = {qq/5:.4f}  (5=Phi3-Phi6-1?)")
print(f"  qq/(Phi6-q+q^2) = {qq/(Phi6-q+q**2):.4f}")
print(f"  Phi4/2 = {Phi4/2:.4f}")
print(f"  qq/(k-Phi6+1) = {qq/(k-Phi6+1):.4f}")
print(f"  qq*(phi_gold-2) = {qq*(phi_gold-2):.6f}  (target {corr_target:.6f})")
print(f"  err: {abs(qq*(phi_gold-2)-corr_target):.4f}")
# Direct: epsilon ~ (phi_gold-2)*qq/(k^2-Phi6)
eps5 = qq*(phi_gold-2)/(k**2-Phi6)
print(f"  epsilon ~ qq*(phi-2)/(k^2-Phi6) = {eps5:.8f}  (target {EPSILON:.8f})")
print(f"  err = {abs(eps5-EPSILON):.2e}")

print()
print("STRATEGY 6: Hall conductance / topological analogy")
# The quantum Hall effect: sigma_xy = e^2/(2*pi*hbar) * nu
# alpha = e^2/(4*pi*epsilon_0*hbar*c) -- relates to Hall conductance
# For W(3,3): the Chern number of the spectral flat band?
# The spectral gap is between ev_s^2 = 16 and ev_r^2 = 4 in the
# squared adjacency. The gap ratio:
gap_ratio = ev_s**2 / ev_r**2  # = 16/4 = 4 = mu
print(f"  Spectral gap ratio ev_s^2/ev_r^2 = {gap_ratio} = mu")
# Hall conductance analogy:
# sigma ~ f/(2*pi*(k-1)) = 24/(2*pi*11)
hall = f / (2*pi*km1)
print(f"  f/(2*pi*km1) = 24/(2*pi*11) = {hall:.6f}")
print(f"  1/hall = {1/hall:.4f}  (cf. alpha^{{-1}} = {ALPHA_INV:.4f})")
print(f"  hall * (k^2-Phi6) = {hall*(k**2-Phi6):.4f}")
# The Chern-Simons level: k_CS = k^2 - Phi6 = 137 -- this IS the level!
print(f"\n  TOPOLOGICAL CONJECTURE:")
print(f"  alpha^{{-1}} = k^2 - Phi6 = 137 is the Chern-Simons level of the")
print(f"  W(3,3) spectral topological field theory, exact at tree level.")
print(f"  The sub-integer correction epsilon = {EPSILON:.6f} is the")
print(f"  1-loop quantum correction to the CS level from the spectral")
print(f"  asymmetry: epsilon ~ (p2(u_R)-p1(u_R))*u_R^2 / normalization")
# Evaluate this:
cs_1loop = (p2(u_R)-p1(u_R))*u_R**2
print(f"  (p2-p1)*u_R^2 at u_R = {cs_1loop:.8f}")
print(f"  Target epsilon       = {EPSILON:.8f}")
print(f"  Ratio: epsilon / cs_1loop = {EPSILON/cs_1loop:.4f}")
# Normalised:
cs_norm = cs_1loop / (3*u_R**2)  # divide by 3 = q
print(f"  cs_1loop / q = {cs_norm:.8f}")
print(f"  cs_1loop * k = {cs_1loop*k:.8f}")
print(f"  cs_1loop * km1 = {cs_1loop*km1:.8f}")
# The answer:
best_cs = cs_1loop * km1 / Phi6
print(f"  cs_1loop * km1/Phi6 = {best_cs:.8f}  (target {EPSILON:.8f})")

print()
print("=" * 70)
print("BEST EPSILON CANDIDATES")
print("=" * 70)
candidates_eps = {
    "frac(zeta_spec(2))": frac_zeta2,
    "qq*(phi-2)/(k^2-Phi6)": eps5,
    "Phi6*(phi-1)/k^2": eps4a,
    "(p2-p1)*u_R^2": cs_1loop,
    "(p2-p1)*u_R^2*km1/Phi6": best_cs,
    "zeta2/k^2/two_k1": zeta2/(k**2*two_k1),
}
print(f"{'Expression':40s}  {'Value':14s}  {'Error':12s}")
for name, val in sorted(candidates_eps.items(), key=lambda x: abs(x[1]-EPSILON)):
    print(f"  {name:40s}  {val:.9f}  {abs(val-EPSILON):.3e}")

results = {"EPSILON_target": EPSILON, "candidates": {k: v for k,v in candidates_eps.items()},
           "topological_conjecture": "alpha^{-1} = k^2 - Phi6 is the W(3,3) Chern-Simons level",
           "best_epsilon": sorted(candidates_eps.items(), key=lambda x: abs(x[1]-EPSILON))[0]}
with open("alpha_exact_results.json", "w") as fh:
    json.dump(results, fh, indent=2, default=str)
print("\nDone. Results saved to alpha_exact_results.json")
