"""Pass 12692: five checks following Passes 12690-12691.
 (1) Can electroweak precision fits tell Cs-alpha from Rb-alpha?  Compare their relative difference with the hadronic Delta alpha(M_Z)
     uncertainty, and the induced M_W shift.
 (2) KM3-230213A: flux bookkeeping.  Expected KM3NeT events for the joint-fit flux (7.5e-10, IceCube+Auger+KM3NeT) relative to the
     KM3NeT-only estimate (5.8e-8 per flavour), Poisson chance of >= 1 event, and comparison with cosmogenic expectations (literature ranges).
 (3) Completion A with a flavour-from-PQ (axiflavon-type) sector: BR(K+ -> pi+ a) = m_K^3 |C_sd|^2 (1 - m_pi^2/m_K^2)^3/(16 pi f_a^2 Gamma_K)
     vs the NA62-based bound f_a/|C_sd| > 1.1e12 GeV (Toni 2025, 2503.05865).
 (4) Completion B's T-B-T' triplet: LO QCD pair production (Combridge partonic cross sections) folded with CT18NNLO (parton package),
     validated on t tbar at 13 TeV (NNLO+NNLL 832 pb defines a K-factor); and the decay regimes: internal off-shell W* transitions
     (Delta M ~ 44 GeV) vs mixing-induced decays to SM quarks.
 (5) Neutron lifetime vs BBN helium: Y_p(tau_n) with d ln Y_p / d ln tau_n = 0.73 around Y_p = 0.2470 at tau_n = 879.4 s (Planck eta),
     against Aver+2021, Hsyu+2020, Kurichin+2021, EMPRESS 2022.
usage: py -3 analysis/toe_pass12692_five_checks.py"""
import json, math, os
import numpy as np
from scipy.stats import norm, poisson
from scipy.integrate import quad

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
res = {}
# ---------------- (1)
d_alpha_rel = (137.035999206 - 137.035999046) / 137.035999
dahad_unc = 1.0e-4
sw2 = 0.2312; dMW = 80.37 * sw2 / (2 * (1 - 2 * sw2)) * d_alpha_rel
res["alpha_vs_EW"] = dict(Cs_Rb_relative_difference=d_alpha_rel, hadronic_Delta_alpha_uncertainty=dahad_unc, ratio=dahad_unc / d_alpha_rel, MW_shift_GeV=dMW)
print(f"(1) Cs-Rb relative alpha difference {d_alpha_rel:.2e} vs Delta alpha_had uncertainty ~{dahad_unc:.0e} (ratio {dahad_unc / d_alpha_rel:.0e}); M_W shift {dMW:.1e} GeV: EW fits cannot discriminate")
# ---------------- (2)
km3_only, joint = 5.8e-8, 7.5e-10
mu_ev = joint / km3_only
p1 = 1 - math.exp(-mu_ev)
res["km3net_flux"] = dict(expected_events_at_joint_flux=mu_ev, p_at_least_one=p1, sigma=norm.isf(p1),
                          cosmogenic_E2Phi_200PeV_ranges="proton-rich UHECR ~1e-9-1e-8; Auger-like mixed composition ~1e-11-1e-10 (GeV cm^-2 s^-1 sr^-1, literature ranges)",
                          reading="the joint-fit flux sits between mixed-composition and proton-rich cosmogenic expectations; a real KM3NeT event at that flux is a ~2.2 sigma upward fluctuation")
print(f"(2) at the joint-fit flux KM3NeT expects {mu_ev:.4f} events; P(>=1) = {p1:.4f} ({norm.isf(p1):.2f} sigma)")
# ---------------- (3)
mK, mpi, GK = 0.493677, 0.13957, 6.582e-25 / 1.2380e-8
def br_kpia(fa, C): return mK ** 3 * C ** 2 * (1 - mpi ** 2 / mK ** 2) ** 3 / (16 * math.pi * fa ** 2 * GK)
ax = {}
for C in (1.0, 0.22, 0.05):
    ax[f"C_sd={C}"] = dict(BR_at_fa_1e11=br_kpia(1e11, C), fa_min_from_1p1e12=1.1e12 * C, ma_max_ueV=57.2 * 1e11 / (1.1e12 * C))
    print(f"(3) |C_sd| = {C}: BR(K+->pi+ a) at f_a = 1e11 = {br_kpia(1e11, C):.1e}; NA62-based f_a > {1.1e12 * C:.1e} GeV -> m_a < {57.2 * 1e11 / (1.1e12 * C):.0f} ueV")
