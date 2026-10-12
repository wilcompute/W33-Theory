"""Pass 11935: the E8 soft-supertrace angular selector is minimised exactly on the log(8/5) Clifford orbit.

Weld between two tracks.
* Parallel packet 8407e70cf (soft-supertrace hierarchy): near a Witting ray of the E8 84-Higgs Cartan, the mixed loop
  selector V_r = F + r G opens the 24 zero modes with total slope 8 and a finite angular coefficient C_G(u) depending on
  the tangent direction u in the flavour qutrit; an arbitrarily weak soft supertrace displaces the vacuum along the
  direction minimising C_G (log t* = -kappa/(32 r) - 1/2 - C_G/16). It reported an intermediate-magic witness and a
  branch optimum "near M2 = 0.4700".
* Pass 11926: Clifford/G25-invariant tangent potentials have special orbits; one has M2 = log(8/5), Clifford stabiliser
  of order 4, orbit 54, and unlocks m_c != m_u with O(1) ratios.

Result: minimising C_G over CP^2 from independent starts converges every time to C_G = 3.69343; polished with the
Clifford group the minimiser has M2 = log(8/5) to 1e-15, maximal Pauli expectation (1+sqrt3)/4 and Clifford stabiliser of
order 4 -- exactly the log(8/5) orbit. The soft-supertrace dynamics therefore selects a definite W(3,3)/Clifford orbit for
the flavour Higgs, below every other special orbit (strange 5.047, stabiliser 4.000, T/log(9/5) 3.742).
Flavour consequence (even g, g = (1, eps, eps)): every member of the orbit unlocks charm and up, but the ratios stay O(1)
as eps -> 0 (min m_c/m_t over the 54 members >= 0.36): the selected direction does not by itself give the up hierarchy,
which must come from the radial displacement / modulus (the essential-scaling weld of 8407e70cf), not the angle.
"""

import json
import sys
from pathlib import Path

import numpy as np
from scipy.optimize import minimize

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))
import w33_20261011_soft_supertrace_hierarchy as SS  # noqa: E402
import w33_pass11923_stabiliser_higgs_lock as H23  # noqa: E402
import w33_pass11926_g25_tangent_vacua as G26  # noqa: E402

OUT = ROOT / "data" / "w33_pass11935_soft_supertrace_selects_log85_orbit.json"
T = 2e-4


def cg(u):
    u = u / np.linalg.norm(u)
    return SS.local_coefficients(u, T)[1]


def main():
    rng = np.random.default_rng(11935)
    runs = []
    for _ in range(6):
        r = minimize(lambda x: cg(x[:3] + 1j * x[3:]), rng.normal(size=6), method="Nelder-Mead",
                     options=dict(maxiter=800, xatol=1e-7, fatol=1e-9))
        u = r.x[:3] + 1j * r.x[3:]
        runs.append((float(r.fun), u / np.linalg.norm(u)))
    runs.sort(key=lambda z: z[0])
    G = G26.clifford()
    pu, stab = G26.polish(runs[0][1], G)
    named = {"strange": np.array([0, 1, -1]) / np.sqrt(2), "stabiliser": np.array([1, 0, 0], complex),
             "T_log95": np.array([1, np.exp(2j * np.pi / 9), np.exp(-2j * np.pi / 9)]) / np.sqrt(3)}
    named_cg = {k: float(cg(v.astype(complex))) for k, v in named.items()}
    orbit = []
    for g in G:
        v = g @ pu
        orbit.append(v / np.linalg.norm(v))
    reps = []
    for v in orbit:                                   # projective deduplication
        if not any(abs(abs(np.vdot(v, w)) - 1) < 1e-9 for w in reps):
            reps.append(v)
    keyset = {i: v for i, v in enumerate(reps)}
    mins = []
    for v in keyset.values():
        s = np.linalg.svd(H23.Y(v, np.array([1, 1e-3, 1e-3])), compute_uv=False)
        mins.append(float(s[1] / s[0]))
    res = dict(pass_id=11935, cg_runs=[r[0] for r in runs], cg_min=runs[0][0], polished_M2=float(H23.magic(pu)),
               log_8_5=float(np.log(8 / 5)), polished_pauli_max=float(H23.pauli_max(pu)), clifford_stabiliser=int(stab),
               cg_polished=float(cg(pu)), named_cg=named_cg, orbit_size=len(keyset), min_mc_mt_over_orbit=min(mins),
               up_gap_polished=float(H23.gap(H23.Y(pu, np.array([1, 0.1, 0.1])))))
    res["checks"] = {k: bool(v) for k, v in dict(
        all_runs_same_minimum=max(res["cg_runs"]) - min(res["cg_runs"]) < 1e-5,
        minimiser_is_log85_orbit=abs(res["polished_M2"] - np.log(8 / 5)) < 1e-12 and stab == 4
        and abs(res["polished_pauli_max"] - (1 + np.sqrt(3)) / 4) < 1e-9,
        polished_point_is_minimum=abs(res["cg_polished"] - res["cg_min"]) < 1e-5,
        below_other_special_orbits=res["cg_min"] < min(named_cg.values()),
        orbit_size_54=len(keyset) == 54,
        unlocks_but_not_hierarchical=res["up_gap_polished"] > 1e-3 and res["min_mc_mt_over_orbit"] > 0.3,
    ).items()}
    res["all_checks_pass"] = all(res["checks"].values())
    OUT.write_text(json.dumps(res, indent=2))
    print(json.dumps({k: v for k, v in res.items() if k != "cg_runs"}, indent=1))


if __name__ == "__main__":
    main()
