"""Passes 12092-12095: four checks on the clock/split GUT picture (Claude track; 12081-12091). One producer, four parts.

12092 -- the 27 SO(10)-making splits are the factorisations through the event. For the E6 vacuum of the three clocks at
  an event p, the splits sigma with span(K, sigma) fixing so(10) (27 of 135, 12089) are exactly the 3 split
  involutions of each of the 9 factorisations containing p; each such factorisation holds 3 far points of p.
12093 -- NEGATIVE: an extra Z3 circle does not move Hosotani toward SU(5). On T^5 (four Z2 holonomies + one order-3
  shift on the fifth circle, all 6561 shifts, 40 bases per type, equal radii), the bosonic minimum is still d4, with
  or without the trivial shift (non-trivial: d4 -437.3 < a4 -428.7).
12094 -- NEGATIVE: the Wilson-line characters do not protect the proton. The pairs of SM sectors whose characters add to
  the X/Y character are exactly (Q, ue) x5 and (L, dN) x10 (and gauge x X/Y): the SU(5) X/Y couplings to
  quark-quark and quark-lepton pairs all survive the grading selection rule.
12095 -- NEGATIVE: the Eisenstein unit gives no family Z3. omega fixes none of the 255 classes, so no SM grading is
  omega-invariant; the omega-orbit of an SM grading is three SM gradings with distinct su(3) and su(2).
"""

import itertools
import json
import random
import sys
from collections import Counter
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))
from w33_pass12052_real_forms_on_forty_points import build  # noqa: E402
from w33_pass12053_gate_sets_and_real_forms import setup  # noqa: E402
from w33_pass12087_standard_model_sectors import Gradings  # noqa: E402

OUT = ROOT / "data" / "w33_pass12092_to_12095_clock_gut_checks.json"
SIMPLE = np.array([
    [0.5, -0.5, -0.5, -0.5, -0.5, -0.5, -0.5, 0.5], [1, 1, 0, 0, 0, 0, 0, 0], [-1, 1, 0, 0, 0, 0, 0, 0], [0, -1, 1, 0, 0, 0, 0, 0],
    [0, 0, -1, 1, 0, 0, 0, 0], [0, 0, 0, -1, 1, 0, 0, 0], [0, 0, 0, 0, -1, 1, 0, 0], [0, 0, 0, 0, 0, -1, 1, 0]])


