"""Pass 12694: follow-ups to Pass 12693, plus the W mass.
 (1) Completion A flavour: PQ charges only on the third generation.  Flavour-violating axion couplings then come with CKM factors:
     C_sd ~ V_td* V_ts, C_bs ~ V_tb* V_ts; BR(K+ -> pi+ a) and BR(B -> K a) at f_a = 1e11 GeV vs current limits.
 (2) Completion B triplet: soft-lepton tag rates.  Pairs TT, BB, T'T' produced equally; B -> T W*, T' -> B W* -> T W* W*;
     P(W* -> e/mu nu) ~ 0.22 (soft, ~44 GeV parent); fraction of HL-LHC pairs with >= 1 soft lepton.
 (3) Deuterium: PRIMAT 2.439(37)e-5 vs PArthENoPE 2.51(11)e-5 (different d(d,n), d(d,p), d(p,g) rates) against Cooke+2018 2.527(30)e-5.
 (4) KM3-230213A chance blazar coincidence: 4FGL density ~0.17 deg^-2, flaring duty fraction ~0.1 (assumption), within 2.4 deg
     (PKS 0605-085 offset) and 1.5 deg (claimed systematic) of the direction.
 (5) Helium mixture model: each Y_p is 'good' N(mu, s_i) with prob 1 - P_out or 'outlier' N(mu, sqrt(s_i^2 + tau^2)), tau = 0.010;
     posterior for mu (flat prior) and per-survey outlier probabilities; implied N_eff at the bottle tau_n.
 (6) W mass: weighted average of CMS 2024, ATLAS 2024, LHCb 2022, D0, LEP with and without CDF 2022; CDF pull; vs the SM fit
     (values entered from the experiments' publications; SM 80356 +- 6 MeV as a representative EW-fit value).
usage: py -3 analysis/toe_pass12694_round.py"""
import json, math, os
import numpy as np
from scipy.stats import poisson, chi2 as chi2d

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
res = {}
# (1)
Vtd, Vts, Vtb = 8.6e-3, 4.15e-2, 0.999
mK, mpi, GK = 0.493677, 0.13957, 6.582e-25 / 1.2380e-8
mB, GB = 5.279, 6.582e-25 / 1.638e-12
def br(mP, mp, G, fa, C, f0=1.0): return mP ** 3 * C ** 2 * f0 ** 2 * (1 - mp ** 2 / mP ** 2) ** 3 / (16 * math.pi * fa ** 2 * G)
Csd, Cbs = Vtd * Vts, Vtb * Vts
r1 = dict(C_sd=Csd, C_bs=Cbs, BR_K_pi_a=br(mK, mpi, GK, 1e11, Csd), BR_B_K_a=br(mB, mK, GB, 1e11, Cbs, 0.33),
          limits="K+->pi+ a < ~(3-6)e-11 (NA62); B->K + invisible ~1e-5 (Belle II)")
res["third_generation_PQ"] = r1
print(f"(1) 3rd-gen PQ charges: C_sd ~ {Csd:.1e}, BR(K->pi a) = {r1['BR_K_pi_a']:.1e}; C_bs ~ {Cbs:.3f}, BR(B->K a) = {r1['BR_B_K_a']:.1e} (both far below limits)")
# (2)
pl = 0.22
p_BB = 1 - (1 - pl) ** 2; p_TpTp = 1 - (1 - pl) ** 4
frac = (0 + p_BB + p_TpTp) / 3
n_pairs = 13045
res["soft_lepton_tags"] = dict(P_BB=p_BB, P_TpTp=p_TpTp, fraction=frac, HL_LHC_tagged=frac * n_pairs, note="lepton pT ~ 5-25 GeV from W* with ~44 GeV parent")
print(f"(2) fraction of triplet pairs with >= 1 soft lepton: {frac:.2f} -> ~{frac * n_pairs:.0f} tagged pairs at HL-LHC (1.65 TeV)")
# (3)
obs = (2.527, 0.030)
dd = {}
for lab, (v, e) in {"PRIMAT (Pitrou+2018/2021)": (2.439, 0.037), "PArthENoPE (Pisanti+2021)": (2.51, 0.11)}.items():
    dd[lab] = dict(DH=v, pull=(obs[0] - v) / math.hypot(obs[1], e))
    print(f"(3) D/H {lab}: {v} -> pull vs Cooke {dd[lab]['pull']:+.2f} sigma")
