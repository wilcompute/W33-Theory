"""Pass 11944: the theta central inversion is mu-tau reflection, and the mixing matrices measure its breaking.

1. Identification. The central inversion -1 of the level-3 structure acts on a flavour qutrit as c -> -c, i.e. the
   transposition (1 2) fixing 0. In a flavour basis (e, mu, tau) <-> (0, 1, 2) it is mu-tau reflection. Every
   zero-characteristic (Wilson-line-free) theta-null Yukawa commutes with it (Pass 11941), so every Wilson-free sector is
   mu-tau symmetric, and its odd mass state is exactly (0, 1, -1)/sqrt2.
2. Lemma (exact, any bases). If one sector is P-symmetric with odd state o, then for every state a of the other sector
   |<a|o>| = ||P_odd a|| (the odd subspace is one-dimensional). Checked on 2000 random bases (violation 1e-16 of the
   inequality form, and equality for the odd column).
   * Quarks: the up coupling is Wilson-free (11941/11942) and its odd state is the middle one (charm), so the CKM charm
     row is the odd content of the down states: |V_cd|, |V_cs|, |V_cb| = ||P_odd d||, ||P_odd s||, ||P_odd b||.
     The fits reproduce this identity to 1e-12; the data read (0.221, 0.975, 0.041).
   * Leptons: a Wilson-free neutrino sector with the near-product texture has the odd state at nu2 (exponent 1 between
     0 and 2; Pass 11943), so |U_e2|, |U_mu2|, |U_tau2| = odd contents of e, mu, tau. Data (NuFIT-like central values):
     (0.548, 0.60, 0.58) -- every charged lepton about one-third odd (close to TM2). The minimal fits of 11942 have
     (0.71, 0.08, 0.70), which is why 11943 failed.
3. The fork. The measured mixing fixes how much mu-tau parity must be broken:
   (a) odd neutrino = nu2 (near-product neutrinos, keeping the Weber relation of 11939/11940): ||P_odd l|| ~ 0.55-0.60
       for all three charged leptons -- O(1) breaking;
   (b) odd neutrino = nu3 (the usual mu-tau paradigm): only ||P_odd e|| >= |U_e3| = 0.148, comparable to the quark sector
       (||P_odd d|| = |V_cd| = 0.221). But nu3 odd needs the odd theta coefficient to dominate, |Omega12| = O(1), i.e.
       neutrinos outside the near-product regime -- which gives up the Weber neutrino relation (Sigma = 0.0596 eV).
   The data thus favour (b) on naturalness (comparable breaking in both sectors) and cost the 11939/11940 prediction its
   near-product premise unless the charged leptons are O(1) mu-tau-broken.
"""

import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))
import w33_pass11942_hypercharge_wilson_leptons as P42  # noqa: E402

OUT = ROOT / "data" / "w33_pass11944_mu_tau_parity_identities.json"
P = np.array([[1, 0, 0], [0, 0, 1], [0, 1, 0]])
ODD = np.array([0, 1, -1]) / np.sqrt(2)
CKM_C_ROW = dict(Vcd=0.221, Vcs=0.975, Vcb=0.0411)
PMNS = dict(s12sq=0.307, s23sq=0.561, s13sq=0.0220, delta_deg=212.0)


def odd_norm(v):
    return float(np.linalg.norm(v - P @ v) / 2)


def pmns_matrix(s12sq, s23sq, s13sq, delta_deg):
    s12, s23, s13 = np.sqrt([s12sq, s23sq, s13sq])
    c12, c23, c13 = np.sqrt([1 - s12sq, 1 - s23sq, 1 - s13sq])
    e = np.exp(1j * np.radians(delta_deg))
    return np.array([[c12 * c13, s12 * c13, s13 / e],
                     [-s12 * c23 - c12 * s23 * s13 * e, c12 * c23 - s12 * s23 * s13 * e, s23 * c13],
                     [s12 * s23 - c12 * c23 * s13 * e, -c12 * s23 - s12 * c23 * s13 * e, c23 * c13]])


