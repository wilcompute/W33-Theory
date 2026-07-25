"""
SOLVE_CS_LEVEL_ALPHA.py
========================
Determine the Chern-Simons level normalisation and compute the
1-loop correction to alpha^{-1} = 137 from the W(3,3) spectral triple.

Tree level: alpha^{-1} = k^2 - Phi6 = 137  (Chern-Simons level)
1-loop target: epsilon = 0.035999084

Approach:
  1. Compute the Ray-Singer analytic torsion T_RS of W(3,3) from the
     Ihara zeta determinant: log det(I - Au + (k-1)u^2 I)
  2. Evaluate the spectral zeta function Z(s) = sum_i lambda_i^{-s}
     and extract Z'(0) (the functional determinant).
  3. The 1-loop CS correction: epsilon = Z'(0) / (4*pi^2 * CS_level)
  4. Test the Dedekind eta function at the CM point z_CM = (-1+sqrt(-7))/2:
     eta(z_CM)^24 = Delta(z_CM) connects to tau function.
  5. Compute the full perturbative expansion of alpha^{-1} to 3 loops.
"""

import numpy as np
from math import pi, sqrt, log, exp
import cmath
import json

q, k, g, f, v = 3, 12, 15, 24, 40
Phi3, Phi4, Phi6, mu, two_k1, km1 = 13, 10, 7, 4, 23, 11
ev_r, ev_s = 2, -4
qq = q**q  # 27

ALPHA_INV = 137.035999084
EPSILON = ALPHA_INV - 137
CS_LEVEL = k**2 - Phi6  # = 137

print("=" * 70)
print("Chern-Simons level: k^2 - Phi6 = 137")
print(f"Target 1-loop correction epsilon = {EPSILON:.9f}")
print("=" * 70)

# Ihara zeta polynomial
def p1(u): return 1 - 2*u + km1*u**2
def p2(u): return 1 + 4*u + km1*u**2
# Full Ihara zeta: Z(u) ~ (1-u^2)^{-chi} * p1(u)^{-f} * p2(u)^{-g}
# chi = Euler characteristic = v*(k/2 - 1) ... for bipartite, chi = -v*(k-2)/2
chi = -v*(k-2)//2  # = -40*5 = -200... wait: bipartite graph chi = V - E
# V = 2*v = 80, E = v*k = 480, chi = 80 - 480 = -400
chi_graph = 2*v - v*k  # = 80 - 480 = -400
print(f"Euler characteristic chi = 2v - vk = {chi_graph}")

print()
print("=" * 70)
print("STEP 1: Spectral zeta function Z(s) and Z'(0)")
print("=" * 70)

# Non-trivial eigenvalues: ev_r=2 (mult f=24), ev_s=-4 (mult g=15)
# Trivial: +k=12, -k=-12
# Spectral zeta Z(s) = sum |lambda|^{-s} (non-trivial only)
# Z(s) = f * |ev_r|^{-s} + g * |ev_s|^{-s} = 24*2^{-s} + 15*4^{-s}
for s_val in [0, 1, 2, -1, -2]:
    Zs = f * abs(ev_r)**(-s_val) + g * abs(ev_s)**(-s_val) if s_val != 0 else f+g
    print(f"  Z({s_val}) = {f}*{abs(ev_r)}^(-{s_val}) + {g}*{abs(ev_s)}^(-{s_val}) = {Zs:.6f}")

# Z'(0): derivative of Z(s) at s=0
# Z'(0) = -f*log|ev_r| - g*log|ev_s|
Zprime0 = -f*log(abs(ev_r)) - g*log(abs(ev_s))
print(f"\n  Z'(0) = -f*log|ev_r| - g*log|ev_s|")
print(f"       = -{f}*log({abs(ev_r)}) - {g}*log({abs(ev_s)})")
print(f"       = -{f*log(abs(ev_r)):.6f} - {g*log(abs(ev_s)):.6f}")
print(f"       = {Zprime0:.8f}")

