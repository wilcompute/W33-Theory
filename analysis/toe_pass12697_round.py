"""Pass 12697: follow-ups to Pass 12696.
 (1) Completion A's PQ-charged doublet: with lambda_12 sigma^2 H1 H2 (or sigma H1 H2) couplings the second doublet mass is ~ sqrt(lambda) f_a,
     so it decouples; flavour/B constraints vanish and the anomaly coefficients (E/N, N_DW) are unchanged; the cost is the usual DFSZ
     hierarchy tuning (125 GeV / m_H2)^2.
 (2) Completion B's SM mixing: singlet-like top mixing theta gives Delta T ~ T_SM theta^2 (2 ln r - 2), r = M^2/m_t^2 (leading-log form);
     doublet-like B mixing shifts g_L^b by ~ theta_b^2/2 (Zbb: |delta g_L^b| < ~2e-3).  Does EW precision fix the prompt vs cascade regime?
 (3) Candidates for the keV-window particle: (a) photophilic ALP with m < 4.4 MeV (photons below the 2.22 MeV D threshold),
     tau = 64 pi/(g^2 m^3); (b) a modulus with Gamma = m^3/(4 pi M_Pl^2); (c) a gravitino tau ~ 4e8 s (100 GeV/m)^3.
 (4) Superallowed corrections: V_ud(0+) = 0.97361(30) (Seng et al. 2024) vs neutron 0.97456(44); needed Ft (equivalently delta_NS)
     shift vs the new ab initio delta_NS(10C) = -0.422(14) % (Gennari et al. PRL 2025).
 (5) Combined ranking with BIC-based Bayes factors over the data set (M_t, n_s, N_eff, D/H, Y_p, K->pi a, collider), n = 7.
usage: py -3 analysis/toe_pass12697_round.py"""
import json, math, os

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
res = {}
# (1)
fa = 1e11
dfsz = []
for lam in (1e-12, 1e-8, 1e-4):
    mH2 = math.sqrt(lam) * fa
    dfsz.append(dict(lambda_12=lam, m_H2_GeV=mH2, tuning=(125.0 / mH2) ** 2))
    print(f"(1) lambda_12 = {lam:.0e}: m_H2 ~ {mH2:.1e} GeV, Higgs tuning ~ {(125 / mH2) ** 2:.0e}")
res["pq_doublet"] = dict(rows=dfsz, note="H2 decouples for any lambda >~ 1e-14; flavour constraints on a 2HDM vanish; E/N and N_DW fixed by charges; "
                                         "cost = DFSZ-type hierarchy tuning (generic in axion models with charged doublets)")
# (2)
mt, TSM = 172.57, 1.2025
rows = []
for M in (1740.0, 2100.0):
    r = (M / mt) ** 2
    for th in (1e-4, 1e-2, 0.1, 0.2):
        dT = TSM * th ** 2 * (2 * math.log(r) - 2)
        rows.append(dict(M=M, theta=th, Delta_T=dT, T_ok=dT < 0.27))
th_max = math.sqrt(0.27 / (TSM * (2 * math.log((1740 / mt) ** 2) - 2)))
thb_max = math.sqrt(2 * 2e-3)
res["b_mixing"] = dict(rows=rows, theta_t_max=th_max, theta_b_max=thb_max, cascade_boundary=1.1e-4,
                       reading="EW precision allows theta up to ~0.17 (top) and ~0.06 (bottom); the 1e-4 prompt/cascade boundary lies deep inside: EW data do not fix the regime")
print(f"(2) top-partner mixing allowed up to theta ~ {th_max:.2f} (T), bottom ~ {thb_max:.2f} (Zbb); cascade boundary 1.1e-4 is unconstrained by EW data")
# (3)
GEV_S = 6.582e-25
cand = {}
for m in (1e-3, 2e-3, 4e-3):
    tau = 1.3e4 / GEV_S
    g = math.sqrt(64 * math.pi / (tau * m ** 3))
    cand[f"ALP m={m * 1e3:.0f} MeV"] = dict(g_agg_GeV_inv=g, lifetime_s=1.3e4)
    print(f"(3a) photophilic ALP, m = {m * 1e3:.0f} MeV, tau = 1.3e4 s: g_agg = {g:.1e} GeV^-1")
MPL = 2.435e18
tau = 1.3e4 / GEV_S
m_mod = (4 * math.pi * MPL ** 2 / tau) ** (1 / 3)
m_grav = 100.0 * (4e8 / 1.3e4) ** (1 / 3)
cand["modulus"] = dict(mass_GeV=m_mod, note="couples to gluons generically -> hadronic BBN bounds")
cand["gravitino"] = dict(mass_GeV=m_grav, note="hadronic branching ~1e-3 -> excluded at zeta ~ 1e-6 GeV")
cand["reading"] = ("MeV ALP with g ~ 1e-9 GeV^-1 has the right lifetime and sub-threshold photons, but sits in the SN1987A / BBN 'cosmological triangle' "
                   "region; modulus (~1.7 TeV) and gravitino (~3 TeV) decays carry hadronic branchings that BBN excludes at zeta ~ 1e-6 GeV")
print(f"(3b) modulus with tau = 1.3e4 s: m ~ {m_mod:.1e} GeV; (3c) gravitino: m ~ {m_grav:.1e} GeV (both hadronic -> excluded)")
res["kev_candidates"] = cand
# (4)
v0, s0, vn, sn = 0.97361, 0.00030, 0.97456, 0.00044
rel = (v0 / vn) ** 2 - 1
res["superallowed"] = dict(V_ud_0plus=v0, V_ud_neutron=vn, pull=(vn - v0) / math.hypot(s0, sn), Ft_rel_shift=rel, Ft_shift_s=3072.24 * rel,
                           delta_NS_10C_percent=-0.422, delta_NS_unc_percent=0.014, shift_over_dNS_unc=abs(rel * 100) / 0.014)
print(f"(4) V_ud(0+) {v0} vs neutron {vn}: {(vn - v0) / math.hypot(s0, sn):.1f} sigma; needed Ft shift {rel * 100:+.3f} % = {3072.24 * rel:.1f} s, "
      f"= {abs(rel * 100) / 0.014:.0f}x the new ab initio delta_NS(10C) uncertainty")
# (5)
n = 7
models = {"SM + LCDM": (2.00, 0), "lambda(sqrt(v M_Pl)) = 0": (2.00, 0), "Completion A (b-only PQ, extra scalar, xi>=10)": (2.04, 2),
          "Completion B (dark dim + VL, GeV reheating)": (2.00, 1), "lambda(M_Pl) = 0": (7.74, 0), "original SMASH": (9.01, 0)}
out = {}
base = models["SM + LCDM"][0]
for k, (c, kpar) in models.items():
    bic = c + kpar * math.log(n); dbic = bic - base
    out[k] = dict(chi2=c, k=kpar, dBIC=dbic, bayes_factor_vs_SM=math.exp(-dbic / 2))
    print(f"(5) {k:50s}: dBIC = {dbic:+.2f}, B(vs SM) ~ {math.exp(-dbic / 2):.2f}")
res["ranking_bic"] = out
json.dump(res, open(os.path.join(ROOT, "data", "toe_pass12697_round.json"), "w"), indent=1)
