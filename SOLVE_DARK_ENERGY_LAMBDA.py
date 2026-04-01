"""
SOLVE_DARK_ENERGY_LAMBDA.py
============================
Test whether the cosmological constant Lambda and dark energy fraction
Omega_Lambda can be derived from W(3,3) spectral invariants.

The cosmological constant problem: observed Lambda ~ (2.3 meV)^4
while naive QFT predicts Lambda_QFT ~ M_Pl^4 -- a discrepancy of 10^120.

W(3,3) approach: the spectral ratio f/(f+g+k) = 24/51 = 8/17 encodes
a natural partition of degrees of freedom. Test whether:
  - Omega_Lambda ~ f/(f+g+k) or variants
  - Lambda^(1/4) ~ mu_eff_nu * m_nu ~ W(3,3) neutrino energy scale
  - The 10^120 hierarchy factors through the W(3,3) spectral cascade
    as Phi4^{N} for some W(3,3)-distinguished N.

W(3,3) parameter ring:
  k=12, g=15, f=24, v=40, Phi3=13, Phi4=10, Phi6=7, mu=4, two_k1=23, q=3
"""

import numpy as np
import json

# Cosmological constants (Planck 2018 + DESI DR1)
OMEGA_LAMBDA = 0.6847        # dark energy fraction
OMEGA_M = 0.3153             # matter fraction
H0_GEV = 1.445e-42           # Hubble constant in GeV
LAMBDA_QUARTER_EV = 2.3e-3   # Lambda^{1/4} ~ 2.3 meV
LAMBDA_QUARTER_GEV = 2.3e-12 # GeV
M_PLANCK_GEV = 1.22089e19
M_EW_GEV = 246.0             # EW vev
M_W_GEV = 80.377

# W(3,3) parameters
k, g, f, v = 12, 15, 24, 40
Phi3, Phi4, Phi6, mu, two_k1 = 13, 10, 7, 4, 23
q = 3
km1 = 11

print("=" * 70)
print("STEP 1: Omega_Lambda from W(3,3) spectral partition")
print("=" * 70)

print(f"Observed Omega_Lambda = {OMEGA_LAMBDA}")
print(f"Observed Omega_M = {OMEGA_M}")