ax["C_sd_max_at_fa_1e11"] = 1e11 / 1.1e12
ax["reading"] = "the lattice window f_a = 0.88-1.27e11 needs |C_sd| < 0.08-0.12: a Cabibbo-size (0.22) flavour-violating axion coupling is excluded"
res["axiflavon"] = ax
print(f"(3) lattice-window completion A needs |C_sd| < {1e11 / 1.1e12:.3f} (Cabibbo-size 0.22 excluded)")
# ---------------- (4)
from parton import mkPDF
pdf = mkPDF("CT18NNLO", 0, pdfdir=os.path.join(os.environ.get("TEMP", "."), "pdfsets"))
def alphas(mu):
    a = 0.118; MZ = 91.1876
    b0, b1 = (33 - 2 * 5) / (12 * math.pi), (153 - 19 * 5) / (24 * math.pi ** 2)
    L = math.log(mu ** 2 / MZ ** 2)
    a1 = a / (1 + a * b0 * L)
    return a1 * (1 - b1 / b0 * a1 * math.log(1 + a * b0 * L))
def sig_hat(sh, m, a):
    rho = 4 * m * m / sh
    if rho >= 1: return 0.0, 0.0
    b = math.sqrt(1 - rho)
    qq = 8 * math.pi * a ** 2 / (27 * sh) * b * (1 + rho / 2)
    gg = math.pi * a ** 2 / (3 * sh) * ((1 + rho + rho ** 2 / 16) * math.log((1 + b) / (1 - b)) - b * (7 / 4 + 31 * rho / 16))
    return qq, gg
GEV2_PB = 0.3894e9
def xf(pid, x, mu):
    x = np.asarray(x, dtype=float); o = np.argsort(x); out = np.empty_like(x)
    out[o] = np.asarray(pdf.xfxQ(pid, x[o], mu), dtype=float).reshape(x.shape)
    return out
def sigma_pair(m, rs, n_tau=160, n_x=160):
    """sigma = int dtau/tau * tau * [L_qq(tau) sig_qq + L_gg(tau) sig_gg], L(tau) = int_tau^1 dx/x f(x) f(tau/x); Gauss-Legendre in logs."""
    s = rs * rs; mu = m; a = alphas(mu); tau0 = 4 * m * m / s
    gt, wt = np.polynomial.legendre.leggauss(n_tau); gx, wx = np.polynomial.legendre.leggauss(n_x)
    lt0 = math.log(tau0); total = 0.0
    for t_node, t_w in zip(gt, wt):
        lt = lt0 / 2 * (1 - t_node); tau = math.exp(lt); jt = -lt0 / 2
        lx = lt / 2 * (1 - gx); x = np.exp(lx); jx = -lt / 2; x2 = tau / x
        g1, g2 = xf(21, x, mu), xf(21, x2, mu)
        Lgg = float(np.sum(wx * g1 * g2)) * jx / tau
        qq = np.zeros_like(x)
        for q in (1, 2, 3, 4, 5):
            qq += xf(q, x, mu) * xf(-q, x2, mu) + xf(-q, x, mu) * xf(q, x2, mu)
        Lqq = float(np.sum(wx * qq)) * jx / tau
        sq, sg = sig_hat(tau * s, m, a)
        total += t_w * jt * tau * (Lqq * sq + Lgg * sg)
    return total * GEV2_PB
stt = sigma_pair(172.5, 13000.0)
K = 832.0 / stt
print(f"(4) validation: LO sigma(t tbar, 13 TeV, CT18NNLO, mu = m_t) = {stt:.0f} pb -> K = 832/LO = {K:.2f}")
vlq = []
for rs in (13600.0, 14000.0, 100000.0):
    for m in (1600.0, 1650.0, 1700.0, 2000.0):
        lo = sigma_pair(m, rs) * 1000  # fb
        vlq.append(dict(sqrt_s=rs, M=m, sigma_LO_fb=lo, sigma_Kscaled_fb=lo * min(K, 1.6)))
        print(f"    sqrt(s) = {rs / 1000:.1f} TeV, M = {m:.0f}: LO {lo:.3g} fb, x K(capped 1.6) {lo * min(K, 1.6):.3g} fb")