def main():
    checks, res = {}, {}
    g = Gradings()
    R, fib = g.R, g.fib
    Adj, invs, tick, _ = setup()
    ev = {h: frozenset(x for x in range(40) if not g.vecs[h][fib[x]].any()) for h in range(g.n)}
    cpt = {h: next(x for x in range(40) if set(np.nonzero(Adj[x])[0]) == set(ev[h])) for h in range(g.n) if g.kinds[h] == "clock"}
    # 12092
    p = 0
    K = [h for h in cpt if cpt[h] == p]
    d5 = [s for s in range(g.n) if g.kinds[s] == "split" and g.typ(g.fixedmask(g.span_of(K[:2] + [s]))) == ("D5",)]
    facs = Counter(ev[s] for s in d5)
    through = {ev[h] for h in range(g.n) if g.kinds[h] == "split" and p in ev[h]}
    far = {x for x in range(40) if x != p and not Adj[p, x]}
    checks["12092: the 27 SO(10) splits = 3 x the 9 factorisations through p; each has 3 far points of p"] = (
        len(K) == 3 and len(d5) == 27 and set(facs) == through and len(through) == 9 and set(facs.values()) == {3}
        and all(len(f & far) == 3 for f in through))
    # 12093
    rnd = random.Random(11)
    Nn = 9
    rng_ = np.arange(-Nn, Nn + 1)
    grid = np.array(np.meshgrid(*([rng_] * 5), indexing="ij")).reshape(5, -1).T
    grid = grid[np.any(grid != 0, axis=1)]
    w = 1 / np.linalg.norm(grid, axis=1) ** 9
    W = np.zeros((16, 3))
    np.add.at(W, ((grid[:, :4] % 2) @ np.array([8, 4, 2, 1]), grid[:, 4] % 3), w)
    pats = np.array(list(itertools.product(range(2), repeat=4)))
    sgn = (-1.0) ** ((pats @ pats.T) % 2)
    cosr = np.array([[np.cos(2 * np.pi * r * ph / 3) for r in range(3)] for ph in range(3)])
    Stab = np.einsum("ec,pr,cr->ep", sgn, cosr, W)
    coefs = np.array(list(itertools.product(range(3), repeat=8)))
    PH = np.round((coefs @ SIMPLE) @ R.T).astype(int) % 3
    PHn = PH[PH.any(1)]
    pindex = {tuple(pp): i for i, pp in enumerate(pats)}
    level = {frozenset([i]) for i in range(g.n)}
    for _ in range(3):
        nxt = set()
        for S in rnd.sample(sorted(level, key=sorted), min(len(level), 1500)):
            for v in range(g.n):
                if v not in S:
                    nxt.add(frozenset(S | {g.key[(g.vecs[v] ^ g.vecs[u]).tobytes()] for u in S} | {v}))
        level = nxt
    reps = {}
    for S in level:
        reps.setdefault(g.typ(g.fixedmask(S)), S)
    best_all, best_nt = {}, {}
    for t, S in reps.items():
        if t == ():
            continue
        bases = [B for B in itertools.combinations(sorted(S), 4) if len(g.span_of(list(B))) == 15]
        va, vn = np.inf, np.inf
        for B in rnd.sample(bases, 40):
            E = np.array([pindex[tuple(int(g.vecs[h][a]) for h in B)] for a in range(240)])
            va = min(va, float((-(Stab[E[None, :], PH].sum(1) + 8 * Stab[0, 0])).min()))
            vn = min(vn, float((-(Stab[E[None, :], PHn].sum(1) + 8 * Stab[0, 0])).min()))
        best_all[t], best_nt[t] = va, vn
    res["12093_min_all_shifts"] = {str(k): v for k, v in best_all.items()}
    res["12093_min_nontrivial_shifts"] = {str(k): v for k, v in best_nt.items()}
    checks["12093: with a Z3 circle (any or non-trivial shift) the bosonic minimum is still d4, ahead of a4"] = (
        min(best_all, key=best_all.get) == ("D4",) and min(best_nt, key=best_nt.get) == ("D4",) and best_nt[("D4",)] < best_nt[("A4",)])
    # 12094
    gens = g.sm_flag()
    sec, Y, xy = g.sectors(gens)
    lab = {ch: g.label(ch, c) for ch, c in sec.items()}
    chXY = next(ch for ch, l in lab.items() if l == "XY")
    pairs = Counter(tuple(sorted((lab[a], lab[b]))) for a, b in itertools.combinations_with_replacement(sorted(sec), 2)
                    if tuple((x + y) % 2 for x, y in zip(a, b)) == chXY)
    res["12094_xy_pairs"] = {str(k): v for k, v in pairs.items()}
    checks["12094: X/Y character pairs are (Q,ue) x5, (L,dN) x10, (gauge,XY) x1 -- no grading protection of the proton"] = (
        pairs == Counter({("Q", "ue"): 5, ("L", "dN"): 10, ("XY", "gauge"): 1}))
    # 12095
    Rr, C, fib2, refl, perm = build()
    Wp = perm(np.linalg.matrix_power(C, 10))
    om = np.array([g.key[g.vecs[h][Wp].tobytes()] for h in range(g.n)])
    V = g.span_of(gens)
    orbit = [V, frozenset(om[list(V)].tolist()), frozenset(om[om[list(V)]].tolist())]
    su3 = {frozenset(next(c for c in g.comps(g.fixedmask(Wd)) if len(c) == 6)) for Wd in orbit}
    su2 = {frozenset(next(c for c in g.comps(g.fixedmask(Wd)) if len(c) == 2)) for Wd in orbit}
    checks["12095: omega fixes no class; the SM grading is not omega-invariant; its orbit is 3 SM gradings with distinct su(3), su(2)"] = bool(
        int(np.sum(om == np.arange(g.n))) == 0 and orbit[0] != orbit[1] and all(g.typ(g.fixedmask(Wd)) == ("A1", "A2") for Wd in orbit)
        and len(su3) == 3 and len(su2) == 3)
    checks = {k: bool(v) for k, v in checks.items()}
    res["checks"] = checks
    res["all_checks_pass"] = all(checks.values())
    OUT.write_text(json.dumps(res, indent=2))
    print(json.dumps(checks, indent=1), res["all_checks_pass"])
    return res


if __name__ == "__main__":
    main()
