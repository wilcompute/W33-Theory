"""Pass 11925: W(3,3) seen from the Witting-tangent flavour qutrit -- collinear points are the stabiliser states (the
charm-up lock of Pass 11903), non-collinear points are the maximally magic strange states (the theta-zero law of Pass
11904).

Setting: the flavour-Higgs qutrit is the transverse tangent of a Witting ray v of the E8 84-Higgs Cartan (parallel
packet 34e149d79: same H27 / G25 matrices). Take v = e0 among the 40 Witting rays of C^4 (Pass 11879 list); then
X = cyclic shift and Z = diag(1, w, w^2) on v-perp = span(e1, e2, e3) lie in the stabiliser of v and permute the rays.

1. The 12 rays orthogonal to v (= W(3,3) points collinear with v, Pass 11681) are exactly the 12 qutrit stabiliser
   states; the 4 isotropic lines through v are the 4 stabiliser bases (pairwise-orthogonal triples).
2. The 27 non-collinear rays (|<v,w>|^2 = 1/3) project onto v-perp 3:1 onto 9 states -- one per hyperbolic line through
   v -- forming the Clifford orbit of the qutrit strange state (0,1,-1)/sqrt2, each with stabiliser Renyi magic
   M2 = log 2, the maximum over qutrit states.
3. Physics of the two classes in the common up Yukawa Y_u(h)_{ab} = h_{a+b} g_{a-b} (g even, Passes 11918-11924):
   stabiliser h gives (1, eps, eps) -- m_c = m_u, the lock of 11903; strange h gives (1, 1, 0) EXACTLY for every even g
   -- m_u = 0 with m_t = m_c, the theta-zero law of 11904. Both W(3,3) classes are degenerate; realistic up masses need
   an intermediate, reflection-breaking Higgs state (consistent with 11923/11924).
4. Tested non-result: 'F-flat second vevs are collinear' fails -- Pass 11681's "orthogonal = commuting" is Pauli
   commutation; all Cartan (Witting) vevs commute under the E8 bracket, so F-flatness does not distinguish collinear from
   non-collinear directions.
"""

import json
import sys
from pathlib import Path

import numpy as np
from scipy.optimize import minimize

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))
import w33_pass11879_11883_e8_higgs_siegel_modulus as P  # noqa: E402

OUT = ROOT / "data" / "w33_pass11925_w33_on_the_flavour_qutrit.json"
W = np.exp(2j * np.pi / 3)
X = np.roll(np.eye(3), 1, axis=0)
Z = np.diag([1, W, W * W])
PAULI_ALL = [np.linalg.matrix_power(X, a) @ np.linalg.matrix_power(Z, b) for a in range(3) for b in range(3)]
STAB = [np.eye(3)[k] for k in range(3)] + [np.array([W ** (s * j * j + t * j) for j in range(3)]) / np.sqrt(3)
                                           for s in range(3) for t in range(3)]


def M2(h):
    return float(-np.log(sum(abs(np.vdot(h, Pm @ h)) ** 4 for Pm in PAULI_ALL) / 3))


def Y(h, g):
    return np.array([[h[(a + b) % 3] * g[(a - b) % 3] for b in range(3)] for a in range(3)])


