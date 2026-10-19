"""Pass 12086: Hosotani dynamics does not select SU(5) or the Standard Model (Claude track; 12078, 12081). NEGATIVE.

Commuting order-2 holonomies on T^k (k = 4, 5), one per circle, generating a subspace of E8/2E8; one-loop
V = -(N_B - N_F) sum_alpha S_R(eps_alpha), with S_R(eps) = sum_{c in F_2^k} (-1)^{c.eps} W_R(c),
W_R(c) = sum_{n = c mod 2, n != 0} |n|_R^{-(4+k)}, |n|_R^2 = sum (n_i R_i)^2.
Results:
  * k = 4, equal radii, one representative subspace of each of the 7 types, ALL 840 bases: the bosonic minimum is d4
    (-239.34); su(5) = a4 is a close second (-238.77, 0.24 % higher); fermion domination picks the torus type.
  * k = 4, 625 radius vectors R in {0.6, 0.8, 1, 1.25, 1.6}^4, all bases: d4 wins every time; a4 never.
  * k = 5, equal radii, 1500 sampled bases per type: a3 (-289.9) beats the Standard-Model type su(3)+su(2) (-275.6).
Reading. The one-loop Wilson-line potential follows the maximal-symmetry branch of 12081 (e6 > so(10) > d4 > a3) and
does not single out su(5) or su(3)+su(2), even with unequal radii. Selecting the Standard-Model grading needs another
ingredient (orbifold projections, fluxes, matter beyond the adjoint). Scope: adjoint loops only; radii grid; sampled
bases at k = 5; truncated lattice sums (|n_i| <= 14 for the radius scan, 20 for equal radii).
"""

import itertools
import json
import random
import sys
from collections import Counter
from functools import lru_cache
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))
from w33_pass12087_standard_model_sectors import Gradings  # noqa: E402

OUT = ROOT / "data" / "w33_pass12086_hosotani_does_not_select_su5.json"


@lru_cache(None)
def S_eq(m, k, N=20):
    rng = np.arange(-N, N + 1)
    grid = np.array(np.meshgrid(*([rng] * k), indexing="ij")).reshape(k, -1).T
    grid = grid[np.any(grid != 0, axis=1)]
    eps = np.array([1] * m + [0] * (k - m))
    return float(np.sum(np.cos(np.pi * grid @ eps) / np.linalg.norm(grid, axis=1) ** (4 + k)))


def main():
    checks, res = {}, {}
    g = Gradings()
    rnd = random.Random(11)

    def VB(basis):
        w = sum(g.vecs[h].astype(int) for h in basis)
        hist = Counter(w.tolist())
        hist[0] = hist.get(0, 0) + 8
        return -sum(c * S_eq(m, len(basis)) for m, c in hist.items())

    def reps_of_dim(d, pool=1500):
        level = {frozenset([i]) for i in range(g.n)}
        for _ in range(d - 1):
            nxt = set()
            for S in rnd.sample(sorted(level, key=sorted), min(len(level), pool)):
                for v in range(g.n):
                    if v not in S:
                        nxt.add(frozenset(S | {g.key[(g.vecs[v] ^ g.vecs[u]).tobytes()] for u in S} | {v}))
            level = nxt
        reps = {}
        for S in level:
            reps.setdefault(g.typ(g.fixedmask(S)), S)
        return reps
    reps4 = reps_of_dim(4)
    eq4 = {}
    for t, S in reps4.items():
        vals = [VB(B) for B in itertools.combinations(sorted(S), 4) if len(g.span_of(list(B))) == 15]
        eq4[t] = (min(vals), max(vals), len(vals))
    res["k4_equal_radii"] = {str(t): v for t, v in eq4.items()}
    checks["k=4 equal radii, all 840 bases of each of 7 types: bosonic minimum d4, a4 second within 0.3 %"] = (
        len(eq4) == 7 and all(v[2] == 840 for v in eq4.values()) and min(eq4, key=lambda t: eq4[t][0]) == ("D4",)
        and sorted(eq4, key=lambda t: eq4[t][0])[1] == ("A4",) and abs(eq4[("A4",)][0] / eq4[("D4",)][0] - 1) < 0.003)
    N = 14
    rng_ = np.arange(-N, N + 1)
    grid = np.array(np.meshgrid(*([rng_] * 4), indexing="ij")).reshape(4, -1).T
    grid = grid[np.any(grid != 0, axis=1)]
    pidx = (grid % 2) @ np.array([8, 4, 2, 1])
    pats = np.array(list(itertools.product(range(2), repeat=4)))
    sign = (-1.0) ** ((pats @ pats.T) % 2)
    pindex = {tuple(p): i for i, p in enumerate(pats)}
    counts = {}
    for t, S in reps4.items():
        if t == ():
            continue
        rows = []
        for B in itertools.combinations(sorted(S), 4):
            if len(g.span_of(list(B))) != 15:
                continue
            c = np.zeros(16)
            for a in range(240):
                c[pindex[tuple(int(g.vecs[h][a]) for h in B)]] += 1
            c[0] += 8
            rows.append(c)
        counts[t] = np.array(rows)
    wins = Counter()
    for Rs in itertools.product([0.6, 0.8, 1.0, 1.25, 1.6], repeat=4):
        w = 1 / np.sqrt(((grid * np.array(Rs)) ** 2).sum(1)) ** 8
        Sv = sign @ np.bincount(pidx, weights=w, minlength=16)
        vals = {t: float(np.min(-(C @ Sv))) for t, C in counts.items()}
        wins[min(vals, key=vals.get)] += 1
    res["k4_radius_scan_winners"] = {str(k): v for k, v in wins.items()}
    checks["k=4, 625 radius vectors, all bases: d4 always the bosonic minimum, a4 never"] = wins == Counter({("D4",): 625})
    reps5 = reps_of_dim(5)
    k5 = {}
    for t, S in reps5.items():
        els = sorted(S)
        vals = []
        for _ in range(3000):
            B = rnd.sample(els, 5)
            if len(g.span_of(B)) == 31:
                vals.append(VB(B))
        k5[t] = min(vals)
    res["k5_equal_radii_min"] = {str(t): v for t, v in k5.items()}
    checks["k=5 equal radii (sampled bases): a3 beats the Standard-Model type su(3)+su(2)"] = (
        ("A3",) in k5 and ("A1", "A2") in k5 and k5[("A3",)] < k5[("A1", "A2")])
    checks = {k: bool(v) for k, v in checks.items()}
    res["checks"] = checks
    res["all_checks_pass"] = all(checks.values())
    OUT.write_text(json.dumps(res, indent=2))
    print(json.dumps(checks, indent=1), res["all_checks_pass"])
    return res


if __name__ == "__main__":
    main()
