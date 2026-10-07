"""Pass 11659: the 45 Burkhardt nodes are the 45 two-qutrit determinants (qutrit concurrences), and every complete
factorisation frame obeys a monogamy sum rule.

In the two-qutrit Hesse space (Passes 11651, 11657), the unit root n_F of the reflection of a tensor factorisation F
(a Burkhardt node) pairs with the Hesse vector u(psi) = B^T psi^(x3) as
        <n_F, u(psi)> = det(psi_F)      EXACTLY (ratio 1, spread 1e-15; F = the standard factorisation, psi_F = the 3x3
                                          coefficient matrix; all other F by Clifford covariance),
the SL3 x SL3-invariant cubic whose modulus^(2/3) is Gour's G-concurrence.  Consequences:
  * the node of F annihilates every F-product state; |det_F|^2 <= 1/27 with equality exactly at maximal F-entanglement;
  * the 45 determinants of the 45 factorisations span only a 5-dim space: they satisfy 40 linear relations;
  * GQ(4,2) LINES = the 27 complete factorisation frames (Pass 11177) = 5 mutually orthogonal nodes = orthonormal bases of
    the Hesse space, so for EVERY frame and every state
        sum_{F in frame} |det_F psi|^2 = |u(psi)|^2 = (M3 - 2)/6 <= 1/9      (M3 = stabiliser third moment, Pass 11651)
    -- a MONOGAMY RELATION for qutrit concurrence: at most 3 of the 5 factorisations of a frame can be maximally entangled
    at once (achieved), and 4 of them reach at most ~0.0156 each (numerical; the sum rule alone gives 1/36).
  * (A tested non-result: being simultaneously maximally entangled across TWO factorisations is possible both for
    orthogonal and for non-orthogonal nodes -- 1/27 in both cases with a converged constrained optimiser; an early
    unconverged Nelder-Mead run suggested otherwise.)
"""

from __future__ import annotations

import itertools
import json
import sys
from pathlib import Path

import numpy as np
from scipy.optimize import minimize

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))
import w33_pass11350_linear_decider as L  # noqa: E402
import w33_pass11651_n_qutrit_hesse_space as H  # noqa: E402
import w33_pass11657_hesse_space_geometrises_w33 as G7  # noqa: E402

OUT = ROOT / "data" / "w33_pass11659_burkhardt_nodes_are_concurrences.json"


def main():
    rng = np.random.default_rng(11659)
    d, pts, idx, B, wg = H.setup(2)
    D = L.Decider(2)
    Om = D.wl.Om
    u = lambda psi: B.T @ np.kron(np.kron(psi, psi), psi)  # noqa: E731

    def rs(n):
        x = rng.normal(size=n) + 1j * rng.normal(size=n)
        return x / np.linalg.norm(x)
    res = dict(pass_id=11659)
    par2 = np.zeros((9, 9))
    for a in pts:
        par2[idx[(a[0], (-a[1]) % 3)], idx[a]] = 1
    r = G7.reflection_root(H.R_of(B, par2))
    ratios = np.array([np.vdot(r, u(p)) / np.linalg.det(p.reshape(3, 3)) for p in (rs(9) for _ in range(300))])
    ph = ratios.mean() / abs(ratios.mean())
    r = r * np.conj(ph)                                                  # fix the root's phase
    ratios = ratios * np.conj(ph)
    res["node_over_det_mean"] = [float(ratios.mean().real), float(ratios.mean().imag)]
    res["node_over_det_spread"] = float(np.abs(ratios - ratios.mean()).max())
    res["node_kills_products_max"] = float(max(abs(np.vdot(r, u(np.kron(rs(3), rs(3))))) for _ in range(500)))
    bell = np.zeros(9, complex)
    for a in range(3):
        bell[idx[(a, a)]] = 1 / np.sqrt(3)
    res["det2_maximally_entangled"] = float(abs(np.vdot(r, u(bell))) ** 2)
    # the 45 nodes
    vecs = [np.array(v) for v in itertools.product(range(3), repeat=4) if any(v)]
    roots = []
    for u_ in vecs:
        for w_ in vecs:
            if (u_ @ Om @ w_) % 3:
                perp = [x for x in vecs if (x @ Om @ u_) % 3 == 0 and (x @ Om @ w_) % 3 == 0]
                c1 = perp[0]
                c2 = next(x for x in perp if (c1 @ Om @ x) % 3)
                Bm = np.stack([u_, w_, c1, c2], 1)
                sig = (Bm @ np.diag([2, 2, 1, 1]) @ (L.R._inv_mod3(Bm % 3) % 3)) % 3
                rr = G7.reflection_root(H.R_of(B, D.weil(sig)))
                if not any(abs(abs(np.vdot(rr, q)) - 1) < 1e-8 for q in roots):
                    roots.append(rr)
        if len(roots) == 45:
            break
    Rt = np.array(roots)
    res["nodes"] = len(roots)
    res["rank_of_45_nodes"] = int(np.linalg.matrix_rank(Rt, tol=1e-9))
    res["linear_relations_among_45_determinants"] = 45 - res["rank_of_45_nodes"]
    A = (np.abs(Rt.conj() @ Rt.T) ** 2 < 1e-8) & ~np.eye(45, dtype=bool)
    frames = set()
    for i in range(45):
        nb = [j for j in range(45) if A[i, j]]
        for c in itertools.combinations(nb, 4):
            if all(A[a, b] for a, b in itertools.combinations(c, 2)):
                frames.add(frozenset((i,) + c))
    frames = [sorted(f) for f in frames]
    res["frames_(5_mutually_orthogonal_nodes)"] = len(frames)
    lag, bases = H.stabiliser_bases(2)
    allst = np.concatenate(bases, 1)
    worst = 0.0
    for _ in range(200):
        psi = rs(9)
        M3 = (np.abs(allst.conj().T @ psi) ** 6).sum()
        for f in frames:
            worst = max(worst, abs(sum(abs(np.vdot(Rt[i], u(psi))) ** 2 for i in f) - (M3 - 2) / 6))
    res["frame_sum_rule_max_error_(27_frames_x_200_states)"] = float(worst)

    def maxmin(qs, starts):
        best = 0.0
        for _ in range(starts):
            x0 = np.concatenate([rng.normal(size=18), [0.0]])

            def d2(x, q):
                psi = x[:9] + 1j * x[9:18]
                psi = psi / np.linalg.norm(psi)
                return abs(np.vdot(q, u(psi))) ** 2
            cons = [dict(type="ineq", fun=(lambda x, q=q: d2(x, q) - x[18])) for q in qs]
            out = minimize(lambda x: -x[18], x0, method="SLSQP", constraints=cons, options=dict(maxiter=3000, ftol=1e-14))
            if out.success:
                best = max(best, min(d2(out.x, q) for q in qs))
        return best
    f0 = frames[0]
    res["max_min_det2_3_of_a_frame"] = maxmin([Rt[i] for i in f0[:3]], 30)
    res["max_min_det2_4_of_a_frame"] = maxmin([Rt[i] for i in f0[:4]], 30)
    j_orth = next(j for j in range(45) if abs(np.vdot(Rt[j], r)) < 1e-8)
    j_non = next(j for j in range(45) if 1e-3 < abs(np.vdot(Rt[j], r)) < 1 - 1e-6)
    res["two_factorisations_orthogonal_nodes"] = maxmin([r, Rt[j_orth]], 30)
    res["two_factorisations_overlap_1/4"] = maxmin([r, Rt[j_non]], 30)
    print(res, flush=True)
    json.dump(res, open(OUT, "w"), indent=1, default=str)


if __name__ == "__main__":
    main()
