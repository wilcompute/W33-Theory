"""Pass 11946: mu-tau-clean neutrinos are excluded in both branches -- the reactor angle measures mu-tau breaking in
the neutrino sector.

Inputs: Pass 11944 (identity: with a mu-tau-clean neutrino sector the odd neutrino's PMNS column equals the odd contents
of e, mu, tau) and Pass 11945 (with an H_d Wilson line the charged leptons fit both mass ratios, and every solution has
one nearly even lepton; branch (a), odd nu2, is impossible).

1. Branch (b), odd nu3, fails on theta13. With nu3 odd, |U_e3| = ||P_odd e|| exactly. In the e-even class (the class
   needed for theta23) the electron's odd content is at most ~0.0095 over all solutions on both quark fits, so
   theta13 <= 0.54 deg, against the measured 8.6 deg.
2. Nor can the neutrino sector place nu3 odd by itself in the direct theta texture. Over random swap-symmetric homes
   Omega = [[tau, w], [w, tau]] (any w), the odd state is the heaviest in only 0.3-0.5% of homes (two scans), and always
   quasi-degenerately: Dm21/Dm31 >= 0.26 there, against 0.0296 measured. (A seesaw with different Dirac and Majorana homes
   can make nu3 odd and hierarchical, but cannot help theta13, which item 1 bounds from the charged-lepton side.)
3. Hence: with the charged leptons of Pass 11945, a mu-tau-clean neutrino sector is excluded in both branches. The
   reactor angle requires mu-tau breaking in the neutrino sector itself, of size ||P_odd||_nu ~ |U_e3| = 0.148 -- comparable
   to the down-sector breaking that gives the Cabibbo angle (|V_cd| = 0.221, Pass 11944). The minimal source compatible with
   the charge rule of Pass 11942 is a Wilson line on H_u entering the Dirac coupling L N H_u (argument h_u, not fixed by
   the rule). This also removes the Wilson-free premise of the 11939/11940 neutrino relation, as Pass 11945 already
   indicated.
"""

import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))
import w33_pass11945_lepton_mu_tau_classes as M45  # noqa: E402
from w33_pass11869_11873_siegel_level3_two_qutrits import theta_null_2  # noqa: E402

OUT = ROOT / "data" / "w33_pass11946_reactor_angle_needs_neutrino_breaking.json"
C45 = ROOT / "data" / "w33_pass11945_lepton_mu_tau_classes.json"
ODD = np.array([0, 1, -1]) / np.sqrt(2)
DATA = dict(Ue3=0.148, theta13_deg=8.6, dm_ratio=7.42e-5 / 2.51e-3, Vcd=0.221)


def main():
    if not C45.exists():
        M45.main()
    c45 = json.loads(C45.read_text())
    rng = np.random.default_rng(11946)
    res = dict(pass_id=11946, data=DATA)
    res["e_even_class_theta13_max_deg"] = max(f["e_even_class"]["theta13_deg"][1] for f in c45["fits"].values())
    res["odd_nu2_branch_chi2"] = {k: f["column_fits"]["nu2"]["chi2"] for k, f in c45["fits"].items()}
    n_valid, hits = 0, []
    for _ in range(8000):
        tau = rng.uniform(-0.5, 0.5) + 1j * rng.uniform(0.3, 2.5)
        w = rng.uniform(-0.5, 0.5) + 1j * rng.uniform(-1, 1) * tau.imag * 0.95
        Om = np.array([[tau, w], [w, tau]])
        if np.linalg.eigvalsh(Om.imag).min() < 0.05:
            continue
        n_valid += 1
        U, s, _ = np.linalg.svd(theta_null_2(Om, N=25).reshape(3, 3))
        if int(np.argmax([abs(np.vdot(ODD, U[:, i])) for i in range(3)])) == 0:
            r32, r21 = s[1] / s[0], s[2] / s[1]
            hits.append(float(r32**2 * (1 - r21**2) / (1 - r32**2 * r21**2)))
    res["direct_scan"] = dict(valid=n_valid, odd_heaviest=len(hits), fraction=len(hits) / n_valid,
                              dm_ratio_min=min(hits) if hits else None)
    res["checks"] = {k: bool(v) for k, v in dict(
        branch_b_theta13_bounded_below_one_degree=res["e_even_class_theta13_max_deg"] < 1.0 < DATA["theta13_deg"],
        branch_a_impossible_per_11945=all(v > 30 for v in res["odd_nu2_branch_chi2"].values()),
        odd_heaviest_is_rare=res["direct_scan"]["fraction"] < 0.02 and len(hits) > 5,
        odd_heaviest_is_quasi_degenerate=res["direct_scan"]["dm_ratio_min"] > 5 * DATA["dm_ratio"],
        needed_breaking_comparable_to_quarks=0.5 < DATA["Ue3"] / DATA["Vcd"] < 1.0,
    ).items()}
    res["all_checks_pass"] = all(res["checks"].values())
    OUT.write_text(json.dumps(res, indent=2, default=float))
    print(json.dumps(res["checks"], indent=1), res["all_checks_pass"], res["e_even_class_theta13_max_deg"], res["direct_scan"])


if __name__ == "__main__":
    main()
