"""Pass 11943: the minimal theta-null SU(5) picture gets the PMNS matrix wrong -- and a correction to Pass 11942.

Setting (Passes 11938-11942). The lepton doublet L sits on the 5bar factor (tau_d, cusp regime). The charged-lepton
coupling is Y_e = Y_d^T with the hypercharge Wilson argument z_e = 6 z_d (11942). The Dirac coupling L N H_u has
Wilson argument -Y_N a = 0 by the same charge rule, so with a near-product seesaw (11940) the neutrino left basis is the
parity-clean Gram-Schmidt basis of f_0, f_1, f_2 at tau_d, ordered nu3, nu2, nu1. PMNS = U_e^dagger U_nu is then fixed by
the quark fit, with no free parameter.

1. No-go (robust).
   Best fits: A -> (theta12, theta23, theta13) = (45.1, 83.0, 1.1) deg; B -> (88.6, 5.7, 45.1) deg.
   Data: (33.4, 49, 8.6).
   Quark-data posterior (frozen record; 2 chains x 3000 steps, 38 thinned samples each):
     A: theta12 44.8-45.2, theta23 80.3-85.2, theta13 0.3-1.7;   B: 86.8-88.6, 2.6-5.0, 45.1-45.2 (5-95%).
   Changing the neutrino Wilson rule (z_nu/z_d in {1, 2, 3, -3/2, -3, 6}) does not help at either best fit.
2. Why. Near the cusp the parity-clean 5bar basis is (numerically, at the fitted tau_d) the tri-bimaximal set of vectors:
   (1,1,1)/sqrt3, (0,1,-1)/sqrt2, (2,-1,-1)/sqrt6 -- the familiar S3/TBM structure already in the corpus (BT920, Pass
   11225, Pass 11243). But the theta parity puts the mu-tau-odd vector (0,1,-1)/sqrt2 = f_1 at the MIDDLE mass (it enters
   at order Omega12), whereas TBM/TM1 need it to be nu3. With a charged-lepton basis near the qutrit basis this gives
   theta12 ~ 0 and theta13 ~ 35 deg. The hypercharge-Wilson charged-lepton basis is instead nearly democratic, which
   rotates the TBM vectors into near-trivial or near-permutation mixing. Large, non-maximal PMNS needs the charged-lepton
   and neutrino L-bases at different points of the level-3 geometry (a residual-symmetry misalignment, cf. 11225/11243),
   which the minimal picture does not provide.
3. Correction to Pass 11942. A fifth MCMC chain (branch B, seed 7, median chi^2 4.4) gives m_mu/m_tau 0.029-0.046 and
   m_e/m_mu 0.0071-0.017 (5-95%), EXCLUDING the data (0.0588, 0.00474). The 11942 statement "both measured ratios lie
   near the centre of every chain's band" is withdrawn. What survives: over the quark-acceptable region the rule
   z_e = 6 z_d gives m_mu/m_tau ~ 0.029-0.081 and m_e/m_mu ~ 0.002-0.017 (union of 5 chains), which contains the data
   and excludes minimal SU(5) (0.0185, 0.050): the right direction and order (Georgi-Jarlskog-like), not a sharp
   prediction.
"""

import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))
import w33_pass11942_hypercharge_wilson_leptons as P42  # noqa: E402

OUT = ROOT / "data" / "w33_pass11943_pmns_no_go_and_lepton_band.json"
DATA_ANGLES = (33.4, 49.0, 8.6)
POSTERIOR_PMNS = {"A": dict(theta12=[44.8, 44.9, 45.2], theta23=[80.3, 82.9, 85.2], theta13=[0.3, 1.3, 1.7]),
                  "B": dict(theta12=[86.8, 87.9, 88.6], theta23=[2.6, 3.8, 5.0], theta13=[45.1, 45.2, 45.2])}
LEPTON_CHAINS = dict(P42.POSTERIOR)
LEPTON_CHAINS["B7"] = dict(chi2_med=4.37, mmu_mtau=[0.0289, 0.0363, 0.0459], me_mmu=[0.00714, 0.01134, 0.01704], yb_ytau=[1.088, 1.13, 1.18])
LEPTON_CHAINS["A7"] = dict(chi2_med=5.60, mmu_mtau=[0.0363, 0.0516, 0.0687], me_mmu=[0.0027, 0.00557, 0.01471], yb_ytau=[1.088, 1.219, 1.325])
TBM = [np.array([1, 1, 1]) / np.sqrt(3), np.array([0, 1, -1]) / np.sqrt(2), np.array([2, -1, -1]) / np.sqrt(6)]


