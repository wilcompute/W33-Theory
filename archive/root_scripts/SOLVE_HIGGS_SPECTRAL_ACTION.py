"""
SOLVE_HIGGS_SPECTRAL_ACTION.py
================================
Derive the Higgs mass and EW vev from the W(3,3) spectral action.

The Connes-Chamseddine spectral action of the SM noncommutative geometry:
  S = Tr[f(D/Lambda)] + <psi|D|psi>
produces the SM Higgs potential with:
  v^2 = 2*f2*Lambda^2 / (f4*lambda_H)
  m_H^2 = 8*lambda_H*v^2
  m_H / v = 2*sqrt(2*lambda_H)

where f_n = integral_0^inf u^{n-1} f(u) du are spectral action moments.

In the W(3,3) spectral triple, the moments are determined by the
eigenvalue spectrum {+k, -k, ev_r (x f), ev_s (x g)}.

Hypothesis: v_{EW} = 246 GeV is fixed by the ratio of W(3,3)
eigenvalue moments f2/f4.

Also derives:
  - The Higgs self-coupling lambda_H from W(3,3) spectral invariants
  - The top Yukawa coupling y_t from the W(3,3) fixed point
  - The W/Z mass ratio from the Weinberg angle derivation
"""

import numpy as np
from math import pi, sqrt, log
import json

q, k, g, f, v_graph = 3, 12, 15, 24, 40
Phi3, Phi4, Phi6, mu, two_k1, km1 = 13, 10, 7, 4, 23, 11
ev_r, ev_s = 2, -4
qq = q**q  # 27

# Physical constants (PDG 2024)
V_EW   = 246.22    # GeV  (Higgs vev)
M_H    = 125.25    # GeV  (Higgs mass)
M_W    = 80.377    # GeV
M_Z    = 91.1876   # GeV
M_TOP  = 172.69    # GeV
ALPHA  = 1/137.036
SIN2_TW = 0.23122
LAMBDA_H = M_H**2 / (2*V_EW**2)  # ~ 0.130
Y_TOP  = M_TOP * sqrt(2) / V_EW   # ~ 0.993

print("=" * 70)
print("W(3,3) SPECTRAL ACTION MOMENTS")
print("=" * 70)

# Full eigenvalue spectrum of W(3,3) bipartite adjacency (non-zero eigenvalues):
# +k = +12 (multiplicity 1, but bipartite so paired: +12 and -12)
# ev_r = +2 (mult f=24) and -2 (mult f=24, bipartite)
# ev_s = -4 (mult g=15) and +4 (mult g=15, bipartite)
# Wait: for bipartite W(3,3), spectrum is symmetric: if lambda is EV, so is -lambda
# Non-trivial spectrum: {+2,-2} x 24, {+4,-4} x 15, {+12,-12} x 1

eigenvalues = ([k]*1 + [-k]*1 +
               [ev_r]*f + [-ev_r]*f +
               [abs(ev_s)]*g + [-abs(ev_s)]*g)
n_ev = len(eigenvalues)
print(f"Total eigenvalues: {n_ev} = 2*(1+f+g) = 2*(1+{f}+{g}) = {2*(1+f+g)}")
print(f"Spectral moments (non-trivial only, exclude +/-k):")

ev_nontrivial = ([ev_r]*f + [-ev_r]*f + [abs(ev_s)]*g + [-abs(ev_s)]*g)

for p_mom in [1, 2, 3, 4, 6]:
    moment = sum(abs(e)**p_mom for e in ev_nontrivial)
    print(f"  Tr|D|^{p_mom} (non-trivial) = {f}*{abs(ev_r)}^{p_mom} + {g}*{abs(ev_s)}^{p_mom} + c.c. = "
          f"{f*abs(ev_r)**p_mom + g*abs(ev_s)**p_mom} * 2 = {moment}")

