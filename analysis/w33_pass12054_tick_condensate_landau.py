"""Pass 12054: does the dynamics choose the tick? Landau theory of an Sp(4,3)-invariant tick condensate on the forty
points. The one-event (one-time) phase is a wide, natural region, and it borders the tensor-split phase exactly at
gamma = 2 beta (Claude track; continues 12052-12053).

Order parameter: phi in R^40, one amplitude per tick centre. The permutation module splits along the SRG eigenspaces as
1 + 24 + 15 (adjacency eigenvalues 12, 2, -4). Below the transition the condensate lives in the irrep with the lowest
quadratic coefficient, and the invariant quartics choose the pattern there. With
    V = -r|phi|^2 + u|phi|^4 + beta * sum_p phi_p^4 + gamma * sum_{p~q} phi_p^2 phi_q^2,
the pattern minimises cos(theta) Q1 + sin(theta) Q2 on the unit sphere of the irrep, with (beta, gamma) ~ (cos, sin).
Results (exact rational invariants for the fixed patterns; numerical phase scan):
  * The localising quartic alone (theta = 180, beta < 0) is maximised -- in both irreps -- by the SINGLE-EVENT
    pattern P e_p. Invariants: V15 (35/216, 25/108); V24 (197/540, 77/540).
  * Phase map. V15: flat +-1 (20-sets) -> hyperbolic line -> transitional -> SINGLE EVENT (theta ~ 136-243 deg) ->
    STAGGERED FACTORISATION (+1 on H1, -1 on H2; exact eigenvector, invariants (1/8, 1/4)) -> flat.
    V24: flat -> ... -> signed hyperbolic line (11/96, 7/96) -> SINGLE EVENT (105.56-221.19 deg) -> isotropic line
    (73/360, 59/180) -> flat.
  * Exact boundaries of the event phase:
      V15, event | staggered factorisation:  tan theta_c = 2         (gamma = 2 beta, both negative)
      V24, event | isotropic line:           tan theta_c = 7/8
      V24, signed hyperbolic line | event:   tan theta_c = -1081/301
    The V15 lower edge (~135.5 deg) borders a continuously deforming 3-point pattern and is numerical.
Reading. A tick condensate with a localising single-site quartic picks ONE event -- one tick centre, hence by 12052-12053
one time, with the tick central in its symmetry group -- over about 30% of quartic space in either mode, with no tuning.
In the 15-mode the competing neighbour is the staggered tensor-factorisation phase, the anchor of the split real form.
So the dichotomy of Theorem 7.3 (clock vs split) reappears as two adjacent Landau phases, separated exactly at
gamma = 2 beta. Whether the universe has one time becomes a question about the sign and ratio of two quartic couplings.
Scope: Landau theory with the two simplest quartics (beyond |phi|^4), in one irrep at a time; no derivation of the
couplings; phase scan numerical (60-80 restarts per angle) except the exact crossings.
Not new: Landau theory on permutation modules; SRG spectra.
"""

import json
import sys
from fractions import Fraction as Fr
from pathlib import Path

import numpy as np
from scipy.optimize import minimize

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))
from w33_pass12053_gate_sets_and_real_forms import setup  # noqa: E402

OUT = ROOT / "data" / "w33_pass12054_tick_condensate_landau.json"


