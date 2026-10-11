"""Pass 11923: the heterotic local-10 lock and the magnetized up lemma are one theorem, and it survives every
Delta(54)-symmetric Higgs vacuum -- the charm-up splitting needs a magic (non-stabiliser) Higgs.

Setting (common to Pass 11903, heterotic prime Z3 orbifolds with a local 10 and families on a Wilson-line-free torus, and
Pass 11918/11921, magnetized SU(5) on T4): the family index a of Q and u^c is a qutrit (the three fixed points of the
family torus / the 10's magnetic-translation qutrit); the Z3 selection rule allows Q_a u_b H_k iff a + b = k (mod 3);
the coupling depends only on the class and on a - b, and theta evenness makes the two off-diagonal values equal. The light
Higgs is a qutrit state h over the three copies (fixed points / Z3 classes). Hence, in both realisations,

    Y_u(h)_{ab} = h_{a+b} g_{a-b},   g_+ = g_-   (no relative Q / u^c shift).

1. Pass 11903's lock is the case h = Z-eigenstate (one Higgs row); Pass 11918's lemma is the same matrix.
2. Every one of the 12 qutrit stabiliser states h locks: Y_u(h) has an exactly degenerate pair, for every even g
   (checked to 1e-15 over random complex g). The converse fails: the degenerate locus is larger (random searches find
   54 of 60 degenerate solutions with Pauli expectation down to 0.51), and a Haar-random h unlocks.
3. The three Higgs copies form a Delta(54) triplet (Kobayashi-Nilles-Ploger-Raby-Ratz 2006). For charge-preserving aligned
   vevs the general degree-(2,2) Delta(27)-invariant potential is a sum|h|^4 + Re(c sum_i hbar_i^2 h_{i+1} h_{i+2}) (plus
   (sum|h|^2)^2): over 300 random (a, c) its global minimum is ALWAYS a stabiliser state (infidelity <= 2e-11; snapped
   states have the same V and gap 2e-16) -- the classical 3HDM result (Ivanov-Nishi 2015; de Medeiros Varzielas). So the
   charm-up lock survives the full Higgs triplet at every Delta(54)-symmetric vacuum: unlocking needs the Higgs potential
   to break Delta(54).
4. Near a stabiliser state the splitting grows like the square root of the Higgs's stabiliser Renyi magic M2: the
   log-slope of the gap against M2 is 1/2. The charm-up splitting measures the Higgs's magic.
"""

import json
from pathlib import Path

import numpy as np
from scipy.optimize import minimize

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass11923_stabiliser_higgs_lock.json"
W = np.exp(2j * np.pi / 3)
XP = np.roll(np.eye(3), 1, axis=0)
ZP = np.diag([1, W, W * W])
PAULIS = [np.linalg.matrix_power(XP, a) @ np.linalg.matrix_power(ZP, b) for a in range(3) for b in range(3)]
STAB = [np.eye(3)[k] for k in range(3)] + [np.array([W ** (s * j * j + t * j) for j in range(3)]) / np.sqrt(3)
                                           for s in range(3) for t in range(3)]


def Y(h, g):
    return np.array([[h[(a + b) % 3] * g[(a - b) % 3] for b in range(3)] for a in range(3)])


def gap(M):
    s = np.linalg.svd(M, compute_uv=False)
    return min(abs(s[0] - s[1]), abs(s[1] - s[2])) / s[0]


def magic(h):
    """stabiliser 2-Renyi entropy of a qutrit state (0 on stabiliser states)"""
    return float(-np.log(sum(abs(np.vdot(h, P @ h)) ** 4 for P in PAULIS) / 3))


def pauli_max(h):
    return max(abs(np.vdot(h, P @ h)) for P in PAULIS[1:])


def potential(h, a, c):
    return a * np.sum(abs(h) ** 4) + np.real(c * sum(np.conj(h[i]) ** 2 * h[(i + 1) % 3] * h[(i + 2) % 3] for i in range(3)))