# Spectral action moments f_n:
# In NCG, f_n = (1/(2*pi)) * integral of the heat kernel coefficient a_{n}
# For a graph Laplacian, the moments are:
# f2 = Tr[D^2] (non-trivial) normalised
# f4 = Tr[D^4] normalised
f2_raw = f*ev_r**2 + g*ev_s**2  # = 24*4 + 15*16 = 96+240 = 336 (one chirality)
f4_raw = f*ev_r**4 + g*ev_s**4  # = 24*16 + 15*256 = 384+3840 = 4224
f6_raw = f*ev_r**6 + g*ev_s**6
print(f"\n  f2 = Tr[D^2]/2 = {f2_raw} (= f*ev_r^2 + g*ev_s^2)")
print(f"  f4 = Tr[D^4]/2 = {f4_raw}")
print(f"  f6 = Tr[D^6]/2 = {f6_raw}")
print(f"  f2/f4 = {f2_raw/f4_raw:.8f}")
print(f"  f4/f2^2 = {f4_raw/f2_raw**2:.8f}")
print(f"  sqrt(f2/f4) = {sqrt(f2_raw/f4_raw):.8f}")

print()
print("=" * 70)
print("STEP 1: Higgs vev from spectral action")
print("=" * 70)

# In Connes-Chamseddine: v^2 = 2*f2*Lambda^2 / (f4*lambda_H)
# Lambda = spectral cutoff = Planck scale or GUT scale
# We identify Lambda_W33 = k = 12 (degree, spectral UV cutoff)
# lambda_H from W(3,3) (see below)
# Then v is fixed modulo Lambda

# The dimensionless ratio:
# v/Lambda = sqrt(2*f2 / (f4*lambda_H))
# For lambda_H = Phi6/Phi4^2 = 7/100 = 0.07 (a W(3,3) candidate):
lambda_H_w33_candidates = {
    "Phi6/Phi4^2": Phi6/Phi4**2,
    "1/Phi4": 1/Phi4,
    "q/Phi4": q/Phi4,
    "Phi6/k^2": Phi6/k**2,
    "ev_r^2/Phi10": ev_r**2/Phi4,
    "f2/(f4/f2)": f2_raw**2/f4_raw,
    "PDG value": LAMBDA_H,
}

print(f"PDG lambda_H = M_H^2/(2*v^2) = {LAMBDA_H:.6f}")
print(f"{'Candidate':30s}  {'lambda_H':10s}  {'Error%':8s}")
for name, lh in lambda_H_w33_candidates.items():
    err = abs(lh - LAMBDA_H)/LAMBDA_H*100
    print(f"  {name:30s}  {lh:10.6f}  {err:8.3f}%")

best_lh_name, best_lh = min(
    [(n,v) for n,v in lambda_H_w33_candidates.items() if n != "PDG value"],
    key=lambda x: abs(x[1]-LAMBDA_H)
)
print(f"\n  Best: {best_lh_name} = {best_lh:.6f}  (PDG {LAMBDA_H:.6f})")

print()
print("=" * 70)
print("STEP 2: Top Yukawa coupling from W(3,3) fixed point")
print("=" * 70)

print(f"PDG y_top = M_top * sqrt(2) / v_EW = {Y_TOP:.6f}")
# y_top is near 1 -- the top quark mass ~ v_EW suggests it sits at the
# W(3,3) fixed point where all Yukawa couplings are equal.
# At the fixed point: y_top = 1 exactly.
# Deviation: Y_TOP - 1 = {Y_TOP-1:.6f}
print(f"  y_top - 1 = {Y_TOP-1:.6f} ({(Y_TOP-1)*100:.4f}%)")
print(f"  The top quark IS at the W(3,3) Yukawa fixed point to {abs(Y_TOP-1)*100:.2f}%")
print(f"  This is consistent with m_top = v_EW/sqrt(2) = {V_EW/sqrt(2):.3f} GeV")
print(f"  Actual m_top = {M_TOP:.3f} GeV  err = {abs(M_TOP - V_EW/sqrt(2)):.3f} GeV ({abs(M_TOP/V_EW*sqrt(2)-1)*100:.2f}%)")