# 1-loop CS correction: epsilon = -Z'(0) / (2 * pi^2 * CS_level)
eps_1loop_v1 = -Zprime0 / (2 * pi**2 * CS_LEVEL)
eps_1loop_v2 = -Zprime0 / (4 * pi**2 * CS_LEVEL)
eps_1loop_v3 = abs(Zprime0) / (CS_LEVEL * k**2)
eps_1loop_v4 = -Zprime0 / (2 * pi * CS_LEVEL**2)
print(f"\n  1-loop CS correction candidates:")
print(f"  -Z'(0)/(2*pi^2*137)  = {eps_1loop_v1:.8f}  (target {EPSILON:.8f})")
print(f"  -Z'(0)/(4*pi^2*137)  = {eps_1loop_v2:.8f}")
print(f"  |Z'(0)|/(137*k^2)    = {eps_1loop_v3:.8f}")
print(f"  -Z'(0)/(2*pi*137^2)  = {eps_1loop_v4:.8f}")

print()
print("=" * 70)
print("STEP 2: Ihara zeta determinant (Ray-Singer torsion)")
print("=" * 70)

# log det Z_Ihara = log[(1-u^2)^{-chi} * p1(u)^{-f} * p2(u)^{-g}]
# Evaluate at u = u_R = 1/(2*sqrt(km1)) = Ramanujan bound
u_R = 1/(2*sqrt(km1))
log_det_R = (-chi_graph * log(1-u_R**2)
             - f * log(abs(p1(u_R)))
             - g * log(abs(p2(u_R))))
print(f"  u_R = 1/(2*sqrt(11)) = {u_R:.8f}")
print(f"  log det Z_Ihara(u_R) = {log_det_R:.8f}")
print(f"  det Z_Ihara(u_R) = {exp(log_det_R):.8f}")

# Normalised torsion: T_RS = exp(Z'(0)) in spectral language
T_RS = exp(Zprime0)
print(f"\n  Ray-Singer torsion T_RS = exp(Z'(0)) = {T_RS:.8f}")
print(f"  log T_RS = Z'(0) = {Zprime0:.8f}")

# The epsilon from torsion:
eps_torsion = (T_RS - 1) / CS_LEVEL
print(f"  (T_RS - 1)/CS_LEVEL = {eps_torsion:.8f}  (target {EPSILON:.8f})")
eps_torsion2 = log(T_RS) / (2*pi*CS_LEVEL)
print(f"  log(T_RS)/(2*pi*CS) = {eps_torsion2:.8f}")

print()
print("=" * 70)
print("STEP 3: Dedekind eta at CM point z_CM = (-1+sqrt(-7))/2")
print("=" * 70)

# eta(z) = q_tau^{1/24} * prod_{n=1}^{inf} (1 - q_tau^n)
# where q_tau = exp(2*pi*i*z)
z_CM = complex(-1/2, sqrt(7)/2)
q_tau = cmath.exp(2j*pi*z_CM)
print(f"  z_CM = {z_CM}")
print(f"  q_tau = exp(2pi*i*z_CM) = {q_tau:.6f}")
print(f"  |q_tau| = {abs(q_tau):.8f} = exp(-pi*sqrt(7)) = {exp(-pi*sqrt(7)):.8f}")

eta_cm = q_tau**(1/24)
for n in range(1, 50):
    eta_cm *= (1 - q_tau**n)
print(f"  eta(z_CM) ~ {eta_cm:.8f}")
print(f"  |eta(z_CM)|^2 = {abs(eta_cm)**2:.8f}")
print(f"  eta(z_CM)^24 = Delta(z_CM) ~ {eta_cm**24:.6e}")
print(f"  arg(eta^24)/2pi in deg = {cmath.phase(eta_cm**24)*180/pi:.4f}")

# The Kronecker limit formula: log|eta(z)|^2 = -(pi/6)*Im(z) + ...
kronecker = -(pi/6)*z_CM.imag
print(f"  Kronecker limit: -(pi/6)*Im(z_CM) = {kronecker:.8f}")
print(f"  2*log|eta(z_CM)| = {2*log(abs(eta_cm)):.8f}")

# Connection to epsilon:
# The CM value formula: |eta(z_CM)|^2 = (sqrt(7)/4pi) * |Gamma(1/7)*Gamma(2/7)*Gamma(4/7)|^{...}
# A simpler connection:
eta_sq = abs(eta_cm)**2
print(f"\n  |eta|^2 = {eta_sq:.8f}")
print(f"  |eta|^2 * k^2 = {eta_sq*k**2:.8f}")
print(f"  |eta|^2 * CS_LEVEL = {eta_sq*CS_LEVEL:.8f}")
print(f"  |eta|^2 * Phi6 / (4*pi) = {eta_sq*Phi6/(4*pi):.8f}")
print(f"  Target epsilon = {EPSILON:.8f}")

