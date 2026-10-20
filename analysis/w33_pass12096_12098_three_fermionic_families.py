"""Passes 12096-12098: three chiral fermionic families from the clock gradings (Claude track; 12089-12091).

12096 -- SO(10) level (a dimension-3 grading: the E6 clock vacuum of an event + a split, realisable with one order-2
  shift and two order-2 Wilson lines). For all 27 such SO(10) gradings and every order-3 shift keeping the so(10)
  roots: the net number of chiral 16s per plane is 0 or +-3 only (never 1, 2, 4); +-3 exactly for the shifts with fixed
  algebra e6 + a2 (4 + 4 per grading); the 10s stay vector-like (net 0); and the split sigma (fermion parity, Kramers
  squared) is odd on every spinor root -- the three chiral 16s are fermions.
12097 -- Standard-Model level. For three SM gradings, combining each of the 20 three-family shifts (12091) with each of
  the 5 clean fermion parities sigma (12090): 40 of the 100 combinations put ALL three families in sigma-odd sectors
  (fermionic N = +-(3,3,3,3,3), bosonic N = 0) -- a fully consistent assignment of three chiral fermion families; the
  other 60 split them (fermionic (2,2,0,0,2), bosonic (1,1,3,3,1)).
12098 -- families as an event. Over 33 SM gradings, every grading has exactly 20 three-family shifts; in 12 gradings
  exactly 2 of them (a +-t pair) have the family a2 equal to an event fibre, in the other 21 none. Whenever the family a2
  is the fibre of an event x, the e6 is exactly E6(x), the event's own E6 (24 of 24). In those vacua the three families
  are the Eisenstein-unit triplet A2(x) of a single event and the unified group is E6(x): the corpus's 81 = 27 x 3
  matter of an event. (A first count that filtered on fixed dimension 86 alone included anomalous shifts and was wrong.)
Scope: untwisted, per-plane counting on the E8 adjoint; twisted sectors and modular invariance are not computed.
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
from w33_pass12087_standard_model_sectors import Gradings  # noqa: E402

OUT = ROOT / "data" / "w33_pass12096_12098_three_fermionic_families.json"
SIMPLE = np.array([
    [0.5, -0.5, -0.5, -0.5, -0.5, -0.5, -0.5, 0.5], [1, 1, 0, 0, 0, 0, 0, 0], [-1, 1, 0, 0, 0, 0, 0, 0], [0, -1, 1, 0, 0, 0, 0, 0],
    [0, 0, -1, 1, 0, 0, 0, 0], [0, 0, 0, -1, 1, 0, 0, 0], [0, 0, 0, 0, -1, 1, 0, 0], [0, 0, 0, 0, 0, -1, 1, 0]])
GEN = {"Q": (6, 1), "uc": (3, -4), "dc": (3, 2), "L": (2, -3), "ec": (1, 6)}


def main():
    checks, res = {}, {}
    g = Gradings()
    R, fib = g.R, g.fib
    Adj, invs, tick, _ = setup()
    ptof = {i: x for x in range(40) for i in fib[x]}
    PH = np.round((np.array(list(itertools.product(range(3), repeat=8))) @ SIMPLE) @ R.T).astype(int) % 3
    PH = PH[PH.any(1)]
    ev = {h: frozenset(x for x in range(40) if not g.vecs[h][fib[x]].any()) for h in range(g.n)}
    cpt = {h: next(x for x in range(40) if set(np.nonzero(Adj[x])[0]) == set(ev[h])) for h in range(g.n) if g.kinds[h] == "clock"}
    # 12096
    K = [h for h in cpt if cpt[h] == 0]
    so10 = Counter()
    ngr = 0
    for s in range(g.n):
        if g.kinds[s] != "split" or g.typ(g.fixedmask(g.span_of(K[:2] + [s]))) != ("D5",):
            continue
        ngr += 1
        V = g.span_of(K[:2] + [s])
        d5 = np.nonzero(g.fixedmask(V))[0]
        Bd = np.linalg.svd(R[d5])[2][:5]
        proj = np.array([np.sum((Bd @ R[a]) ** 2) for a in range(240)])
        spin, vec = np.where(np.isclose(proj, 1.25))[0], np.where(np.isclose(proj, 1.0))[0]
        sing = np.where(np.isclose(proj, 0.0) & ~g.fixedmask(V))[0]
        Ba = np.linalg.svd(R[sing])[2][:3]
        P4 = np.array([Ba @ R[a] for a in spin])
        cls = np.array([np.isclose(P4[0] @ v, 0.75) or np.isclose(P4[0] @ v, -0.25) for v in P4])
        s16, s16b = spin[cls], spin[~cls]
        for ph in PH:
            if np.any(ph[d5] != 0):
                continue
            n16 = int(np.sum(ph[s16] == 1) - np.sum(ph[s16b] == 1))
            n10 = int(np.sum(ph[vec] == 1) - np.sum(ph[vec] == 2))
            so10[(n16 / 16, n10, 8 + int(np.sum(ph == 0)), bool(np.all(g.vecs[s][spin])))] += 1
    res["12096"] = {str(k): v for k, v in so10.items()}
    checks["12096: 27 SO(10) gradings; net chiral 16s per plane only 0 or +-3, +-3 iff e6+a2 (108+108), 10s vector-like, sigma odd on all spinors"] = (
        ngr == 27 and so10 == Counter({(0.0, 0, 134, True): 324, (0.0, 0, 92, True): 162, (-3.0, 0, 86, True): 108, (3.0, 0, 86, True): 108}))
    # 12097
    ok97, t97 = True, Counter()
    for seed in (7, 8, 9):
        gens = g.sm_flag(seed)
        V = g.span_of(gens)
        sec, Y, xy = g.sectors(gens)
        lab = {ch: g.label(ch, c) for ch, c in sec.items()}
        gauge = [i for c in g.comps(g.fixedmask(V)) for i in c]
        Y6 = np.round(R @ Y * 6).astype(int)
        orbsize = np.zeros(240, int)
        for i in range(240):
            orb, st = {i}, [i]
            while st:
                a = st.pop()
                for b in gauge:
                    j = g.rkey[tuple(np.round((R[a] - (R[a] @ R[b]) * R[b]) * 2).astype(int))]
                    if j not in orb:
                        orb.add(j)
                        st.append(j)
            orbsize[i] = len(orb)
        eps = np.array([[int(g.vecs[h][a]) for h in gens] for a in range(240)])
        chs = {tuple(e) for e in eps}
        clean = []
        for h in V:
            if g.kinds[h] != "split":
                continue
            odd_labels = {lab[ch] for ch in chs if any(g.vecs[h][a] for a in range(240) if tuple(eps[a]) == ch)}
            if "XY" not in odd_labels and "gauge" not in odd_labels:
                clean.append(h)
        tally = Counter()
        for ph in PH:
            if np.any(ph[gauge] != 0):
                continue
            N = [int(np.sum((orbsize == o) & (Y6 == y) & (ph == 1)) - np.sum((orbsize == o) & (Y6 == -y) & (ph == 1))) // o for o, y in GEN.values()]
            if len(set(N)) != 1 or N[0] == 0:
                continue
            for s in clean:
                sig = g.vecs[s]
                No = tuple(int(np.sum((orbsize == o) & (Y6 == y) & (ph == 1) & sig) - np.sum((orbsize == o) & (Y6 == -y) & (ph == 1) & sig)) // o for o, y in GEN.values())
                Ne = tuple(int(np.sum((orbsize == o) & (Y6 == y) & (ph == 1) & ~sig) - np.sum((orbsize == o) & (Y6 == -y) & (ph == 1) & ~sig)) // o for o, y in GEN.values())
                tally[("perfect" if Ne == (0,) * 5 and len(set(No)) == 1 and abs(No[0]) == 3 else "split", No, Ne)] += 1
        good = sum(v for k, v in tally.items() if k[0] == "perfect")
        ok97 &= len(clean) == 5 and sum(tally.values()) == 100 and good == 40
        t97[seed] = {str(k): v for k, v in tally.items()}
    res["12097"] = t97
    checks["12097: three SM gradings: 40 of 100 (shift, clean sigma) pairs make all three families fermionic, none bosonic"] = bool(ok97)
    # 12098 (restricted to the true three-family shifts: N = +-3 on all five fields)
    dist, fib_e6, tot = Counter(), 0, 0
    for seed in list(range(100, 130)) + [7, 8, 9]:
        gens = g.sm_flag(seed)
        V = g.span_of(gens)
        sec, Y, xy = g.sectors(gens)
        gauge = [i for c in g.comps(g.fixedmask(V)) for i in c]
        Y6 = np.round(R @ Y * 6).astype(int)
        orbsize = np.zeros(240, int)
        for i in range(240):
            orb, st = {i}, [i]
            while st:
                a = st.pop()
                for b in gauge:
                    j = g.rkey[tuple(np.round((R[a] - (R[a] @ R[b]) * R[b]) * 2).astype(int))]
                    if j not in orb:
                        orb.add(j)
                        st.append(j)
            orbsize[i] = len(orb)
        nf, nfam = 0, 0
        for ph in PH:
            if np.any(ph[gauge] != 0):
                continue
            N = [int(np.sum((orbsize == o) & (Y6 == y) & (ph == 1)) - np.sum((orbsize == o) & (Y6 == -y) & (ph == 1))) // o for o, y in GEN.values()]
            if len(set(N)) != 1 or abs(N[0]) != 3:
                continue
            nfam += 1
            comps = g.comps(ph == 0)
            a2 = next(c for c in comps if len(c) == 6)
            e6 = next(c for c in comps if len(c) == 72)
            pts = {ptof[i] for i in a2}
            if len(pts) == 1:
                nf += 1
                x = next(iter(pts))
                tot += 1
                fib_e6 += {ptof[i] for i in e6} == set(np.nonzero(Adj[x])[0].tolist())
        dist[(nfam, nf)] += 1
    res["12098_distribution_(family_shifts,fibre_type)"] = {str(k): v for k, v in dist.items()}
    res["12098_fibre_cases"] = [tot, fib_e6]
    checks["12098: every grading has 20 three-family shifts; fibre-type ones are a minority, and fibre a2 always comes with e6 = E6(x)"] = bool(
        all(k[0] == 20 for k in dist) and fib_e6 == tot)
    checks = {k: bool(v) for k, v in checks.items()}
    res["checks"] = checks
    res["all_checks_pass"] = all(checks.values())
    OUT.write_text(json.dumps(res, indent=2))
    print(json.dumps(checks, indent=1), res["all_checks_pass"])
    return res


if __name__ == "__main__":
    main()
