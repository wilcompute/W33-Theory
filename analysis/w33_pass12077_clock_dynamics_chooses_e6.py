"""Pass 12077: dynamics on the clocks themselves chooses E6 (Claude track; replaces the withdrawn tick reading, 12072).

Model. The 120 clock involutions theta_c of E8 commute (inner, one torus) and act on the 248 as gradings: +1 on the
Cartan and on even roots, -1 on odd roots. With generators h_c = (1 - theta_c)/2 >= 0 and rates phi >= 0,
H(phi) = sum phi_c h_c is diagonal: 0 on the Cartan, sum_c phi_c [alpha odd under c] on the root alpha, and
F_T = -T log Tr e^{-H/T} is concave in phi (so at fixed total rate a single clock wins, as in 12055).
Exact results:
  1. Counting. Every clock is odd on 112 roots; every root is odd under 56 clocks; the uniform state has H = 7/15 on all
     roots. Pairs: 3360 with 72 roots even under both (their product is a clock: Klein pairs) and 3780 with 64.
  2. Pairs. Z_72 - Z_64 = 8 (1 - x)^2 > 0 with x = e^{-1/(2T)} (Z_72 = 80 + 112x + 56x^2, Z_64 = 72 + 128x + 48x^2):
     at every temperature the clock pair whose product is a clock wins.
  3. Triples (all 280840, exhaustive): five types by the number of roots odd under 0/1/2/3 of them; the KLEIN triples
     {c1, c2, c1 c2} (1120 = 40 at one event + 1080 on hyperbolic lines) have pattern (72, 0, 168, 0):
     Z_K = 80 + 168 e^{-2/(3T)}, and they fix e6 + u(1)^2 (12071).
  4. Capacity. With V = F_T + g sum phi^2, the single clock (Z_1 = 136 + 112 e^{-1/T}) gives way FIRST to a Klein triple,
     at g_K = (3/2)(F_K - F_1), below every pair, every other triple type and the uniform state on T in [0.05, 3].
     The Klein window closes against the uniform state at g = (F_u - F_K)/(1/3 - 1/120).
Reading. On the clocks themselves (rather than on the Clifford ticks, which are not clocks, 12072), the first
multi-clock condensate is a Klein group of clocks, whose common symmetry in E8 is the grand-unified e6 + u(1)^2.
Scope: this diagonal grading model with a capacity cost; global optimality over sets larger than three is not
established (a 25-start multistart can stall; it found larger mixed sets above the Klein window).
"""

import itertools
import json
import sys
from collections import Counter
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))
from w33_pass12053_gate_sets_and_real_forms import setup  # noqa: E402

OUT = ROOT / "data" / "w33_pass12077_clock_dynamics_chooses_e6.json"


