"""Pass 11649: the maximally time-asymmetric qutrit state, a parameter-free CP vacuum, and its Weyl filter.

h6 (Passes 11419/11434) is the unique lowest-degree time-odd Clifford invariant of a qutrit ray (bidegree (6,6)),
explicitly h6 = R(p_a^3 p_b^2 p_c) (odd Reynolds average over the 432-element extended Clifford group).

FOUND HERE.
  * max over unit states of |h6| = sqrt3 / 62208 (= (81/16) sqrt3 / (432 * 3^6)), attained at
        psi* = (0, cos(pi/8), sin(pi/8) e^(5 pi i/6))
    and its images: ALL 200 random BFGS starts converge to this value, and every end point lies in the extended-Clifford
    orbit of psi*.  The orbit has 144 rays: 72 with h6 > 0 (one unitary-Clifford orbit, stabiliser of order 3) and
    their 72 time reverses with h6 < 0.
  * psi* lies on a stabiliser line (a line of the Z triangle, Pi_Z = 0) with the qubit 'H-magic' amplitudes
    cos(pi/8), sin(pi/8); the other three MUBs have IDENTICAL spectra.  Hence at psi*: the Hesse doublet sits at a
    stabiliser vertex (j = infinity), Pass 11600's CP discriminant W = 0, and every label-blind arrow vanishes
    (Pass 11648) -- the strongest arrow of time is invisible to the Hesse CP order parameter and to label-blind data.
  * FIXED-RADIUS CP SELECTOR. On a supplied sphere, -lam h6(psi)^2 selects the candidate144-ray orbit if the
    global maximizer conjecture holds. The originally proposed quartic radial term cannot stabilize it: h6 has
    degree12, so its negative square has degree24 and the unrestricted potential is unbounded below.
    Intake11663 withdraws the radial-vacuum claim while retaining the unit-sphere search and filter algebra.
  * WEYL FILTER (Passes 11593/11607 carrier): h6 is odd exactly under the antiunitary coset, so h6 Chi is invariant
    under the diagonal action, and H_gap = lam [ (sqrt3/62208) |psi|^12 I + h6 Chi ]^2 is positive with
    H_gap = 4 lam (sqrt3/62208)^2 P_s at a vacuum (P_s = (I + s Chi)/2): an exact Weyl kernel Chi = -s.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
from scipy.optimize import minimize

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))
import w33_pass11357_jarlskog_degree_by_dimension as P7  # noqa: E402
import w33_pass11434_h6_explicit as H  # noqa: E402

OUT = ROOT / "data" / "w33_pass11649_maximal_arrow_state.json"
ST, _ = H.stabiliser_states()
CL = P7.clifford_group(3)
PERMS = H.group_permutations(CL, ST)
PM = np.array([p for p, _ in PERMS])
SG = np.array([s for _, s in PERMS], float)
G = np.abs(ST.conj() @ ST.T) ** 2
MUBS = []
for i in range(12):
    if not any(i in m for m in MUBS):
        MUBS.append([i] + [j for j in range(12) if j != i and G[i, j] < 1e-9])
M6 = (MUBS[0][0],) * 3 + (MUBS[1][0],) * 2 + (MUBS[2][0],)
STAR = np.array([0, np.cos(np.pi / 8), np.sin(np.pi / 8) * np.exp(5j * np.pi / 6)])
H6MAX = np.sqrt(3) / 62208


def probs(psi):
    return np.abs(ST.conj() @ psi) ** 2


def h6(psi):
    p = probs(psi)
    v = np.ones(len(PM))
    for i in M6:
        v = v * p[PM[:, i]]
    return float((SG * v).mean())


def unit(x):
    psi = x[:3] + 1j * x[3:]
    return psi / np.linalg.norm(psi)


def orbit(psi):
    rays = []
    for U in CL:
        for anti in (False, True):
            v = U @ (np.conj(psi) if anti else psi)
            if not any(abs(abs(np.vdot(v, r)) - 1) < 1e-9 for r in rays):
                rays.append(v)
    return rays


def main():
    res = dict(pass_id=11649)
    val = h6(STAR)
    res["h6_at_star"] = val
    res["equals_minus_sqrt3_over_62208"] = bool(abs(val + H6MAX) < 1e-15)
    orb = orbit(STAR)
    signs = [np.sign(h6(r)) for r in orb]
    res["orbit_size"] = len(orb)
    res["orbit_positive"] = int(sum(s > 0 for s in signs))
    res["unitary_stabiliser_order"] = len(CL) // (len(orb) // 2)
    rng = np.random.default_rng(11649)
    vals, in_orbit = [], 0
    for _ in range(200):
        r = minimize(lambda x: -abs(h6(unit(x))), rng.normal(size=6), method="BFGS", options=dict(gtol=1e-12))
        psi = unit(r.x)
        vals.append(-r.fun)
        in_orbit += any(abs(abs(np.vdot(psi, o)) - 1) < 1e-6 for o in orb)
    vals = np.array(vals)
    res["random_starts"] = 200
    res["starts_reaching_max"] = int((vals > H6MAX * (1 - 1e-8)).sum())
    res["end_points_in_orbit"] = int(in_orbit)
    res["max_found"] = float(vals.max())
    p = probs(STAR)
    res["mub_spectra_at_star"] = [sorted(np.round(p[m], 12).tolist()) for m in MUBS]
    res["three_mubs_share_a_spectrum"] = bool(all(np.allclose(sorted(p[MUBS[1]]), sorted(p[m])) for m in MUBS[2:]))
    res["Pi_Z_at_star"] = float(np.prod(p[MUBS[0]]))
    # Weyl filter algebra on a toy chirality
    Chi = np.diag([1.0] * 16 + [-1.0] * 16)
    for s in (1, -1):
        Hg = (H6MAX * np.eye(32) + s * H6MAX * Chi) @ (H6MAX * np.eye(32) + s * H6MAX * Chi)
        Ps = (np.eye(32) + s * Chi) / 2
        res[f"H_gap_equals_4_h6max^2_P_s_(s={s})"] = bool(np.allclose(Hg, 4 * H6MAX ** 2 * Ps))
    print(res, flush=True)
    json.dump(res, open(OUT, "w"), indent=1, default=str)


if __name__ == "__main__":
    main()