def main():
    rays = [r / np.linalg.norm(r) for r in P.witting_rays()]
    v = rays[0]
    # X, Z (extended by 1 on e0) permute the 40 rays
    def permutes(U4):
        return all(max(abs(np.vdot(s, U4 @ r)) for s in rays) > 1 - 1e-12 for r in rays)
    X4 = np.eye(4, dtype=complex); X4[1:, 1:] = X
    Z4 = np.eye(4, dtype=complex); Z4[1:, 1:] = Z
    orth = [r for r in rays[1:] if abs(np.vdot(v, r)) < 1e-12]
    non = [r for r in rays[1:] if abs(np.vdot(v, r)) > 1e-12]

    def proj(r):
        u = r[1:]
        return u / np.linalg.norm(u)

    po = [proj(r) for r in orth]
    orth_are_stab = min(max(abs(np.vdot(s, p)) for s in STAB) for p in po)
    G = np.array([[abs(np.vdot(a, b)) for b in orth] for a in orth])
    lines = {tuple(sorted([i] + [j for j in range(12) if G[i, j] < 1e-12])) for i in range(12)}
    reps, fibre = [], []
    for r in non:
        p = proj(r)
        k = next((i for i, q in enumerate(reps) if abs(abs(np.vdot(q, p)) - 1) < 1e-12), None)
        if k is None:
            reps.append(p)
            k = len(reps) - 1
        fibre.append(k)
    # each fibre lies in one hyperbolic line: span(v, w) contains the 3 rays of the fibre
    hyper_ok = True
    for k in range(len(reps)):
        ws = [non[i] for i in range(len(non)) if fibre[i] == k]
        Bm = np.array([v, ws[0]]).T
        for w_ in ws[1:]:
            c = np.linalg.lstsq(Bm, w_, rcond=None)[0]
            hyper_ok &= bool(np.linalg.norm(Bm @ c - w_) < 1e-12)
    strange = np.array([0, 1, -1]) / np.sqrt(2)
    rng = np.random.default_rng(11925)
    best = 0.0
    for _ in range(40):
        r = minimize(lambda x: -M2((x[:3] + 1j * x[3:]) / np.linalg.norm(x[:3] + 1j * x[3:])), rng.normal(size=6),
                     method="Nelder-Mead", options=dict(maxiter=4000, xatol=1e-10, fatol=1e-13))
        best = max(best, -r.fun)
    # Yukawa spectra of the two classes over random even g
    stab_gap, strange_dev = 0.0, 0.0
    for _ in range(100):
        e = rng.normal() + 1j * rng.normal()
        g = np.array([rng.normal() + 1j * rng.normal(), e, e])
        for h in STAB:
            s = np.linalg.svd(Y(h, g), compute_uv=False)
            stab_gap = max(stab_gap, min(abs(s[0] - s[1]), abs(s[1] - s[2])) / s[0])
        for h in reps:
            s = np.linalg.svd(Y(h, g), compute_uv=False)
            strange_dev = max(strange_dev, abs(s[0] - s[1]) / s[0] + s[2] / s[0])
    res = dict(pass_id=11925, rays=len(rays), X_Z_permute_rays=permutes(X4) and permutes(Z4),
               collinear=len(orth), noncollinear=len(non), noncollinear_overlap=sorted(set(np.round([abs(np.vdot(v, r)) ** 2 for r in non], 10))),
               collinear_min_fidelity_to_stabiliser=float(orth_are_stab), isotropic_lines_through_v=len(lines),
               projected_strange_states=len(reps), fibre_sizes=sorted(np.bincount(fibre).tolist()), fibres_are_hyperbolic_lines=hyper_ok,
               strange_in_orbit=any(abs(abs(np.vdot(strange, p)) - 1) < 1e-12 for p in reps),
               M2_projected=sorted(set(np.round([M2(p) for p in reps], 10))), M2_max_found=best,
               stabiliser_yukawa_max_gap=stab_gap, strange_yukawa_deviation_from_110=strange_dev)
    res["checks"] = {k: bool(val) for k, val in dict(
        hessian_paulis_permute_witting_rays=res["X_Z_permute_rays"],
        collinear_points_are_the_12_stabiliser_states=len(orth) == 12 and orth_are_stab > 1 - 1e-12,
        four_isotropic_lines_are_four_bases=len(lines) == 4 and all(len(t) == 3 for t in lines),
        noncollinear_project_3to1_onto_9_strange_states=len(non) == 27 and len(reps) == 9 and res["fibre_sizes"] == [3] * 9
        and hyper_ok and res["strange_in_orbit"],
        strange_states_have_maximal_magic=abs(res["M2_projected"][0] - np.log(2)) < 1e-9 and len(res["M2_projected"]) == 1
        and best < np.log(2) + 1e-7,
        stabiliser_higgs_locks_mc_mu=stab_gap < 1e-12,
        strange_higgs_gives_theta_zero_law=strange_dev < 1e-12,
    ).items()}
    res["all_checks_pass"] = all(res["checks"].values())
    OUT.write_text(json.dumps(res, indent=2))
    print(json.dumps(res, indent=1))


if __name__ == "__main__":
    main()
