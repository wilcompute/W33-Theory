"""Pass 12726 (Claude track), items 1-3 (item 4: explore_pass12726_layers.py; item 5: build_toe_status.py + the summary page).
 (1) Rescuing A by pre-inflation misalignment: Omega_a h^2 = 0.12 (f_a / 9e11 GeV)^1.165 theta_i^2 F(theta_i), F = [ln(e / (1 - theta^2/pi^2))]^(7/6)
     (anharmonic correction).  theta_i needed for f_a = mu_0 across the 1-sigma band (Pass 12725), and the closeness to pi (tuning 1 - theta/pi).
 (2) B''s second dark-matter component vs mesogenesis: psi -> phi_B + xi with stable phi_B, xi and n = n_B each, so the mesogenesis dark matter per
     baryon is m_phi + m_xi < m_psi < m_B - m_p = 4.34 GeV -> at most 4.34 / 5.03 = 86% of the observed DM; the coupled >= 20% (Pass 12725) must
     be outside the mesogenesis sector.
 (3) Brane kinetic terms on the Pati-Salam brane for the SO(10) orbifold: a_4, a_L, a_R shift alpha_i^-1 by delta_3 = a_4, delta_2 = a_L,
     delta_1 = 0.6 a_R + 0.4 a_4; Delta(alpha_3^-1 pred) = 1.2857 a_4 + 0.4286 a_R - 1.7143 a_L; needed to cancel -1.46 (M_s R = 10, Pass 12725);
     natural size alpha_G^-1 / (pi M_s R) (brane-to-bulk volume ratio).
usage: py -3 analysis/explore_pass12726_round.py"""
import json, math, os
from scipy.optimize import brentq

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
res = {}
F = lambda th: math.log(math.e / (1 - (th / math.pi) ** 2)) ** (7 / 6)
om = lambda fa, th: 0.12 * (fa / 9e11) ** 1.165 * th ** 2 * F(th)
mis = []
for fa in (3.7e9, 2.48e10, 1.7e11):
    try:
        th = brentq(lambda t: om(fa, t) - 0.12, 0.01, math.pi * (1 - 1e-15))
        mis.append(dict(f_a=fa, theta_i=th, one_minus_theta_over_pi=1 - th / math.pi))
        print(f"(1) f_a = {fa:.1e}: all-DM misalignment needs theta_i = {th:.4f} ({th / math.pi:.5f} pi; tuning 1 - theta/pi = {1 - th / math.pi:.1e})")
    except ValueError:
        mis.append(dict(f_a=fa, theta_i=None)); print(f"(1) f_a = {fa:.1e}: no solution below pi")
res["misalignment"] = dict(rows=mis, note="pre-inflation PQ breaking (H_I / 2pi < f_a, T_RH < f_a) and low-scale inflation (isocurvature, enhanced near pi)")

mm = 4.34 / (5.36 * 0.938)
res["mesogenesis_share"] = dict(max_share=mm, min_other=1 - mm)
print(f"(2) mesogenesis dark matter (phi_B + xi, one pair per baryon) <= {mm:.0%} of the DM; >= {1 - mm:.0%} must lie outside it - the coupled >= 20% fits there")

need = 1.46; aG = 23.2
nat = {MsR: aG / (math.pi * MsR) for MsR in (10, 15)}
a4 = need / 1.2857; aL = -need / 1.7143; aR = need / 0.4286
res["brane_terms"] = dict(needed_shift=need, a4_only=a4, aL_only=aL, aR_only=aR, natural=nat)
print(f"(3) cancel -1.46 with a single brane term: a_4 = {a4:.2f}, or a_L = {aL:.2f}, or a_R = {aR:.2f} (units of alpha^-1); natural size "
      f"alpha_G^-1/(pi M_s R) = {nat[10]:.2f} (M_s R = 10): needs an O({a4 / nat[10]:.1f}) coefficient on SU(4) (or O({abs(aL) / nat[10]:.1f}) on SU(2)_L)")
json.dump(res, open(os.path.join(ROOT, "data", "explore_pass12726_round.json"), "w"), indent=1)
