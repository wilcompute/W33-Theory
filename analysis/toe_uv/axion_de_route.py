"""Outside idea: if the dark matter is the PQ axion (Model A / trinification), through which parameter can the fading coupling b = d ln m_DM / d(phi/M_P) ~ 0.053 act?
m_a = sqrt(chi_QCD)/f_a, chi_QCD ~ Lambda^3 * m_q-type scaling (chi ~ m_pi^2 f_pi^2 ~ m_q Lambda^3), so d ln m_a = (3/2) d ln Lambda + (1/2) d ln m_q - d ln f_a.
Routes (each carrying all of b):
  Lambda_QCD: d ln Lambda/dphi = 2b/3 -> nucleon mass coupling alpha_N = 2b/3;
  quark masses via the Higgs vev: d ln v/dphi = 2b -> electron mass and nucleons couple too (alpha_e = 2b);
  f_a (PQ sector only): d ln f_a/dphi = -b, baryons and leptons untouched at tree level.
Bounds for a field of Hubble-scale mass (long range):
  Cassini |gamma - 1| = 2 alpha_N^2 < 2.3e-5 (Bertotti et al. 2003) -> alpha_N < 3.4e-3;
  atomic clocks |d ln mu/dt| < 5e-17 /yr for mu = m_p/m_e (order of magnitude from memory of Yb+/Cs comparisons; not re-read).
Field velocity today: (phi_dot/M_P)^2 = 3 (1 + w) Omega_DE H0^2 for a kinetic-dominated departure from w = -1; range 1 + w = 0.05-0.3.
usage: py -3 axion_de_route.py"""
import json
import math

b = 0.053
H0 = 0.678 * 100 / 3.0857e19 * 3.156e7  # per year
ODE = 0.69
out = dict(b=b, H0_per_yr=H0, routes={})
for opw in (0.05, 0.15, 0.3):
    phid = math.sqrt(3 * opw * ODE) * H0
    rows = {}
    for name, aN, amu in (("Lambda_QCD", 2 * b / 3, 2 * b / 3), ("higgs_vev", 2 * b, 0.0), ("f_a", 0.0, 0.0)):
        # mu = m_p/m_e: Lambda route moves m_p only; vev route moves m_q (small part of m_p, sigma term ~ 5 percent) and m_e: d ln mu ~ -d ln m_e = -2b dphi
        dmu = amu if name != "higgs_vev" else -2 * b * (1 - 0.05)
        rows[name] = dict(alpha_N=aN, gamma_minus_1=2 * aN ** 2, cassini_ratio=2 * aN ** 2 / 2.3e-5, mu_dot_per_yr=abs(dmu) * phid, clock_ratio=abs(dmu) * phid / 5e-17, axion_mass_drift_per_yr=b * phid)
    out["routes"][f"1+w={opw}"] = rows
    for k, v in rows.items():
        print("1+w %.2f %-10s alpha_N %.3f  gamma-1 %.1e (x%.0f Cassini)  mu_dot %.1e/yr (x%.0e clocks)  m_a drift %.1e/yr" % (opw, k, v["alpha_N"], v["gamma_minus_1"], v["cassini_ratio"], v["mu_dot_per_yr"], v["clock_ratio"], v["axion_mass_drift_per_yr"]))
json.dump(out, open("axion_de_route.json", "w"), indent=1)

# f_a route leaks into the Higgs through the portal lambda_hs |H|^2 |sigma|^2 with <sigma> = f_a / sqrt(2) (up to N_DW):
#   V = mu^2 H^2 + lambda H^4 with mu^2 containing lambda_hs f_a(phi)^2 / 2; v^2 = -mu^2/lambda, m_h^2 = 2 lambda v^2, b = -d ln f_a/dphi  =>  d ln v / dphi = lambda_hs f_a^2 b / m_h^2
#   d ln m_e / dphi = d ln v / dphi; the clock bound on mu then caps lambda_hs.
fa_list = (1e9, 1e11, 7e12)
mh = 125.25
caps = {}
for fa in fa_list:
    phid = math.sqrt(3 * 0.05 * ODE) * H0  # most forgiving 1+w
    alpha_v_max = 5e-17 / phid
    lam_max = alpha_v_max * mh ** 2 / (b * fa ** 2)
    caps[fa] = lam_max
    print("f_a %.0e GeV: clocks need lambda_hs < %.1e (most forgiving 1+w = 0.05)" % (fa, lam_max))
out["higgs_portal_cap"] = {str(k): v for k, v in caps.items()}
out["needed_for_threshold_stabilisation"] = "lambda_hs ~ 0.1 to 0.5 (Pass 12612 sigma-threshold mechanism)"
out["radiative_floor_estimate"] = "two-loop via PQ quarks with SM gauge charges: of order g^4 y^2/(16 pi^2)^2 ~ 1e-7 to 1e-5 (rough)"
json.dump(out, open("axion_de_route.json", "w"), indent=1)
