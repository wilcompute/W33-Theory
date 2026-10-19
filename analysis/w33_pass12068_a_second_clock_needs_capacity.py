"""Pass 12068: what condenses more than one clock -- a tick-capacity cost turns the single tick directly into a whole
compatible CONTEXT, never into a pair (Claude track; 12055, 12061).

Model: the 12055 free energy plus a capacity cost, V_T(phi) = F_T(phi) + g sum phi_a^2 at fixed total rate sum phi = 1
(g > 0 penalises piling all rate on one tick). Compatible ticks on one context L = {x1..x4} with labels sharing a joint
eigenvector (a stabiliser state of L) have exact uniform-weight spectra
    n = 1: {0^3, 1^6}      n = 2: {0, (1/2)^4, 1^4}      n = 3: {0, (2/3)^6, 1^2}      n = 4: {0, (3/4)^8}.
The n-set beats the single tick when g > g_n = n/(n-1) (F_n - F_1). For the full context, with y = e^{-beta/4},
    g_4(T) = (4/3) T log[(3 + 6 y^4) / (1 + 8 y^3)] > 0,  since 3 + 6y^4 - 1 - 8y^3 = 2 (1-y)^2 (1 + 2y + 3y^2).
Results:
  1. g_4 < g_3 < g_2 at every temperature on the grid T in [0.05, 2]: the first condensate beyond one tick is the FULL
     compatible context (4 ticks, one stabiliser state), not a pair; non-collinear pairs and the delocalised uniform
     state have higher thresholds.
  2. Inside the 4-set the optimal weights are uniform (Nelder-Mead, 10 starts, at four (T, g) points).
  3. The context phase is a window g_4 < g < g_u (g_u: context = uniform crossing; T = 0.2: [0.251, 1.083], T = 1:
     [0.114, 0.139] -- narrow at high T). Inside it the context beats every structured candidate (single, compatible
     pair and triple, far pair, uniform). Above it the condensate spreads (the frozen 40-start multistart finds
     spreading and delocalised states there; it can also stall in a 3-set below, so it is a record, not a proof).
Reading. A finite tick capacity does not produce two clocks; it jumps straight to a whole measurement context of four
mutually compatible ticks -- the stabiliser state of the context, which 12055 found as the minimiser of signed Pauli
fields. So positive tick generators with a capacity cost also choose contexts. CAUTION for 12060-12061: those passes
read clock pairs as tick pairs, but the Clifford ticks of 12055 match the 120 clock involutions only in number; under
linear Sp(4,3) the label-0 tick at x is fixed by the whole point stabiliser, not the clock group. Rest-frame statements
for tick condensates therefore wait on an explicit tick-to-clock map (open).
Scope: this model and candidate class; global optimality is numerical.
"""

import json
import sys
from pathlib import Path

import numpy as np
from scipy.optimize import minimize

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))
from w33_pass12055_microscopic_tick_model import ADJ, HS, free  # noqa: E402

OUT = ROOT / "data" / "w33_pass12068_a_second_clock_needs_capacity.json"
SCAN = {  # frozen 40-start softmax/L-BFGS multistart (search driver capacity.py), support sizes of the best found
    "T=0.2": {"0.5": 1, "0.9": 1, "1.1": 3, "1.5": 4, "2.0": 4, "3.0": 4, "5.0": "delocalised", "10.0": "delocalised"},
    "T=1.0": {"0.5": 1, "0.9": 1, "1.1": 4, "1.5": "7 (spreading)", "2.0": "delocalised"},
}