hl = next(v for v in vlq if v["sqrt_s"] == 14000.0 and v["M"] == 1650.0)
events_hl = 3 * hl["sigma_Kscaled_fb"] * 3000
# decay regimes
GF = 1.1664e-5; dM = 44.4; v = 246.22
gam_int = 0.5 * 9 * GF ** 2 * dM ** 5 / (192 * math.pi ** 3)          # overlap 1/2, ~9 open channels
def gam_mix(M, th): return M ** 3 * th ** 2 / (16 * math.pi * v ** 2)   # T -> W b + Z t + h t, Goldstone-equivalence order of magnitude
th_cross = math.sqrt(gam_int * 16 * math.pi * v ** 2 / 1650.0 ** 3)
res["vlq_production_decay"] = dict(K_from_ttbar=K, sigma_ttbar_LO_pb=stt, rows=vlq, HL_LHC_events_3ab_triplet=events_hl,
                                   Gamma_internal_GeV=gam_int, theta_crossover=th_cross,
                                   reading="mixing angle below theta_crossover: cascades B->T W*, T'->B W* (soft) dominate; above: direct T -> Wb/Zt/ht")
print(f"(4) HL-LHC (3/ab, 14 TeV) triplet pairs at 1.65 TeV ~ {events_hl:.0f}; internal width {gam_int:.1e} GeV; cascades dominate for SM mixing < {th_cross:.1e}")
# ---------------- (5)
def Yp(tau): return 0.2470 * (tau / 879.4) ** 0.73
obs = {"Aver+2021": (0.2453, 0.0034), "Hsyu+2020": (0.2436, 0.0040), "Kurichin+2021": (0.2462, 0.0022), "EMPRESS 2022": (0.2370, 0.0034)}
bbn = {}
for lab, tau in (("bottle 877.8", 877.8), ("beam 888.1", 888.1)):
    y = Yp(tau); bbn[lab] = dict(Yp=y, pulls={k: (o - y) / s for k, (o, s) in obs.items()})
    print(f"(5) tau_n {lab}: Y_p = {y:.4f}; pulls " + ", ".join(f"{k} {(o - y) / s:+.2f}" for k, (o, s) in obs.items()))
w = np.array([1 / s ** 2 for _, s in obs.values()]); yv = np.array([o for o, _ in obs.values()])
ymean = float((w * yv).sum() / w.sum()); ysig = float(1 / math.sqrt(w.sum()))
tau_inf = 879.4 * (ymean / 0.2470) ** (1 / 0.73); tau_sig = tau_inf / 0.73 * ysig / ymean
bbn["combined_Yp"] = dict(mean=ymean, sigma=ysig, tau_inferred=tau_inf, tau_sigma=tau_sig)
print(f"(5) combined Y_p = {ymean:.4f} +- {ysig:.4f} -> tau_n = {tau_inf:.0f} +- {tau_sig:.0f} s (BBN alone cannot split 877.8 from 888.1)")
res["neutron_bbn"] = bbn
json.dump(res, open(os.path.join(ROOT, "data", "toe_pass12692_five_checks.json"), "w"), indent=1)
# ---------------- (5b) helium without EMPRESS, and the N_eff reading (dY_p/dN_eff ~ 0.013)
sub = {k: v for k, v in obs.items() if k != "EMPRESS 2022"}
w2 = np.array([1 / s ** 2 for _, s in sub.values()]); y2 = np.array([o for o, _ in sub.values()])
ym2, ys2 = float((w2 * y2).sum() / w2.sum()), float(1 / math.sqrt(w2.sum()))
dY_neff = 0.013 * (2.86 - 3.044)
neff_from_he = {}
for lab, (ym, ys) in (("all four", (ymean, ysig)), ("without EMPRESS", (ym2, ys2))):
    neff = 3.044 + (ym - Yp(877.8)) / 0.013
    neff_from_he[lab] = dict(Yp=ym, sigma=ys, Neff_at_bottle_tau=neff, Neff_sigma=ys / 0.013)
    print(f"(5b) Y_p ({lab}) = {ym:.4f} +- {ys:.4f}: with bottle tau_n, N_eff = {neff:.2f} +- {ys / 0.013:.2f} (ACT DR6: 2.86 +- 0.13)")
print(f"(5b) ACT's N_eff = 2.86 shifts Y_p by {dY_neff:+.4f} -> {Yp(877.8) + dY_neff:.4f}")
res["neutron_bbn"]["helium_Neff"] = dict(rows=neff_from_he, ACT_Yp_shift=dY_neff, Yp_bottle_with_ACT_Neff=Yp(877.8) + dY_neff)
json.dump(res, open(os.path.join(ROOT, "data", "toe_pass12692_five_checks.json"), "w"), indent=1)
