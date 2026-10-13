"""Pass 11945: PMNS excludes the pure charge-rule charged leptons in every branch; one Higgs Wilson line fits the lepton
masses and forces a near-mu-tau-adapted charged-lepton basis -- the odd-nu2 branch is impossible, the mu-tau paradigm
(odd nu3) emerges.

Inputs: Passes 11942 (z_e = 6 z_d), 11943 (PMNS no-go), 11944 (identities: with a mu-tau-clean neutrino sector the PMNS
column of the odd neutrino equals the odd contents of e, mu, tau).

1. Branch-independent exclusion. Measured |U| columns (e, mu, tau): nu1 (0.82, 0.36, 0.43), nu2 (0.55, 0.60, 0.58),
   nu3 (0.15, 0.74, 0.66). Whatever neutrino is odd, the muon's odd content must be >= 0.36. The charge-rule leptons of
   11942 have muon odd content 0.08 (both fits): excluded in EVERY branch.
2. Minimal escape: an H_d Wilson line h_d. The down sector is unchanged (z_d is fitted), the leptons get
   z_e = 6 z_d - 5 h_d (one complex parameter). Fitting the two charged-lepton mass ratios alone gives many solutions
   (re-found by multistart on both quark fits, keeping |Im z_e| <= 0.5 so that the Gaussian centre stays well inside the
   N = 40 theta truncation; one solution beyond that bound looked like an outlier and was traced to truncation). EVERY solution has the same
   odd-content profile: one charged lepton nearly mu-tau even (odd content <= 0.12), the other two near-maximal
   (0.61-0.79) -- three classes by which lepton is even.
3. Consequences.
   * Branch (a) (odd nu2; needs all three ~0.58) is impossible in this family -- so the near-product Wilson-free
     neutrino relation of Passes 11939/11940 (Sigma = 0.0596 eV) is disfavoured within the framework.
   * In the e-even class the charged leptons give theta13 ~ 0.3-0.5 deg and sin^2 theta23 in [0.37, 0.59] (data 0.561):
     the mu-tau paradigm with odd nu3. A fit to masses + the nu3 column (2 parameters, 4 constraints) has chi^2 = 7.7 at
     both quark fits, with masses (0.0585, 0.00482) and sin^2 theta23 = 0.558; the miss is theta13 (0.5 vs 8.6 deg),
     which must come from the neutrino side, as must theta12.
"""

import json
import sys
from pathlib import Path

import numpy as np
from scipy.optimize import least_squares

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))
import w33_pass11942_hypercharge_wilson_leptons as P42  # noqa: E402

OUT = ROOT / "data" / "w33_pass11945_lepton_mu_tau_classes.json"
Pm = np.array([[1, 0, 0], [0, 0, 1], [0, 1, 0]])
COLS = {"nu1": (0.82, 0.36, 0.43), "nu2": (0.548, 0.605, 0.578), "nu3": (0.148, 0.74, 0.66)}
L = P42.LEPTONS
SEARCH_RECORD = dict(distinct_solutions={"A": 34, "B": 48}, max_min_odd=0.118, min_other_odd=0.612)


def odd(v):
    return float(np.linalg.norm(v - Pm @ v) / 2)


def leptons(Om, ze):
    Y = P42.normalised(Om, (0, ze)).T
    if not np.isfinite(Y).all():
        return 1e3, 1e3, [1.0, 1.0, 1.0]
    try:
        U, s, _ = np.linalg.svd(Y)
    except np.linalg.LinAlgError:
        return 1e3, 1e3, [1.0, 1.0, 1.0]                         # tau, mu, e
    return float(s[1] / s[0]), float(s[2] / s[1]), [odd(U[:, 2]), odd(U[:, 1]), odd(U[:, 0])]   # e, mu, tau