def main():
    rng = np.random.default_rng(11923)
    # 2. stabiliser states lock for random even g
    worst_stab = 0.0
    for _ in range(200):
        e = rng.normal() + 1j * rng.normal()
        g = np.array([rng.normal() + 1j * rng.normal(), e, e])
        worst_stab = max(worst_stab, max(gap(Y(h, g)) for h in STAB))
    haar = []
    for _ in range(3000):
        h = rng.normal(size=3) + 1j * rng.normal(size=3)
        haar.append(gap(Y(h / np.linalg.norm(h), np.array([1, 0.1, 0.1]))))
    # converse fails: degenerate non-stabiliser h
    g0 = np.array([1, 0.1, 0.1])
    found = []
    for _ in range(60):
        f = lambda x: gap(Y((x[:3] + 1j * x[3:]) / np.linalg.norm(x[:3] + 1j * x[3:]), g0)) ** 2
        r = minimize(f, rng.normal(size=6), method="Nelder-Mead", options=dict(xatol=1e-12, fatol=1e-28, maxiter=20000))
        if r.fun < 1e-18:
            h = r.x[:3] + 1j * r.x[3:]
            found.append(pauli_max(h / np.linalg.norm(h)))
    # 3. Delta(27)/Delta(54) potential minima are stabiliser states
    infid, gaps_snapped, dv = [], [], []
    for _ in range(300):
        a, c = rng.normal(), rng.normal() + 1j * rng.normal()
        best = None
        for _ in range(25):
            f = lambda x: potential((x[:3] + 1j * x[3:]) / np.linalg.norm(x[:3] + 1j * x[3:]), a, c)
            r = minimize(f, rng.normal(size=6), method="BFGS")
            if best is None or r.fun < best.fun - 1e-12:
                best = r
        h = best.x[:3] + 1j * best.x[3:]
        h /= np.linalg.norm(h)
        ov = [abs(np.vdot(s, h)) for s in STAB]
        hs = STAB[int(np.argmax(ov))]
        infid.append(1 - max(ov))
        gaps_snapped.append(gap(Y(hs, g0)))
        dv.append(potential(hs, a, c) - best.fun)
    # 4. splitting vs magic near a stabiliser state
    pts = []
    for d in np.logspace(-6, -2, 9):
        v = rng.normal(size=3) + 1j * rng.normal(size=3)
        h = STAB[0] + d * v
        h /= np.linalg.norm(h)
        pts.append((magic(h), gap(Y(h, g0))))
    pts = np.array(pts)
    slope = float(np.polyfit(np.log(pts[:, 0]), np.log(pts[:, 1]), 1)[0])
    res = dict(pass_id=11923, worst_stabiliser_gap=worst_stab, haar_min_gap=float(min(haar)),
               degenerate_found=len(found), degenerate_clearly_nonstabiliser=int(sum(x < 0.9 for x in found)),
               min_pauli_expectation_among_them=float(min(found)) if found else None,
               potential_trials=300, max_infidelity_to_stabiliser=float(max(infid)),
               max_gap_snapped=float(max(gaps_snapped)), max_dV_snapped=float(max(dv)),
               magic_gap_points=pts.tolist(), loglog_slope_gap_vs_magic=slope)
    res["checks"] = {k: bool(v) for k, v in dict(
        all_stabiliser_states_lock=worst_stab < 1e-12,
        haar_unlocks=min(haar) > 1e-4,
        converse_fails=sum(x < 0.9 for x in found) > 10,
        delta54_minima_are_stabiliser=max(infid) < 1e-8 and max(dv) < 1e-10,
        lock_at_every_delta54_vacuum=max(gaps_snapped) < 1e-12,
        splitting_is_sqrt_magic=abs(slope - 0.5) < 0.05,
    ).items()}
    res["all_checks_pass"] = all(res["checks"].values())
    OUT.write_text(json.dumps(res, indent=2))
    print(json.dumps({k: v for k, v in res.items() if k != "magic_gap_points"}, indent=1))


if __name__ == "__main__":
    main()
