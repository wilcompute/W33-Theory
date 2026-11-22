"""Pass 12690: follow-ups to the two completions (Passes 12688-12689).
 (1) Completion B collider handle: for equal Dirac masses the two charge-2/3 states are split by exactly y' v/sqrt2 (singular values
     sqrt(M^2 + m^2/4) +- m/2, m = y' v/sqrt2), with the charge -1/3 B in the middle: a compressed T-B-T' triplet whose internal decays
     (Delta M ~ 45 GeV < m_W) are off-shell three-body.  y' = sqrt2 Delta M / v, so a Delta M resolution maps to delta y'.
 (2) Completion B dark matter: the dark-graviton DM mass today (few x 10-10^2 keV) vs m_KK; no further pinning of R from this pass.
 (3) Completion A leptogenesis vs ACT inflation: a PQ-generated Majorana mass M_N = y_N f_a/sqrt2 needs y_N ~ sqrt2 M_N/f_a; its fermion
     contribution to the running of lambda_sigma, b_N = -c sum y_N^4 / (16 pi^2 lambda_sigma), must be over-compensated by the extra scalar
     to give the needed b ~ +0.03.  Report the cancellation (tuning) factor |b_N|/b_needed vs M_N and xi.
 (4) Family-symmetry breaking (cross-track): neither completion contains a field charged under a family group (H27 in the other track),
     so neither supplies the breaking their no-go requires.
usage: py -3 analysis/toe_pass12690_completion_followups.py"""
import json, math, os
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
res = {}
v = 246.22
# (1)
spec = []
for M in (1650.0, 2000.0, 3000.0):
    for yp in (0.494, 0.51, 0.529):
        m = yp * v / math.sqrt(2)
        sv = sorted(np.linalg.svd(np.array([[M, m], [0.0, M]]), compute_uv=False))
        spec.append(dict(M_VL=M, y_prime=yp, mT=sv[0], mB=M, mTp=sv[1], dM_TTp=sv[1] - sv[0], dM_BT=M - sv[0]))
    print(f"(1) M_VL={M:.0f}: y'=0.51 -> T {spec[-2]['mT']:.1f}, B {M:.0f}, T' {spec[-2]['mTp']:.1f}; Delta M(T'-T) = {spec[-2]['dM_TTp']:.2f} GeV = y' v/sqrt2")
assert all(abs(s["dM_TTp"] - s["y_prime"] * v / math.sqrt(2)) < 1e-6 for s in spec)
res["vlq_triplet"] = dict(rows=spec, y_prime_from_splitting="y' = sqrt2 dM/v; dM resolution 5 GeV -> delta y' = 0.029; 2 GeV -> 0.011",
                          internal_decays="B -> T W*, T' -> B W* with dM ~ 44-45 GeV < m_W: soft off-shell products (compressed spectrum)")
# (2)
res["graviton_dm"] = dict(mass_today_keV="~50-few hundred (2311.05318, 2307.11048 benchmarks for R 1-30 um)", m_KK_eV="0.007-0.2",
                          note="DM mass today >> m_KK: the tower has decayed down from ~GeV; X-ray/EBL bound mass today <~ MeV; no extra pinning of R here")
# (3)
f_a = 1e11
lam_s = {1.0: 4.42e-10, 10.0: 3.84e-8, 100.0: 3.8e-6}
bneed = 0.03
tune = []
for MN in (1e8, 1e9, 1e10, 1e11):
    yN = math.sqrt(2) * MN / f_a
    for xi, ls in lam_s.items():
        for c in (0.5, 2.0):
            bN = c * 3 * yN ** 4 / (16 * math.pi ** 2 * ls)       # three degenerate N
            tune.append(dict(M_N=MN, y_N=yN, xi=xi, c=c, b_N=bN, cancellation_factor=bN / bneed))
for t in tune:
    if t["c"] == 2.0: print(f"(3) M_N={t['M_N']:.0e} (y_N={t['y_N']:.3f}) xi={t['xi']:g}: fermion running |b_N| = {t['b_N']:.2e} -> cancellation factor {t['cancellation_factor']:.1e} (c=2)")
res["leptogenesis_vs_inflation"] = dict(rows=tune, b_needed=bneed, davidson_ibarra_GeV=1e9,
    note="M_N >= 1e9 (Davidson-Ibarra) with xi = 1 needs the extra scalar to cancel the N_R running to ~1e-2 or worse; xi >~ 10 removes the tension")
# (4)
res["family_breaking"] = "neither completion contains a family-charged field; H27 (other track, fc0971f0e) breaking needs a separate flavon sector"
json.dump(res, open(os.path.join(ROOT, "data", "toe_pass12690_completion_followups.json"), "w"), indent=1)