def fk(tau, k, z=0.0, N=60):
    n = np.arange(-N, N + 1)
    return np.array([np.sum((n + c / 3) ** k * np.exp(3j * np.pi * tau * (n + c / 3) ** 2 + 6j * np.pi * (n + c / 3) * z)) for c in range(3)])


def gram_schmidt(vs):
    out = []
    for v in vs:
        w = v.astype(complex)
        for u in out:
            w = w - np.vdot(u, w) * u
        out.append(w / np.linalg.norm(w))
    return np.array(out).T


def angles(U):
    s13 = abs(U[0, 2])
    c13 = np.sqrt(1 - s13**2)
    return [float(x) for x in np.degrees([np.arcsin(min(1, abs(U[0, 1]) / c13)), np.arcsin(min(1, abs(U[1, 2]) / c13)), np.arcsin(s13)])]


def main():
    res = dict(pass_id=11943, data_angles=DATA_ANGLES, posterior_pmns_frozen=POSTERIOR_PMNS, lepton_chains=LEPTON_CHAINS, fits={})
    for lab, x in P42.FITS.items():
        x = np.array(x)
        c = x[0::2] + 1j * x[1::2]
        tau, td, eu, ed, zd = c
        Om = np.array([[tau, ed], [ed, td]])
        Ue = np.linalg.svd(P42.normalised(Om, (0, 6 * zd)).T)[0][:, ::-1]       # e, mu, tau
        rules = {}
        for r in (0, 1, 2, 3, -1.5, -3, 6):
            Fn = gram_schmidt([fk(td, 0, r * zd), fk(td, 1, r * zd), fk(td, 2, r * zd)])
            rules[str(r)] = angles(Ue.conj().T @ Fn[:, ::-1])
        Fn0 = gram_schmidt([fk(td, 0), fk(td, 1), fk(td, 2)])
        tbm_dev = max(min(np.linalg.norm(np.abs(Fn0[:, j]) - np.abs(t)) for t in TBM) for j in range(3))
        odd_is_middle = abs(abs(np.vdot(Fn0[:, 1], TBM[1])) - 1) < 1e-9
        res["fits"][lab] = dict(angles_by_rule=rules, tbm_vector_deviation=float(tbm_dev), mu_tau_odd_is_middle_mass=bool(odd_is_middle))
    F = res["fits"]
    far = lambda a: abs(a[1] - DATA_ANGLES[1]) > 25 or abs(a[2] - DATA_ANGLES[2]) > 7
    union_mu = [min(b["mmu_mtau"][0] for b in LEPTON_CHAINS.values()), max(b["mmu_mtau"][2] for b in LEPTON_CHAINS.values())]
    union_e = [min(b["me_mmu"][0] for b in LEPTON_CHAINS.values()), max(b["me_mmu"][2] for b in LEPTON_CHAINS.values())]
    res["lepton_union_band"] = dict(mmu_mtau=union_mu, me_mmu=union_e)
    L = P42.LEPTONS
    res["checks"] = {k: bool(v) for k, v in dict(
        pmns_fails_at_both_best_fits=all(far(f["angles_by_rule"]["0"]) for f in F.values()),
        no_neutrino_wilson_rule_rescues=all(far(a) for f in F.values() for a in f["angles_by_rule"].values()),
        posterior_pmns_far_from_data=all(abs(p["theta23"][1] - 49) > 30 for p in POSTERIOR_PMNS.values()),
        neutrino_basis_is_tbm_vectors=all(f["tbm_vector_deviation"] < 0.02 for f in F.values()),
        mu_tau_odd_state_is_middle_mass=all(f["mu_tau_odd_is_middle_mass"] for f in F.values()),
        chain_B7_excludes_lepton_data=not (LEPTON_CHAINS["B7"]["mmu_mtau"][0] < L["mmu_mtau"] < LEPTON_CHAINS["B7"]["mmu_mtau"][2]),
        union_band_contains_data_excludes_minimal_su5=union_mu[0] < L["mmu_mtau"] < union_mu[1] and union_e[0] < L["me_mmu"] < union_e[1]
        and not (union_mu[0] < 0.01853 < union_mu[1] and union_e[0] < 0.0504 < union_e[1]),
    ).items()}
    res["all_checks_pass"] = all(res["checks"].values())
    OUT.write_text(json.dumps(res, indent=2, default=float))
    print(json.dumps(res["checks"], indent=1), res["all_checks_pass"])
    for k, f in F.items():
        print(k, f["tbm_vector_deviation"], {r: [round(a, 1) for a in v] for r, v in f["angles_by_rule"].items()})
    print(res["lepton_union_band"])


if __name__ == "__main__":
    main()