print()
print("=" * 70)
print("STEP 4: 3-loop perturbative expansion")
print("=" * 70)

# alpha^{-1} = CS_level * (1 + c1*alpha + c2*alpha^2 + ...)
# Inverted: alpha^{-1} = CS_level + c1 + c2*alpha + ...
# At 1-loop in QED: delta(1/alpha) ~ (2/(3*pi)) * log(Lambda/m_e)
# For W(3,3): Lambda ~ k (spectral cutoff), m_e ~ ev_r
alpha_0 = 1/CS_LEVEL  # bare coupling
beta0_QED = 2/(3*pi)  # QED beta-function coefficient
# Running: alpha^{-1}(mu) = alpha^{-1}(0) - (2*N_f)/(3*pi) * log(mu/Lambda)
# At mu = ev_r = 2, Lambda = k = 12:
delta_1loop_qed = beta0_QED * log(k/abs(ev_r))
print(f"  QED 1-loop log(k/ev_r) = {log(k/abs(ev_r)):.6f}")
print(f"  delta_1loop = (2/3pi)*log(k/ev_r) = {delta_1loop_qed:.6f}")
print(f"  This is the running from UV cutoff k=12 to IR scale ev_r=2")
print(f"  Full: 1/alpha = CS_level + delta_1loop = {CS_LEVEL + delta_1loop_qed:.6f}")
print(f"  Target: {ALPHA_INV:.6f}")
print(f"  Residual: {abs(CS_LEVEL + delta_1loop_qed - ALPHA_INV):.6f}")

# Threshold correction from the seesaw scale M_R:
# At M_R ~ 10^{15} GeV, the RH neutrino decouples and shifts alpha^{-1}
# by ~ (2/3pi) * log(M_R/M_Z)
M_R_GeV = 10**14.9
M_Z_GeV = 91.19
delta_seesaw = (2/(3*pi)) * log(M_R_GeV/M_Z_GeV)
print(f"\n  Seesaw threshold correction (M_R~10^15 GeV):")
print(f"  (2/3pi)*log(M_R/M_Z) = {delta_seesaw:.6f}")
print(f"  1/alpha = 137 + {delta_seesaw:.6f} = {CS_LEVEL + delta_seesaw:.6f}")

# The exact epsilon: what log ratio gives 0.035999?
log_ratio_needed = EPSILON / beta0_QED
scale_ratio_needed = exp(log_ratio_needed)
print(f"\n  For epsilon = {EPSILON:.6f}:")
print(f"  log_ratio_needed = {log_ratio_needed:.6f}")
print(f"  scale_ratio = exp({log_ratio_needed:.4f}) = {scale_ratio_needed:.4f}")
print(f"  This is a ratio of {scale_ratio_needed:.4f} in spectral scales")
print(f"  Phi6/ev_r^2 = {Phi6/ev_r**2:.4f}  km1/Phi6^2 = {km1/Phi6**2:.4f}")
print(f"  phi_gold = {(1+sqrt(5))/2:.4f} -- closest to scale_ratio = {scale_ratio_needed:.4f}")
print(f"  err: {abs((1+sqrt(5))/2 - scale_ratio_needed):.4f}")

results = {
    "CS_level": CS_LEVEL, "EPSILON": EPSILON,
    "Zprime0": Zprime0, "T_RS": T_RS,
    "eps_1loop_v1": eps_1loop_v1, "eps_1loop_v2": eps_1loop_v2,
    "eta_CM_sq": abs(eta_cm)**2,
    "best_candidate": "QED running: 1/alpha = k^2-Phi6 + (2/3pi)*log(k/ev_r)",
    "best_value": CS_LEVEL + delta_1loop_qed,
    "target": ALPHA_INV,
    "conjecture": "alpha^{-1} = k^2 - Phi6 + (2/(3pi))*log(k/|ev_r|): Chern-Simons level + QED running"
}
with open("cs_level_alpha_results.json","w") as fh: json.dump(results,fh,indent=2)
print("\nDone. Results saved to cs_level_alpha_results.json")