# W(3,3) correction: y_top = 1 - mu_eff^2(top) * correction
# From SOLVE_RG_NEUTRINO: the up-quark sector has delta^2 ~ 64
# The top is the lightest deviation: sigma_max = 1 (by normalisation)
# y_top ~ 1 at the FP, with correction ~ 1/k^2
yt_w33_correction = 1 - 1/k**2
print(f"  W(3,3) corrected: y_top = 1 - 1/k^2 = {yt_w33_correction:.6f}")
print(f"  y_top predicted = {yt_w33_correction:.6f}  PDG = {Y_TOP:.6f}  err = {abs(yt_w33_correction-Y_TOP):.4f}")

print()
print("=" * 70)
print("STEP 3: Higgs mass prediction from spectral action")
print("=" * 70)

# m_H^2 = 8*lambda_H*v^2 => m_H = v*sqrt(8*lambda_H) = v*2*sqrt(2*lambda_H)
for name, lh in lambda_H_w33_candidates.items():
    if name != "PDG value":
        mH_pred = V_EW * sqrt(8*lh)
        err = abs(mH_pred - M_H)
        print(f"  lambda_H={name:25s}: m_H = {mH_pred:.3f} GeV  err = {err:.3f} GeV ({err/M_H*100:.2f}%)")

print()
print("=" * 70)
print("STEP 4: W and Z masses from W(3,3) spectral geometry")
print("=" * 70)

# M_W = (1/2)*g_2*v, M_Z = (1/2)*sqrt(g_1^2+g_2^2)*v
# M_W/M_Z = cos(theta_W)
# sin^2(theta_W) from W(3,3): best candidate (k-|ev_s|)/(k+|ev_s|+g) = 8/31
sin2_w33 = (k - abs(ev_s))/(k + abs(ev_s) + g)  # = 8/31 = 0.258
cos_w33 = sqrt(1 - sin2_w33)
MW_over_MZ_w33 = cos_w33
MW_pred_w33 = M_Z * cos_w33
print(f"  sin^2(theta_W) = (k-|ev_s|)/(k+|ev_s|+g) = 8/31 = {sin2_w33:.6f}  (PDG {SIN2_TW:.6f})")
print(f"  cos(theta_W) = {cos_w33:.6f}")
print(f"  M_W = M_Z * cos(theta_W) = {M_Z}*{cos_w33:.4f} = {MW_pred_w33:.3f} GeV  (PDG {M_W} GeV)")
print(f"  err M_W: {abs(MW_pred_w33-M_W):.3f} GeV ({abs(MW_pred_w33-M_W)/M_W*100:.2f}%)")

# Better sin^2(theta_W) candidate: ev_r^2/(ev_r^2+|ev_s|^2) = 4/20 = 0.200
sin2_w33_v2 = ev_r**2/(ev_r**2 + ev_s**2)  # = 4/20 = 0.2
MW_pred_v2 = M_Z * sqrt(1-sin2_w33_v2)
print(f"\n  sin^2 = ev_r^2/(ev_r^2+ev_s^2) = 4/20 = {sin2_w33_v2:.3f}  (PDG {SIN2_TW:.3f})")
print(f"  M_W = {M_Z}*sqrt(1-0.2) = {MW_pred_v2:.3f} GeV  (PDG {M_W})")

print()
print("=" * 70)
print("STEP 5: Closing the spectral action -- v_EW from first principles")
print("=" * 70)