def main():
    rng = np.random.default_rng(11944)
    res = dict(pass_id=11944)
    nu = np.column_stack([np.array([2, -1, -1]) / np.sqrt(6), ODD, np.ones(3) / np.sqrt(3)])
    viol, eq = 0.0, 0.0
    for _ in range(2000):
        Ue, _ = np.linalg.qr(rng.normal(size=(3, 3)) + 1j * rng.normal(size=(3, 3)))
        U = Ue.conj().T @ nu
        for a in range(3):
            viol = max(viol, abs(U[a, 1]) - odd_norm(Ue[:, a]))
            eq = max(eq, abs(abs(U[a, 1]) - odd_norm(Ue[:, a])))
    res["lemma_max_violation"] = viol
    res["odd_column_equality_max_dev"] = eq
    res["inversion_is_mu_tau_swap"] = bool(np.array_equal(P @ np.array([0, 1, 2]), np.array([0, 2, 1])))
    fits = {}
    for k, x in P42.FITS.items():
        x = np.array(x)
        c = x[0::2] + 1j * x[1::2]
        tau, td, eu, ed, zd = c
        Om = np.array([[tau, ed], [ed, td]])
        Uu = np.linalg.svd(P42.theta(np.array([[tau, eu], [eu, tau]])))[0]             # t, c, u
        Ud = np.linalg.svd(P42.normalised(Om, (0, zd)))[0]                              # b, s, d
        V = Uu.conj().T @ Ud
        charm_row = np.abs(V[1])
        down_odd = [odd_norm(Ud[:, i]) for i in range(3)]
        UL = np.linalg.svd(P42.normalised(Om, (0, 6 * zd)).T)[0]                      # tau, mu, e
        fits[k] = dict(charm_is_odd=float(abs(abs(np.vdot(ODD, Uu[:, 1])) - 1)), charm_row_b_s_d=charm_row.tolist(),
                       down_odd_b_s_d=down_odd, identity_dev=float(np.max(np.abs(charm_row - down_odd))),
                       lepton_odd_tau_mu_e=[odd_norm(UL[:, i]) for i in range(3)])
    res["fits"] = fits
    U = pmns_matrix(**PMNS)
    res["data_pmns_nu2_column_e_mu_tau"] = [float(abs(U[a, 1])) for a in range(3)]
    res["data_Ue3"] = float(abs(U[0, 2]))
    res["data_ckm_charm_row"] = CKM_C_ROW
    D = res["data_pmns_nu2_column_e_mu_tau"]
    res["checks"] = {k: bool(v) for k, v in dict(
        inversion_is_mu_tau_reflection=res["inversion_is_mu_tau_swap"],
        lemma_inequality=viol < 1e-12,
        odd_column_equals_odd_content=eq < 1e-12,
        up_charm_is_the_odd_state=all(f["charm_is_odd"] < 1e-9 for f in fits.values()),
        ckm_charm_row_is_down_odd_content=all(f["identity_dev"] < 1e-9 for f in fits.values()),
        fit_charm_row_matches_data=all(abs(f["down_odd_b_s_d"][2] - CKM_C_ROW["Vcd"]) < 0.01 and abs(f["down_odd_b_s_d"][0] - CKM_C_ROW["Vcb"]) < 0.002 for f in fits.values()),
        data_needs_all_leptons_one_third_odd=all(0.5 < d < 0.65 for d in D),
        minimal_fits_have_wrong_lepton_odd_content=all(min(f["lepton_odd_tau_mu_e"]) < 0.2 for f in fits.values()),
        branch_b_needs_only_mild_breaking=res["data_Ue3"] < CKM_C_ROW["Vcd"],
    ).items()}
    res["all_checks_pass"] = all(res["checks"].values())
    OUT.write_text(json.dumps(res, indent=2, default=float))
    print(json.dumps(res["checks"], indent=1), res["all_checks_pass"])
    print({k: (np.round(f["down_odd_b_s_d"], 4).tolist(), np.round(f["lepton_odd_tau_mu_e"], 3).tolist()) for k, f in fits.items()},
          np.round(D, 3), round(res["data_Ue3"], 4))


if __name__ == "__main__":
    main()