res["deuterium_rates"] = dd
# (4)
dens, duty = 7195 / 41253.0, 0.10
coin = {}
for r in (2.4, 1.5, 0.5):
    lam = dens * duty * math.pi * r * r
    coin[str(r)] = dict(expected_flaring=lam, P_at_least_one=1 - math.exp(-lam))
    print(f"(4) radius {r} deg: expected flaring 4FGL blazars {lam:.3f}, P(>=1 by chance) = {1 - math.exp(-lam):.2f}")
res["km3net_coincidence"] = dict(rows=coin, assumptions="4FGL-DR4 ~7195 sources; flaring duty fraction 0.1 (assumed)")
# (5)
Y = np.array([0.2453, 0.2436, 0.2462, 0.2370]); S = np.array([0.0034, 0.0040, 0.0022, 0.0034]); names = ["Aver+2021", "Hsyu+2020", "Kurichin+2021", "EMPRESS 2022"]
mu = np.linspace(0.230, 0.260, 6001); tau = 0.010
mix = {}
for pout in (0.1, 0.2):
    like = np.ones_like(mu);
    comps = []
    for y, s in zip(Y, S):
        g = (1 - pout) * np.exp(-0.5 * ((y - mu) / s) ** 2) / s
        o = pout * np.exp(-0.5 * (y - mu) ** 2 / (s * s + tau * tau)) / math.sqrt(s * s + tau * tau)
        like *= g + o; comps.append((g, o))
    post = like / np.trapezoid(like, mu)
    m = float(np.trapezoid(mu * post, mu)); sd = float(math.sqrt(np.trapezoid((mu - m) ** 2 * post, mu)))
    pout_i = {n: float(np.trapezoid(post * o / (g + o), mu)) for n, (g, o) in zip(names, comps)}
    neff = 3.044 + (m - 0.2467) / 0.013
    mix[f"P_out={pout}"] = dict(Yp=m, sigma=sd, Neff=neff, Neff_sigma=sd / 0.013, outlier_prob=pout_i)
    print(f"(5) mixture P_out={pout}: Y_p = {m:.4f} +- {sd:.4f} -> N_eff = {neff:.2f} +- {sd / 0.013:.2f}; P(outlier): " + ", ".join(f"{n} {p:.2f}" for n, p in pout_i.items()))
res["helium_mixture"] = mix
# (6)
W = {"CMS 2024": (80360.2, 9.9), "ATLAS 2024": (80366.5, 15.9), "LHCb 2022": (80354, 32), "D0 Run II": (80375, 23), "LEP": (80376, 33), "CDF 2022": (80433.5, 9.4)}
SM = (80356.0, 6.0)
def wavg(keys):
    w = np.array([1 / W[k][1] ** 2 for k in keys]); x = np.array([W[k][0] for k in keys])
    m = (w * x).sum() / w.sum(); s = 1 / math.sqrt(w.sum()); c = float((((x - m) * np.sqrt(w)) ** 2).sum())
    return m, s, c, len(keys) - 1
wres = {}
for lab, keys in (("all", list(W)), ("without CDF", [k for k in W if k != "CDF 2022"])):
    m, s, c, dof = wavg(keys)
    wres[lab] = dict(mean=m, sigma=s, chi2=c, dof=dof, p=float(chi2d.sf(c, dof)), pull_vs_SM=(m - SM[0]) / math.hypot(s, SM[1]))
    print(f"(6) W mass {lab}: {m:.1f} +- {s:.1f} MeV, chi2 {c:.1f}/{dof} (p {chi2d.sf(c, dof):.1e}); vs SM {SM[0]}: {(m - SM[0]) / math.hypot(s, SM[1]):+.2f} sigma")
m_o, s_o, _, _ = wavg([k for k in W if k != "CDF 2022"])
wres["CDF_pull_vs_rest"] = (80433.5 - m_o) / math.hypot(9.4, s_o)
print(f"(6) CDF vs the rest: {wres['CDF_pull_vs_rest']:+.1f} sigma")
res["W_mass"] = wres
json.dump(res, open(os.path.join(ROOT, "data", "toe_pass12694_round.json"), "w"), indent=1)