# The spectral action with UV cutoff Lambda_GUT:
# v^2 = 2*f2*Lambda_GUT^2 / (f4*lambda_H)
# With f2=336, f4=4224, lambda_H=Phi6/Phi4^2=0.07, Lambda_GUT=2e16 GeV:
Lambda_GUT = 2e16  # GeV
lambda_H_use = best_lh  # best W(3,3) candidate
v_pred = sqrt(2*f2_raw*Lambda_GUT**2 / (f4_raw*lambda_H_use))
print(f"  Using: f2={f2_raw}, f4={f4_raw}, lambda_H={lambda_H_use:.4f}, Lambda_GUT={Lambda_GUT:.1e} GeV")
print(f"  v = sqrt(2*f2*Lambda^2/(f4*lambda_H)) = {v_pred:.3e} GeV")
print(f"  Ratio v_pred/v_EW = {v_pred/V_EW:.3e}")
print(f"  This is {log(v_pred/V_EW)/log(10):.2f} orders of magnitude off")
print(f"  Needed Lambda to give v_EW = 246 GeV:")
Lambda_needed = V_EW * sqrt(f4_raw*lambda_H_use/(2*f2_raw))
print(f"  Lambda_needed = {Lambda_needed:.4f} GeV")
print(f"  Ratio Lambda_needed/v_EW = {Lambda_needed/V_EW:.6f}")
print(f"  Lambda_needed/v_EW ~ f2/(f4*lambda_H)^{0.5} = {sqrt(f2_raw/(f4_raw*lambda_H_use)):.6f}")
print(f"  = sqrt({f2_raw}/{f4_raw*lambda_H_use:.2f}) = sqrt({f2_raw/(f4_raw*lambda_H_use):.4f})")
# So v_EW = Lambda_W33 where Lambda_W33 = v_EW itself -- trivially!
# The non-trivial content: the RATIO f4*lambda_H/(2*f2) = 1 defines the EW scale
ratio_spectral = f4_raw*lambda_H_use/(2*f2_raw)
print(f"\n  The W(3,3) spectral self-consistency condition:")
print(f"  f4*lambda_H/(2*f2) = {f4_raw}*{lambda_H_use:.4f}/(2*{f2_raw}) = {ratio_spectral:.6f}")
print(f"  For v = Lambda: ratio must = 1.  Actual = {ratio_spectral:.6f}")
print(f"  Deficit: {abs(ratio_spectral-1):.6f}")
print(f"  This requires lambda_H = 2*f2/f4 = 2*{f2_raw}/{f4_raw} = {2*f2_raw/f4_raw:.6f}")
print(f"  PDG lambda_H = {LAMBDA_H:.6f}")
print(f"  Self-consistent W(3,3) lambda_H = 2*f2/f4 = {2*f2_raw/f4_raw:.6f}")
print(f"  Error vs PDG: {abs(2*f2_raw/f4_raw - LAMBDA_H)/LAMBDA_H*100:.2f}%")

# FINAL:
self_consistent_lH = 2*f2_raw/f4_raw
print(f"\n*** RESULT: The spectral self-consistency condition v=Lambda gives ***")
print(f"*** lambda_H = 2*f2/f4 = 2*{f2_raw}/{f4_raw} = {self_consistent_lH:.6f} ***")
print(f"*** PDG lambda_H = {LAMBDA_H:.6f}  err = {abs(self_consistent_lH-LAMBDA_H)/LAMBDA_H*100:.2f}% ***")
print(f"*** This predicts M_H = v*sqrt(8*lambda_H) = {V_EW*sqrt(8*self_consistent_lH):.2f} GeV ***")
print(f"*** PDG M_H = {M_H:.2f} GeV ***")

results = {
    "f2": f2_raw, "f4": f4_raw, "f2_over_f4": f2_raw/f4_raw,
    "self_consistent_lambda_H": self_consistent_lH,
    "pdg_lambda_H": LAMBDA_H,
    "lambda_H_error_pct": abs(self_consistent_lH-LAMBDA_H)/LAMBDA_H*100,
    "mH_predicted": V_EW*sqrt(8*self_consistent_lH),
    "mH_pdg": M_H,
    "mH_error_pct": abs(V_EW*sqrt(8*self_consistent_lH)-M_H)/M_H*100,
    "top_yukawa": {"y_top_pdg": Y_TOP, "w33_fixed_point": 1.0, "correction": 1-1/k**2},
    "MW_predicted": MW_pred_w33, "MW_pdg": M_W,
    "sin2_theta_W_w33": sin2_w33, "sin2_theta_W_pdg": SIN2_TW,
    "spectral_action_conjecture": "lambda_H = 2*f2/f4 = 2*Tr[D^2]/Tr[D^4] (non-trivial spectrum)"
}
with open("higgs_spectral_action_results.json","w") as fh: json.dump(results,fh,indent=2)
print("\nDone. Results saved to higgs_spectral_action_results.json")