def main():
    checks, res = {}, {}
    p = 0
    q = int(np.nonzero(ADJ[p])[0][0])
    line = ([p, q] + [int(r) for r in np.nonzero(ADJ[p])[0] if ADJ[q, r]])[:4]

    def kern(idx):
        return int(np.sum(np.linalg.eigvalsh(sum(HS[i] for i in idx)) < 1e-9))
    sel = [3 * p]
    for x in line[1:]:
        sel.append(next(3 * x + k for k in range(3) if kern(sel + [3 * x + k]) == 1))
    checks["4 ticks on one context with a common kernel vector (one stabiliser state)"] = kern(sel) == 1 and len(set(i // 3 for i in sel)) == 4
    exact = {1: {0.0: 3, 1.0: 6}, 2: {0.0: 1, 0.5: 4, 1.0: 4}, 3: {0.0: 1, round(2 / 3, 9): 6, 1.0: 2}, 4: {0.0: 1, 0.75: 8}}
    spec_ok = True
    for n in (1, 2, 3, 4):
        e = np.round(np.linalg.eigvalsh(sum(HS[i] for i in sel[:n]) / n), 9)
        spec_ok &= {float(v): int(np.sum(np.isclose(e, v))) for v in sorted(set(e))} == exact[n]
    checks["exact uniform spectra n = 1..4: {0^3,1^6}, {0,(1/2)^4,1^4}, {0,(2/3)^6,1^2}, {0,(3/4)^8}"] = bool(spec_ok)

    def F(idx, T):
        phi = np.zeros(120)
        phi[idx] = 1 / len(idx)
        return free(phi, T)
    far = next(x for x in range(40) if x != p and not ADJ[p, x])
    table, order_ok, closed_ok = {}, True, True
    for T in (0.05, 0.1, 0.2, 0.3, 0.5, 1.0, 2.0):
        F1 = F(sel[:1], T)
        g = {str(n): n / (n - 1) * (F(sel[:n], T) - F1) for n in (2, 3, 4)}
        g["far_pair"] = 2 * (F([sel[0], 3 * far], T) - F1)
        g["uniform"] = 120 / 119 * (free(np.ones(120) / 120, T) - F1)
        table[str(T)] = {k: float(v) for k, v in g.items()}
        order_ok &= g["4"] < g["3"] < g["2"] and g["4"] < g["far_pair"] and g["4"] < g["uniform"]
        y = np.exp(-1 / (4 * T))
        closed_ok &= abs(g["4"] - 4 / 3 * T * np.log((3 + 6 * y ** 4) / (1 + 8 * y ** 3))) < 1e-9
    res["thresholds"] = table
    checks["closed form g_4 = (4/3) T log[(3+6y^4)/(1+8y^3)], y = e^{-1/4T}, matches the model"] = bool(closed_ok)
    ys = np.linspace(0, 0.999, 1000)
    checks["g_4 > 0: 3 + 6y^4 - 1 - 8y^3 = 2(1-y)^2(1+2y+3y^2) > 0 on [0,1)"] = bool(
        np.allclose(2 - 8 * ys ** 3 + 6 * ys ** 4, 2 * (1 - ys) ** 2 * (1 + 2 * ys + 3 * ys ** 2)) and np.all(2 - 8 * ys ** 3 + 6 * ys ** 4 > 0))
    checks["first condensate beyond one tick is the full context: g_4 < g_3 < g_2, g_4 < far pair, g_4 < uniform (T grid)"] = bool(order_ok)
    uni, windows = True, {}
    for T in (0.2, 1.0):
        F1, F4, Fu = F(sel[:1], T), F(sel, T), free(np.ones(120) / 120, T)
        g4 = 4 / 3 * (F4 - F1)
        gu = (Fu - F4) / (1 / 4 - 1 / 120)  # context -> uniform crossing
        windows[str(T)] = [float(g4), float(gu)]
        for gg in (g4 + 0.25 * (gu - g4), g4 + 0.5 * (gu - g4)):
            def ob(z):
                w = np.exp(z - z.max())
                w /= w.sum()
                phi = np.zeros(120)
                phi[sel] = w
                return free(phi, T) + gg * np.sum(w ** 2)
            best = min((minimize(ob, np.random.default_rng(s).normal(size=4), method="Nelder-Mead",
                                 options=dict(xatol=1e-10, fatol=1e-12, maxiter=4000)) for s in range(10)), key=lambda r: r.fun)
            w = np.exp(best.x - best.x.max())
            w /= w.sum()
            cands = [F(sel[:1], T) + gg, F(sel[:2], T) + gg / 2, F(sel[:3], T) + gg / 3, F([sel[0], 3 * far], T) + gg / 2, Fu + gg / 120]
            uni &= np.allclose(w, 0.25, atol=1e-3) and best.fun < min(cands)
    res["context_window_g"] = windows
    checks["context window g_4 < g < g_u exists (T = 0.2, 1); inside it the uniform context is optimal in its 4-set and beats every structured candidate"] = bool(
        uni and all(v[0] < v[1] for v in windows.values()))
    res["frozen_multistart"] = SCAN
    checks = {k: bool(v) for k, v in checks.items()}
    res["checks"] = checks
    res["all_checks_pass"] = all(checks.values())
    OUT.write_text(json.dumps(res, indent=2))
    print(json.dumps(checks, indent=1), res["all_checks_pass"])
    return res


if __name__ == "__main__":
    main()