def main():
    checks, res = {}, {}
    Adj, invs, tick, fib = setup()
    ev, U = np.linalg.eigh(Adj.astype(float))
    V15, V24 = U[:, np.isclose(ev, -4)], U[:, np.isclose(ev, 2)]
    Ei, Ej = np.nonzero(np.triu(Adj))

    def q(phi):
        phi = phi / np.linalg.norm(phi)
        return np.sum(phi ** 4), np.sum(phi[Ei] ** 2 * phi[Ej] ** 2)

    def proj(V, x):
        return V @ (V.T @ x)

    e = np.eye(40)[0]
    nb = list(np.nonzero(Adj[0])[0])
    line = [0, nb[0]] + [r for r in nb if Adj[nb[0], r]]
    split = next(s for k, s in invs if k == "split")
    F = [x for x in range(40) if not split[fib[x]].any()]
    sub = Adj[np.ix_(F, F)]
    H1 = [F[0]] + [F[j] for j in range(1, 8) if not sub[0, j]]
    H2 = [x for x in F if x not in H1]
    stag = np.zeros(40); stag[H1] = 1; stag[H2] = -1
    pats = {"event_V15": q(proj(V15, e)), "event_V24": q(proj(V24, e)), "staggered_factorisation_V15": q(stag),
            "isotropic_line_V24": q(proj(V24, np.isin(np.arange(40), line).astype(float)))}
    exact = {"event_V15": (Fr(35, 216), Fr(25, 108)), "event_V24": (Fr(197, 540), Fr(77, 540)),
             "staggered_factorisation_V15": (Fr(1, 8), Fr(1, 4)), "isotropic_line_V24": (Fr(73, 360), Fr(59, 180))}
    res["invariants"] = {k: [float(v[0]), float(v[1])] for k, v in pats.items()}
    checks["exact rational invariants of the event, staggered factorisation and isotropic line patterns"] = bool(
        all(abs(pats[k][0] - float(exact[k][0])) < 1e-12 and abs(pats[k][1] - float(exact[k][1])) < 1e-12 for k in exact))
    checks["the staggered factorisation (+1 on H1, -1 on H2) is an exact V15 eigenvector"] = bool(np.allclose(Adj @ stag, -4 * stag))

    def tanc(a, b):
        return (b[0] - a[0]) / (a[1] - b[1])
    t15 = tanc(exact["event_V15"], exact["staggered_factorisation_V15"])
    t24 = tanc(exact["event_V24"], exact["isotropic_line_V24"])
    t24lo = tanc(exact["event_V24"], (Fr(11, 96), Fr(7, 96)))
    res["exact_boundaries"] = dict(V15_event_factorisation=str(t15), V24_event_line=str(t24), V24_hyperbolic_event=str(t24lo))
    checks["exact boundaries: tan = 2 (V15 event|factorisation), 7/8 (V24 event|line), -1081/301 (V24 hyperbolic|event)"] = bool(
        t15 == 2 and t24 == Fr(7, 8) and t24lo == Fr(-1081, 301))

    rng = np.random.default_rng(12054)

    def optimum(V, thd, n=60):
        th = np.radians(thd)
        c, s = np.cos(th), np.sin(th)

        def f(x):
            phi = V @ (x / np.linalg.norm(x))
            return c * np.sum(phi ** 4) + s * np.sum(phi[Ei] ** 2 * phi[Ej] ** 2)
        best = min((minimize(f, rng.normal(size=V.shape[1]), method="BFGS") for _ in range(n)), key=lambda r: r.fun)
        phi = V @ (best.x / np.linalg.norm(best.x))
        a = np.abs(phi)
        return int((a > 0.9 * a.max()).sum()), float(a.max()), phi

    th15 = 180 + np.degrees(np.arctan(2.0))
    th24 = 180 + np.degrees(np.arctan(7 / 8))
    th24lo = 180 + np.degrees(np.arctan(-1081 / 301))
    probes = {"V15 theta=180": optimum(V15, 180)[:2], "V24 theta=180": optimum(V24, 180)[:2],
              "V15 theta_c-1": optimum(V15, th15 - 1)[:2], "V15 theta_c+1": optimum(V15, th15 + 1)[:2],
              "V24 theta_c-1": optimum(V24, th24 - 1)[:2], "V24 theta_c+1": optimum(V24, th24 + 1)[:2],
              "V24 lo-1": optimum(V24, th24lo - 1)[:2], "V24 lo+1": optimum(V24, th24lo + 1)[:2]}
    res["probes"] = probes
    res["theta_c_deg"] = dict(V15=th15, V24=th24, V24_lower=th24lo)
    ev15 = np.sqrt(15 / 40)
    ev24 = np.sqrt(24 / 40)
    checks["theta = 180 (localising quartic): the optimum is the single event in both irreps"] = bool(
        probes["V15 theta=180"][0] == 1 and abs(probes["V15 theta=180"][1] - ev15) < 1e-4
        and probes["V24 theta=180"][0] == 1 and abs(probes["V24 theta=180"][1] - ev24) < 1e-4)
    checks["across each exact boundary the optimum switches between the predicted patterns"] = bool(
        probes["V15 theta_c-1"][0] == 1 and probes["V15 theta_c+1"][0] == 8 and probes["V24 theta_c-1"][0] == 1
        and probes["V24 theta_c+1"][0] == 4 and probes["V24 lo-1"][0] == 4 and probes["V24 lo+1"][0] == 1)
    width15 = th15 - 135.5
    width24 = th24 - th24lo
    res["event_phase_width_deg"] = dict(V15=width15, V24=width24)
    checks["the event phase covers ~30% of quartic space in either irrep"] = bool(0.25 < width15 / 360 < 0.35 and 0.25 < width24 / 360 < 0.35)
    checks = {k: bool(v) for k, v in checks.items()}
    res["checks"] = checks
    res["all_checks_pass"] = all(checks.values())
    OUT.write_text(json.dumps(res, indent=2, default=float))
    print(json.dumps(checks, indent=1), res["all_checks_pass"])
    return res


if __name__ == "__main__":
    main()