omega_candidates = {
    "f/(f+g+k)": f/(f+g+k),
    "f/(f+g+v//4)": f/(f+g+v//4),
    "k^2/(k^2+g^2)": k**2/(k**2+g**2),
    "Phi4/(Phi4+Phi6)": Phi4/(Phi4+Phi6),
    "v/(v+f)": v/(v+f),
    "(k+g)/(k+g+f)": (k+g)/(k+g+f),
    "Phi6*Phi4/(Phi6*Phi4+Phi3*mu)": Phi6*Phi4/(Phi6*Phi4+Phi3*mu),
    "f/(v+g)": f/(v+g),
    "(f-g)/(f-g+v//4)": (f-g)/(f-g+v//4),
    "k*(k-1)/(k*(k-1)+g*(g-1))": k*(k-1)/(k*(k-1)+g*(g-1)),
    "km1/(km1+Phi6+mu)": km1/(km1+Phi6+mu),
    "two_k1/(two_k1+Phi3)": two_k1/(two_k1+Phi3),
    "Phi4^2/(Phi4^2+Phi6^2+Phi3)": Phi4**2/(Phi4**2+Phi6**2+Phi3),
}

print(f"{'Expression':50s}  {'Value':8s}  {'Error%':8s}")
best_omega = sorted(omega_candidates.items(), key=lambda x: abs(x[1]-OMEGA_LAMBDA))
for name, val in best_omega[:8]:
    err = abs(val - OMEGA_LAMBDA) / OMEGA_LAMBDA * 100
    marker = " <--- BEST" if name == best_omega[0][0] else ""
    print(f"  {name:50s}  {val:.6f}  {err:8.3f}%{marker}")

print()
print("=" * 70)
print("STEP 2: Lambda^{1/4} from W(3,3) neutrino scale")
print("=" * 70)

print(f"Observed Lambda^{{1/4}} = {LAMBDA_QUARTER_EV*1e3:.2f} meV = {LAMBDA_QUARTER_GEV:.2e} GeV")

# The neutrino mass at W(3,3) fixed point (NH, mu_eff^2=1/4):
m_nu_w33_eV = 0.101 / 3  # ~ 33.7 meV average
print(f"W(3,3) neutrino mass scale (NH, 1/mu): <m_nu> = {m_nu_w33_eV*1e3:.1f} meV")
print(f"Lambda^{{1/4}} / <m_nu> = {LAMBDA_QUARTER_EV / m_nu_w33_eV:.4f}")
print(f"--> Lambda^{{1/4}} ~ (1/14) * m_nu^W33 -- near 1/Phi6=1/7 or 1/two_k1?")

# Lambda = (m_nu^4) * epsilon where epsilon is the suppression
epsilon = (LAMBDA_QUARTER_EV / m_nu_w33_eV)**4
print(f"epsilon = (Lambda^1/4 / m_nu)^4 = {epsilon:.4e}")
# Is epsilon = Phi4^{-N} for some W(3,3) N?
for N in range(1, 20):
    val = 10**(-N)
    err = abs(val - epsilon) / epsilon
    if err < 0.5:
        print(f"  Phi4^(-{N}) = 10^(-{N}) = {val:.2e}  err={err*100:.1f}%")

print()
print("=" * 70)
print("STEP 3: The 10^120 hierarchy via W(3,3) spectral cascade")
print("=" * 70)

lambda_natural_log10 = 4 * np.log10(M_PLANCK_GEV / 1e-12 * 1e-9)  # (M_Pl in eV)^4 / Lambda
# Actually: log10(M_Pl^4 / Lambda) = 4*log10(M_Pl_eV) - 4*log10(Lambda^1/4_eV)
M_Pl_eV = M_PLANCK_GEV * 1e9
log10_fine_tuning = 4 * (np.log10(M_Pl_eV) - np.log10(LAMBDA_QUARTER_EV * 1e9))
print(f"log10(M_Pl^4 / Lambda) = {log10_fine_tuning:.2f}  (the '10^120 problem')")

print(f"\nFactoring through W(3,3) spectral cascade:")
print(f"  Each cascade step T multiplies mu_eff^2 by ~0.52 (from Phi4/Phi6^2 ratio)")
print(f"  Phi4^(k^2-Phi6) = 10^137 -- log10 = {137:.0f}  (alpha^-1 cascade!)")
print(f"  10^137 vs 10^{log10_fine_tuning:.1f}: ratio = 10^{137-log10_fine_tuning:.1f}")
print()

# Number of cascade steps to descend from Planck to Lambda scale
# Each step reduces energy by Phi4^(mu_eff^2) ~ Phi4^(1/4)
step_ratio = Phi4**(1/4)  # ~1.778 per step
N_steps = np.log(M_Pl_eV / (LAMBDA_QUARTER_EV * 1e9)) / np.log(step_ratio)
print(f"Steps to descend from M_Pl to Lambda^1/4 at rate Phi4^(1/4) per step:")
print(f"  N_steps = log(M_Pl/Lambda^1/4) / log(Phi4^1/4) = {N_steps:.2f}")
print(f"  N_steps / (k^2 - Phi6) = {N_steps / 137:.4f}  (in units of alpha^-1)")
print(f"  N_steps / Phi4^Phi6     = {N_steps / 10**7:.4f}  (in units of Phi4^Phi6)")

print()
print("=" * 70)
print("STEP 4: Dark energy as W(3,3) Ihara zeta residue")
print("=" * 70)

# The Ihara zeta function of W(3,3) evaluated at u=1/k:
# Z(u) ~ (1 - u^2)^{-chi/2} * prod_C (1 - u^|C|)^{-1}
# At u = 1/k = 1/12: p1(1/k) and p2(1/k)
u = 1/k
p1_u = 1 - 2*u + 11*u**2
p2_u = 1 + 4*u + 11*u**2
print(f"Ihara zeta factors at u = 1/k = 1/12:")
print(f"  p1(1/12) = 1 - 2/12 + 11/144 = {p1_u:.6f}")
print(f"  p2(1/12) = 1 + 4/12 + 11/144 = {p2_u:.6f}")
print(f"  p2/p1 = {p2_u/p1_u:.6f}")
print(f"  1 - p1/p2 = {1 - p1_u/p2_u:.6f}  (cf. Omega_Lambda = {OMEGA_LAMBDA})")
print(f"  p2/(p1+p2) = {p2_u/(p1_u+p2_u):.6f}  (cf. Omega_Lambda = {OMEGA_LAMBDA})")

# The spectral asymmetry: at u = 1/sqrt(k-1) = 1/sqrt(11)
u_spec = 1/np.sqrt(km1)
p1_spec = 1 - 2*u_spec + 11*u_spec**2
p2_spec = 1 + 4*u_spec + 11*u_spec**2
print(f"\nAt u = 1/sqrt(k-1) = 1/sqrt(11):")
print(f"  p1 = {p1_spec:.6f}")
print(f"  p2 = {p2_spec:.6f}")
print(f"  p2/(p1+p2) = {p2_spec/(p1_spec+p2_spec):.6f}  (cf. Omega_Lambda = {OMEGA_LAMBDA})")
print(f"  p1/(p1+p2) = {p1_spec/(p1_spec+p2_spec):.6f}  (cf. Omega_M = {OMEGA_M})")

print()
print("=" * 70)
print("STEP 5: w0 dark energy equation of state from W(3,3)")
print("=" * 70)

# DESI DR1: w0 = -0.838, wa = -0.62 (best fit)
w0_DESI = -0.838
wa_DESI = -0.62
print(f"DESI DR1: w0 = {w0_DESI}, wa = {wa_DESI}")

# W(3,3) w0 candidate: -(Phi6+mu)/(Phi6+mu+q) = -(7+4)/(7+4+3) = -11/14
w0_w33_1 = -(Phi6 + mu) / (Phi6 + mu + q)
w0_w33_2 = -(km1) / (km1 + q)        # -11/14
w0_w33_3 = -(f - g) / (f)            # -(24-15)/24 = -9/24 = -3/8
w0_w33_4 = -(Phi6 + q) / (Phi6 + q + mu)  # -10/14
w0_w33_5 = -1 + 1/Phi4               # -0.9
w0_w33_6 = -1 + Phi6/k**2            # -1 + 7/144
w0_w33_7 = -(k - mu) / k             # -(12-4)/12 = -8/12 = -2/3
w0_w33_8 = -(two_k1 - mu) / (two_k1) # -19/23

print(f"{'Expression':50s}  {'Value':8s}  {'Err from w0':10s}")
w0_candidates = [
    ("-(Phi6+mu)/(Phi6+mu+q) = -11/14", w0_w33_1),
    ("-km1/(km1+q) = -11/14", w0_w33_2),
    ("-(f-g)/f = -9/24", w0_w33_3),
    ("-(Phi6+q)/(Phi6+q+mu) = -10/14", w0_w33_4),
    ("-1+1/Phi4 = -0.9", w0_w33_5),
    ("-1+Phi6/k^2", w0_w33_6),
    ("-(k-mu)/k = -2/3", w0_w33_7),
    ("-(two_k1-mu)/two_k1 = -19/23", w0_w33_8),
]
for name, val in sorted(w0_candidates, key=lambda x: abs(x[1]-w0_DESI)):
    err = val - w0_DESI
    print(f"  {name:50s}  {val:8.4f}  {err:10.4f}")

results = {
    "best_Omega_Lambda_expression": best_omega[0][0],
    "best_Omega_Lambda_value": best_omega[0][1],
    "Omega_Lambda_error_pct": abs(best_omega[0][1] - OMEGA_LAMBDA)/OMEGA_LAMBDA*100,
    "Ihara_zeta_at_1_over_k": {
        "u": 1/k,
        "p1": p1_u,
        "p2": p2_u,
        "p2_over_p1_plus_p2": p2_u/(p1_u+p2_u),
        "vs_Omega_Lambda": OMEGA_LAMBDA,
    },
    "Ihara_zeta_at_1_over_sqrt_km1": {
        "u": u_spec,
        "p2_over_p1_plus_p2": p2_spec/(p1_spec+p2_spec),
        "p1_over_p1_plus_p2": p1_spec/(p1_spec+p2_spec),
    },
    "fine_tuning_log10": log10_fine_tuning,
    "cascade_steps_to_Lambda": N_steps,
    "DESI_w0": w0_DESI,
    "best_w0_expression": sorted(w0_candidates, key=lambda x: abs(x[1]-w0_DESI))[0][0],
    "best_w0_value": sorted(w0_candidates, key=lambda x: abs(x[1]-w0_DESI))[0][1],
}
with open("dark_energy_results.json", "w") as fh:
    json.dump(results, fh, indent=2)
print("\nDone. Results saved to dark_energy_results.json")