def main():
    checks, res = {}, {}
    Adj, invs, tick, fib = setup()
    clocks = [s for k, s in invs if k == "clock"]
    P = np.array(clocks, dtype=np.int8)
    checks["each clock odd on 112 roots; each root odd under 56 clocks"] = set(P.sum(1)) == {112} and set(P.sum(0)) == {56}
    n00 = Counter(int(np.sum((P[a] == 0) & (P[b] == 0))) for a in range(120) for b in range(a + 1, 120))
    checks["pairs: 3360 with 72 even-even roots, 3780 with 64"] = n00 == Counter({72: 3360, 64: 3780})
    prod_clock = 0
    for a in range(120):
        for b in range(a + 1, 120):
            if np.sum((P[a] == 0) & (P[b] == 0)) == 72:
                prod_clock += int((P == (P[a] ^ P[b])).all(1).any())
    checks["the 72-pairs are exactly the pairs whose product is a clock"] = prod_clock == 3360
    idx = np.array(list(itertools.combinations(range(120), 3)), dtype=np.int32)
    types = Counter()
    for ch in range(0, len(idx), 20000):
        I = idx[ch:ch + 20000]
        K = P[I[:, 0]] + P[I[:, 1]] + P[I[:, 2]]
        H = np.stack([(K == j).sum(1) for j in range(4)], 1)
        types.update(map(tuple, H.tolist()))
    res["triple_types"] = {str(k): v for k, v in types.items()}
    checks["triples: five types; Klein type (72,0,168,0) occurs 1120 times"] = len(types) == 5 and types[(72, 0, 168, 0)] == 1120
    klein = next([a, b, int(np.where((P == (P[a] ^ P[b])).all(1))[0][0])] for a in range(120) for b in range(a + 1, 120)
                 if (P == (P[a] ^ P[b])).all(1).any())
    cen = []
    for c in range(120):
        ev = {x for x in range(40) if not clocks[c][fib[x]].any()}
        cen.append(next(x for x in range(40) if set(np.nonzero(Adj[x])[0]) == ev))
    kl_pts = Counter()
    seen = set()
    for a in range(120):
        for b in range(a + 1, 120):
            m = np.where((P == (P[a] ^ P[b])).all(1))[0]
            if len(m):
                t = tuple(sorted((a, b, int(m[0]))))
                if t not in seen:
                    seen.add(t)
                    pts = {cen[i] for i in t}
                    kl_pts["one event" if len(pts) == 1 else ("hyperbolic line" if len(pts) == 3 and not any(Adj[x, y] for x in pts for y in pts if x != y) else "other")] += 1
    checks["Klein triples: 40 at one event + 1080 on three pairwise non-collinear events"] = kl_pts == Counter({"one event": 40, "hyperbolic line": 1080})

    def F(ids, T):
        k = P[list(ids)].sum(0) / len(ids)
        return -T * np.log(8 + np.sum(np.exp(-k / T)))
    x_ok = True
    for T in (0.1, 0.5, 2.0):
        x = np.exp(-1 / (2 * T))
        p72 = klein[:2]
        p64 = next([0, b] for b in range(1, 120) if np.sum((P[0] == 0) & (P[b] == 0)) == 64)
        Z72, Z64 = np.exp(-F(p72, T) / T), np.exp(-F(p64, T) / T)
        x_ok &= abs(Z72 - (80 + 112 * x + 56 * x * x)) < 1e-6 * Z72 and abs(Z64 - (72 + 128 * x + 48 * x * x)) < 1e-6 * Z64
        x_ok &= abs((Z72 - Z64) - 8 * (1 - x) ** 2) < 1e-6 * Z72
    checks["Z_72 - Z_64 = 8(1-x)^2 > 0, x = e^{-1/2T} (closed forms match)"] = bool(x_ok)
    first_ok, win = True, {}
    reps = {}
    for ch in range(0, len(idx), 20000):
        I = idx[ch:ch + 20000]
        K = P[I[:, 0]] + P[I[:, 1]] + P[I[:, 2]]
        H = np.stack([(K == j).sum(1) for j in range(4)], 1)
        for row, h in zip(I, map(tuple, H.tolist())):
            reps.setdefault(h, list(row))
    for T in (0.05, 0.2, 0.5, 1.0, 3.0):
        F1 = F([0], T)
        gK = 1.5 * (F(klein, T) - F1)
        Fu = -T * np.log(8 + 240 * np.exp(-(56 / 120) / T))
        others = [2 * (F([0, b], T) - F1) for b in range(1, 120)] + [1.5 * (F(r, T) - F1) for h, r in reps.items() if h != (72, 0, 168, 0)]
        others.append(120 / 119 * (Fu - F1))
        first_ok &= gK < min(others) - 1e-12
        win[str(T)] = [float(gK), float((Fu - F(klein, T)) / (1 / 3 - 1 / 120))]
        first_ok &= abs(F(klein, T) + T * np.log(80 + 168 * np.exp(-2 / (3 * T)))) < 1e-9 and abs(F1 + T * np.log(136 + 112 * np.exp(-1 / T))) < 1e-9
    res["klein_window"] = win
    checks["capacity: the Klein triple condenses first (below all pairs, all other triple types, uniform; T in [0.05, 3])"] = bool(
        first_ok and all(v[0] < v[1] for v in win.values()))
    checks = {k: bool(v) for k, v in checks.items()}
    res["checks"] = checks
    res["all_checks_pass"] = all(checks.values())
    OUT.write_text(json.dumps(res, indent=2))
    print(json.dumps(checks, indent=1), res["all_checks_pass"])
    return res


if __name__ == "__main__":
    main()
