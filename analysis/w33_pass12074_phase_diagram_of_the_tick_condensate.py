"""Pass 12074: the (T, g) phase diagram of the tick condensate with a capacity cost (Claude track; continues 12068).

V_T(phi) = F_T(phi) + g sum phi^2 at fixed sum phi = 1 (12055 model). Exact ingredients:
  * sum of all 120 tick projectors = 40 I, so the uniform (spread) state has H = (2/3) I and F_u = 2/3 - T log 9 exactly;
    the same holds for the three ticks of any one point.
  * single tick Z_1 = 3 + 6e^{-1/T}; compatible context (4 ticks) Z_4 = 1 + 8e^{-3/(4T)};
    the 13-tick star (the four compatible contexts through one tick) has spectrum
    {(15 - 3 sqrt5)/26, (9/13)^7, (15 + 3 sqrt5)/26}.
  * all phases have mean energy 2/3, so at high T the gaps are variances: Var_1 = 2/9, Var_4 = 1/18, Var_u = 0.
Phase boundaries:
  single | context:   g_4(T) = (4/3)(F_4 - F_1)   -> 0 as T -> 0 (~ (4/3) T log 3),  ~ 1/(9T) at high T
  context | spread:   g_u(T) = (120/29)(F_u - F_4) -> 80/29 as T -> 0,                ~ 10/(87T) at high T
  The context window never closes: g_u/g_4 -> 30/29 at high T, and g_u > g_4 on the whole grid T in [0.01, 5].
  For T below T* = 1.39 (solved), the context beats every structured candidate in its window (single, pairs, triples,
  two contexts sharing a tick, the 13-tick star, uniform). Above T*, the 13-tick star enters between context and spread.
Reading. At low temperature a tick capacity produces a sharp sequence: one event (one time) -> one measurement context
(a stabiliser state) -> spread; the context phase is wide (up to g = 80/29 at T -> 0). At high temperature the ordered
window shrinks like 1/T and a star of contexts appears. Scope: this model and the listed candidates; the phase above
the star is not mapped beyond the uniform state.
"""

import json
import sys
from pathlib import Path

import numpy as np
from scipy.optimize import brentq

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))
from w33_pass12055_microscopic_tick_model import ADJ, HS, PROJ, free  # noqa: E402

OUT = ROOT / "data" / "w33_pass12074_phase_diagram_of_the_tick_condensate.json"


def main():
    checks, res = {}, {}

    def kern(idx):
        return int(np.sum(np.linalg.eigvalsh(sum(HS[i] for i in idx)) < 1e-9))

    def ctx_through(p, q):
        line = ([p, q] + [int(r) for r in np.nonzero(ADJ[p])[0] if ADJ[q, r]])[:4]
        sel = [3 * p]
        for x in line[1:]:
            sel.append(next(3 * x + k for k in range(3) if kern(sel + [3 * x + k]) == 1))
        return sel
    p = 0
    lines = []
    for q in [int(x) for x in np.nonzero(ADJ[p])[0]]:
        L = ctx_through(p, q)
        if sorted(L) not in [sorted(m) for m in lines]:
            lines.append(L)
    star = sorted(set(sum(lines, [])))
    two = sorted(set(lines[0] + lines[1]))
    checks["sum of all tick projectors = 40 I; three ticks of one point give H = (2/3) I"] = bool(
        np.allclose(sum(PROJ[i][k] for i in range(40) for k in range(3)), 40 * np.eye(9))
        and np.allclose(sum(HS[i] for i in (0, 1, 2)) / 3, 2 / 3 * np.eye(9)))
    e = np.sort(np.linalg.eigvalsh(sum(HS[i] for i in star) / 13))
    s5 = np.sqrt(5)
    checks["4 compatible contexts through one tick; star of 13 ticks with spectrum {(15-3sqrt5)/26, (9/13)^7, (15+3sqrt5)/26}"] = bool(
        len(lines) == 4 and len(star) == 13 and np.allclose(e, sorted([(15 - 3 * s5) / 26] + [9 / 13] * 7 + [(15 + 3 * s5) / 26] + [1.0] * 0)[:9]) if len(e) == 9 else False)

    def F(idx, T):
        phi = np.zeros(120)
        phi[idx] = 1 / len(idx)
        return free(phi, T)
    F1 = lambda T: -T * np.log(3 + 6 * np.exp(-1 / T))  # noqa: E731
    F4 = lambda T: -T * np.log(1 + 8 * np.exp(-3 / (4 * T)))  # noqa: E731
    Fu = lambda T: 2 / 3 - T * np.log(9)  # noqa: E731
    closed = all(abs(F1(T) - F([0], T)) < 1e-9 and abs(F4(T) - F(lines[0], T)) < 1e-9 and abs(Fu(T) - F(list(range(120)), T)) < 1e-9
                 for T in (0.05, 0.3, 1.0, 3.0))
    checks["closed forms F_1, F_4, F_u match the model"] = bool(closed)
    g4 = lambda T: 4 / 3 * (F4(T) - F1(T))  # noqa: E731
    gu = lambda T: (Fu(T) - F4(T)) / (1 / 4 - 1 / 120)  # noqa: E731
    Ts = np.geomspace(0.01, 5, 300)
    checks["context window open on T in [0.01, 5]: g_4 < g_u"] = bool(np.all([g4(T) < gu(T) for T in Ts]))
    checks["T -> 0: g_4 -> 0, g_u -> 80/29"] = abs(g4(1e-4)) < 1e-3 and abs(gu(1e-4) - 80 / 29) < 2e-3
    hiT = [(gu(T) / g4(T), g4(T) * 9 * T, gu(T) * 87 * T / 10) for T in (200.0, 400.0)]
    res["high_T"] = hiT
    checks["high T: g_4 ~ 1/(9T), g_u ~ 10/(87T), ratio -> 30/29"] = all(abs(r - 30 / 29) < 2e-3 and abs(a - 1) < 5e-3 and abs(b - 1) < 5e-3 for r, a, b in hiT)
    gs = lambda T: (F(star, T) - F4(T)) / (1 / 4 - 1 / 13)  # noqa: E731
    Tstar = brentq(lambda T: gs(T) - gu(T), 1.0, 2.0)
    res["T_star"] = Tstar
    checks["T* (13-tick star enters the window) = 1.39 +- 0.01"] = abs(Tstar - 1.39) < 0.01
    ok = True
    far = next(x for x in range(40) if x != p and not ADJ[p, x])
    cands = {"single": [0], "pair": lines[0][:2], "triple": lines[0][:3], "far_pair": [0, 3 * far], "two_ctx": two, "star": star, "uniform": list(range(120))}
    for T in (0.1, 0.3, 0.6, 1.0, 1.3):
        for gg in np.linspace(g4(T), gu(T), 9)[1:-1]:
            v = F(lines[0], T) + gg / 4
            ok &= all(v < F(c, T) + gg / len(c) for c in cands.values())
    checks["below T*, inside the window the context beats every structured candidate (5 temperatures x 7 couplings)"] = bool(ok)
    res["window"] = {str(T): [float(g4(T)), float(gu(T))] for T in (0.05, 0.2, 0.5, 1.0, 2.0, 5.0)}
    checks = {k: bool(v) for k, v in checks.items()}
    res["checks"] = checks
    res["all_checks_pass"] = all(checks.values())
    OUT.write_text(json.dumps(res, indent=2))
    print(json.dumps(checks, indent=1), res["all_checks_pass"], Tstar)
    return res


if __name__ == "__main__":
    main()
