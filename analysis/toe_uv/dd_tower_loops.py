"""Where loops and drag meet: the regulated KK tower that toe_20261103_dark_radiative_stability.py sets aside, against the mass dm_drag_mod.py requires.
Ownership: the one-particle cap Delta m^2 = g c'^2 m^4/(8 pi^2 M^2) is that producer's (aae4f41f5), reproduced here as a control; Casimir energy on a circle is textbook.
1 Tower: V = -(1/2) int ds/s (4 pi s)^-2 [sum_n exp(-s (2 pi n/l)^2) - l/sqrt(4 pi s)], the subtraction being the local bulk term linear in l.  Result per real massless dof: V = -3 zeta(5)/(4 pi^2 l^4) = -3 zeta(5) m_KK^4/(64 pi^6), m_KK = 2 pi/l.  Direct sum against closed form.  No m_n^4 survives, whatever level the dark matter sits on.
2 Natural modulus mass: V ~ m_KK^4 has curvature 16 b^2 V along grad ln m.  If |V| is at most rho_DE, mu <= 4 b sqrt(3 Omega_DE) H0: Hubble mass, the mass the drag excludes.  Shortfall against mu >= 1e5 to 1e6 H0.
3 Non-tower particle: the loop matrix g m^4/(8 pi^2) d_i ln m d_j ln m is rank one along grad ln m, so its curvature on the light path is c'^2 but on chi is b^2.  Cap against the mass that direction actually has: m <= (8 pi^2 mu^2/(g b^2))^(1/4).
Assumes m0 = mu_MSbar as that producer does: a naturalness statement, not an exclusion.  Bulk cosmological constant and brane tension are local counterterms which this does not address.
usage: py -3 dd_tower_loops.py"""
import json
import math
import mpmath as mp

mp.mp.dps = 30
MPL = 2.435e27
HBAR = 6.582119569e-16
MPC = 3.085677581491367e22
HC_M_EV = 1.973269804e-7
out = {}


def integrand(s, l=mp.mpf(1)):
    terms = 1 + 2 * mp.nsum(lambda n: mp.exp(-s * (2 * mp.pi * n / l) ** 2), [1, mp.inf])
    return -0.5 / s * (4 * mp.pi * s) ** -2 * (terms - l / mp.sqrt(4 * mp.pi * s))


def casimir(l=1):
    l = mp.mpf(l)
    return mp.quad(lambda s: integrand(s, l), [l * l / 200, l * l / 20, l * l / 2, l * l * 5, l * l * 50, mp.inf])


exact = lambda l: -3 * mp.zeta(5) / (4 * mp.pi ** 2 * mp.mpf(l) ** 4)
out["casimir"] = {str(l): dict(numeric=float(casimir(l)), exact=float(exact(l))) for l in (1, 2)}
print(out["casimir"], flush=True)
# control: the scaling l^-4 must follow from the direct sum alone
out["casimir_scaling_ratio_l1_over_l2"] = float(casimir(1) / casimir(2))
# control of the subtraction: without removing the local bulk term the result is not finite as the lower limit falls
unsub = lambda s0: float(mp.quad(lambda s: -0.5 / s * (4 * mp.pi * s) ** -2 * (1 + 2 * mp.nsum(lambda n: mp.exp(-s * (2 * mp.pi * n) ** 2), [1, mp.inf])), [s0, s0 * 10, 5, mp.inf]))
out["unsubtracted_grows_as_cutoff_falls"] = {str(s0): unsub(s0) for s0 in (0.02, 0.01, 0.005)}
print(out["unsubtracted_grows_as_cutoff_falls"], flush=True)

coef = float(3 * mp.zeta(5) / (64 * mp.pi ** 6))
out["V_over_mKK4_per_dof"] = coef
fits = {}
d = json.load(open("fading_ds_dovekie.json"))
for lab in ("free_c_neg", "free_c_pos"):
    p = d[lab]
    H0 = 100 * p["h"] * 1000 / MPC * HBAR
    fits[lab] = dict(cp=p["cp"], H0=H0, rho=3 * H0 ** 2 * MPL ** 2 * p["info"]["Ophi0"], OmDE=p["info"]["Ophi0"])
    fits[lab]["cap_one_particle"] = (H0 ** 2 * 8 * math.pi ** 2 * MPL ** 2 / (4 * p["cp"] ** 2)) ** 0.25
out["control_parallel_cap_eV"] = {k: v["cap_one_particle"] for k, v in fits.items()}
par = {(r["dataset"], r["branch"]): r["MS_no_curvature_cancellation_DM_mass_cap_eV"] for r in json.load(open("../../data/toe_20261103_dark_radiative_stability.json"))["rows"]}
out["parallel_track_cap_eV"] = {k: par[("dovekie", k)] for k in fits}
print(out["control_parallel_cap_eV"], out["parallel_track_cap_eV"], flush=True)
pl = json.load(open("class_fit_dovekie.json"))["free_neg"]
H0_pl = 100 * pl["p"]["h"] * 1000 / MPC * HBAR
out["cap_at_full_planck_fit_eV"] = (H0_pl ** 2 * 8 * math.pi ** 2 * MPL ** 2 / (4 * pl["p"]["cp"] ** 2)) ** 0.25

f = fits["free_c_neg"]
H0, rho, Om = f["H0"], f["rho"], f["OmDE"]
# m_KK from |V_C| = rho_DE for net dof N, the dark dimension relation at unit coefficient
out["mKK_if_casimir_is_DE"] = {str(N): dict(mKK_eV=(rho / (N * coef)) ** 0.25, R_micron=HC_M_EV / (rho / (N * coef)) ** 0.25 * 1e6) for N in (1, 5, 20)}
rows = {}
for name, b2 in (("all moduli free", 1.5), ("fixed volume n=1", 0.5), ("fixed volume n=6", 6 / 7)):
    b = math.sqrt(b2)
    mu_max = 4 * b * math.sqrt(3 * Om)
    rows[name] = dict(b=b, mu_max_over_H0=mu_max, shortfall_mass_to_1e5=1e5 / mu_max, shortfall_mass_to_1e6=1e6 / mu_max, shortfall_curvature_to_1e5=(1e5 / mu_max) ** 2)
out["tower_natural_mass"] = rows
print(rows, flush=True)
caps = {}
for g, lab in ((4, "Dirac"), (1, "real scalar")):
    for b in (0.7071, 1.2247):
        for lm in (0, 5, 6, 7, 8):
            mu = 10.0 ** lm
            m = (8 * math.pi ** 2 * (mu * H0) ** 2 * MPL ** 2 / (g * b * b)) ** 0.25
            caps[f"{lab} b={b} mu=1e{lm}H0"] = dict(m_cap_eV=m, V_CW_over_rho_DE=g * m ** 4 * 1.5 / (64 * math.pi ** 2) / rho)
out["particle_caps"] = caps
print({k: (round(v["m_cap_eV"], 5), float("%.3g" % v["V_CW_over_rho_DE"])) for k, v in caps.items() if k.startswith("Dirac")}, flush=True)
json.dump(out, open("dd_tower_loops.json", "w"), indent=1, default=float)
