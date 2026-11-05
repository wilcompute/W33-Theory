"""Items 2-4 of Pass 12622.
Item 3, the heavy-axion orbifold variant.  Brane SU(3) small instantons add V = K e^(-S) (1/R)^4 cos(N a/f - theta_brane), S = 8 pi^2/g_b^2 = 2 pi alpha_b^-1, with alpha_b the brane-localised coupling (apparent unification wants brane terms small, alpha_b^-1 well below alpha_U^-1 ~ 38).  K: the 't Hooft vertex of six quark flavours closed by Yukawa loops, K ~ prod_q y_q/(4 pi), with high-scale Yukawas (rough values, from memory): an estimate to a few orders of magnitude.
   If theta_brane = theta_QCD (aligned, e.g. by CP), strong CP is still solved and the axion is heavy: m_a^2 f_a^2 = chi + K e^-S R^-4.  If not aligned, the PQ solution needs K e^-S R^-4 < 1e-10 chi.
   Report m_a versus alpha_b^-1 for f_a = 1e11 GeV and 1/R = 5e15 GeV, and the alpha_b^-1 above which the brane term is harmless.
Item 4, why three copies.  If the three vectorlike (3,3bar,1) came with full E6 27 + 27bar, they would add a universal shift to all three b_i and change nothing: control by two-loop, expected no solution (the threshold drops out at one loop).  So the trinification candidate needs SU(3)^3 multiplets that are not full E6 27s, and the number three is not explained by E6.
Item 2, joint target for Model A with Higgs-portal inflation: n_s from my fits under fading and CPL; SMASH-type inflation predictions n_s ~ 0.965-0.968 and r ~ 0.004 (from memory of Ballesteros et al 2016, not re-read); w from the CPL fit.
usage: py -3 items_234.py"""
import json
import math
import numpy as np

out = {}
# item 3
chi = (75.6e-3) ** 4
invR = 5e15
fa = 1e11
yq = dict(u=3e-6, d=6e-6, s=1.2e-4, c=1.5e-3, b=5e-3, t=0.45)
K = float(np.prod([y / (4 * math.pi) for y in yq.values()]))
rows = []
for ab in (1, 2, 3, 5, 8, 10, 15, 20, 30):
    S = 2 * math.pi * ab
    D = K * math.exp(-S) * invR ** 4
    ma = math.sqrt(chi + D) / fa
    rows.append(dict(alpha_b_inv=ab, S=S, brane_over_chi=D / chi, m_a_eV=ma * 1e9, harmless_if_misaligned=D < 1e-10 * chi))
    print("alpha_b^-1 %2d  S %5.1f  brane/chi %.2g  m_a %.3g eV  harmless if misaligned: %s" % (ab, S, D / chi, ma * 1e9, D < 1e-10 * chi), flush=True)
ab_dom = (math.log(K * invR ** 4 / chi)) / (2 * math.pi)
ab_safe = (math.log(K * invR ** 4 / (1e-10 * chi))) / (2 * math.pi)
out["heavy_axion"] = dict(K=K, rows=rows, alpha_b_inv_brane_dominates_below=ab_dom, alpha_b_inv_safe_above=ab_safe, QCD_m_a_eV=math.sqrt(chi) / fa * 1e9)
print("K %.2g; brane term dominates the QCD mass for alpha_b^-1 < %.1f; harmless if misaligned for alpha_b^-1 > %.1f" % (K, ab_dom, ab_safe), flush=True)
# item 4: E6 27 content under SM: Q(3,2,1/6) u^c d^c L e^c nu^c + D(3,1,-1/3) Dbar + Hu Hd + singlet: as vectorlike pairs
src = open("pq_twoloop.py", encoding="utf-8").read().split("out = {}")[0]
g = {}
exec(src, g)
solve2 = g["solve2"]
full27 = [(3, 2, 1 / 6), (3, 1, 2 / 3), (3, 1, -1 / 3), (1, 2, 1 / 2), (1, 1, 1), (3, 1, -1 / 3), (1, 2, 1 / 2)]  # Dirac pairs of 27 + 27bar fragments (singlets dropped)
s = solve2(full27 * 3, x0=[math.log(1e10), math.log(2e16)])
out["control_three_full_27"] = s
print("three full 27 + 27bar:", s, "(expected: no solution, since a complete E6 multiplet shifts all b_i equally at one loop)", flush=True)
# item 2
ns = json.load(open("ns_by_model.json"))
out["joint_target"] = dict(n_s_fading=ns["class_fit_dovekie.json"]["free_neg"], n_s_CPL=ns["class_fit_dovekie.json"]["CPL"], n_s_LCDM=ns["class_fit_dovekie.json"]["LCDM"], n_s_SMASH=[0.965, 0.968], r_SMASH=0.004, note="SMASH values from memory, not re-read")
print("joint:", out["joint_target"], flush=True)
json.dump(out, open("items_234.json", "w"), indent=1, default=float)