def main():
    rng = np.random.default_rng(11945)
    res = dict(pass_id=11945, columns=COLS, search_record=SEARCH_RECORD, fits={})
    for k, x in P42.FITS.items():
        x = np.array(x)
        c = x[0::2] + 1j * x[1::2]
        tau, td, eu, ed, zd = c
        Om = np.array([[tau, ed], [ed, td]])
        rule = leptons(Om, 6 * zd)
        sols = []
        for _ in range(120):
            p0 = [rng.uniform(-1, 1), rng.uniform(-0.06, 0.06)]
            r = least_squares(lambda p: [np.log(leptons(Om, 6 * zd - 5 * (p[0] + 1j * p[1]))[i] / v)
                                         for i, v in enumerate((L["mmu_mtau"], L["me_mmu"]))], p0, max_nfev=200)
            if r.cost < 1e-10:
                ze = 6 * zd - 5 * (r.x[0] + 1j * r.x[1])
                if abs(ze.imag) > 0.5:          # Gaussian centre Im z / Im tau_d beyond ~29 nears the N = 40 truncation
                    continue
                key = complex((ze.real + 0.5) % 1 - 0.5, ze.imag)
                if not any(abs(key - s["z"]) < 1e-4 for s in sols):
                    sols.append(dict(z=key, odd=leptons(Om, ze)[2]))
        prof = [sorted(s["odd"]) for s in sols]
        e_even = [s["odd"] for s in sols if s["odd"][0] < 0.12]
        def col_fit(target):
            best = None
            for _ in range(40):
                p0 = [rng.uniform(-0.5, 0.5), rng.uniform(-0.03, 0.03)]
                def f(p):
                    a, b, o = leptons(Om, 6 * zd - 5 * (p[0] + 1j * p[1]))
                    return [np.log(a / L["mmu_mtau"]) / 0.2, np.log(b / L["me_mmu"]) / 0.2] + [(o[i] - target[i]) / 0.05 for i in range(3)]
                r = least_squares(f, p0, max_nfev=300)
                if best is None or r.cost < best.cost:
                    best = r
            a, b, o = leptons(Om, 6 * zd - 5 * (best.x[0] + 1j * best.x[1]))
            return dict(chi2=float(2 * best.cost), mmu_mtau=a, me_mmu=b, odd_e_mu_tau=o,
                        sin2_theta23=o[1] ** 2 / (1 - o[0] ** 2), theta13_deg=float(np.degrees(np.arcsin(o[0]))))
        res["fits"][k] = dict(charge_rule_odd_e_mu_tau=rule[2], n_solutions=len(sols),
                              max_min_odd=max(p[0] for p in prof), min_other_odd=min(min(p[1:]) for p in prof),
                              e_even_class=dict(n=len(e_even), theta13_deg=[float(np.degrees(np.arcsin(min(o[0] for o in e_even)))), float(np.degrees(np.arcsin(max(o[0] for o in e_even))))],
                                                sin2_theta23=[min(o[1] ** 2 / (1 - o[0] ** 2) for o in e_even), max(o[1] ** 2 / (1 - o[0] ** 2) for o in e_even)]),
                              column_fits={n: col_fit(t) for n, t in COLS.items()})
    F = res["fits"]
    res["checks"] = {k: bool(v) for k, v in dict(
        charge_rule_muon_nearly_even=all(f["charge_rule_odd_e_mu_tau"][1] < 0.15 for f in F.values()),
        muon_needs_at_least_036=min(c[1] for c in COLS.values()) > 0.35,
        many_mass_solutions=all(f["n_solutions"] >= 10 for f in F.values()),
        every_solution_near_mu_tau_adapted=all(f["max_min_odd"] < 0.13 and f["min_other_odd"] > 0.58 for f in F.values()),
        odd_nu2_branch_impossible=all(f["column_fits"]["nu2"]["chi2"] > 30 and f["column_fits"]["nu1"]["chi2"] > 30 for f in F.values()),
        odd_nu3_branch_fits_except_theta13=all(f["column_fits"]["nu3"]["chi2"] < 10 and abs(f["column_fits"]["nu3"]["sin2_theta23"] - 0.561) < 0.03
                                               and f["column_fits"]["nu3"]["theta13_deg"] < 1.5 for f in F.values()),
        e_even_class_theta23_band_contains_data=all(f["e_even_class"]["n"] > 0 and f["e_even_class"]["sin2_theta23"][0] < 0.561 < f["e_even_class"]["sin2_theta23"][1] + 0.01 for f in F.values()),
    ).items()}
    res["all_checks_pass"] = all(res["checks"].values())
    OUT.write_text(json.dumps(res, indent=2, default=lambda o: [o.real, o.imag] if isinstance(o, complex) else float(o)))
    print(json.dumps(res["checks"], indent=1), res["all_checks_pass"])
    for k, f in F.items():
        print(k, f["n_solutions"], round(f["max_min_odd"], 3), round(f["min_other_odd"], 3), f["e_even_class"],
              {n: round(v["chi2"], 2) for n, v in f["column_fits"].items()}, round(f["column_fits"]["nu3"]["sin2_theta23"], 3))


if __name__ == "__main__":
    main()
